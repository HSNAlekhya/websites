import re
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.utils import timezone

from .models import Coupon


class CouponAgent:
    """Provider-free task agent for coupon-management commands."""

    def run(self, command):
        text = ' '.join(command.strip().split())
        lowered = text.lower()
        if not text:
            return 'Tell me what to do, such as “create a 15% coupon called SAVE15”.', []
        if lowered in {'help', '?', 'what can you do'}:
            return ('I can create, pause, activate, delete, and inspect coupons. Try: '
                    '“create a 20% coupon called SPRING20”, “pause SPRING20”, '
                    'or “show active coupons”.'), []
        if re.search(r'\b(show|list|find|view|display|inspect|get)\b', lowered):
            return self._list_coupons(lowered)
        if re.search(r'\b(delete|remove)\b', lowered):
            return self._delete(text)
        if re.search(r'\b(pause|deactivate|disable)\b', lowered):
            return self._set_active(text, False)
        if re.search(r'\b(activate|enable|resume)\b', lowered):
            return self._set_active(text, True)
        if re.search(r'\b(create|make|add)\b', lowered):
            return self._create(text)
        return ('I did not recognize that task. Ask me to create, pause, activate, delete, '
                'or list coupons. Type “help” for examples.'), []

    def _code(self, text):
        named_code = re.search(r'\b(?:called|named|code)\s*[:=-]?\s*([A-Z][A-Z0-9_-]{2,39})\b', text, re.IGNORECASE)
        if named_code:
            return named_code.group(1).upper()
        matches = re.findall(r'\b[A-Z][A-Z0-9_-]{2,39}\b', text.upper())
        ignored = {
            'CREATE', 'CREATED', 'MAKE', 'MAke', 'ADD', 'COUPON', 'COUPONS', 'CALLED', 'CALL',
            'NAMED', 'CODE', 'DELETE', 'DELETED', 'REMOVE', 'PAUSE', 'PAUSED', 'ACTIVATE',
            'ACTIVATED', 'CONFIRM', 'YES', 'SHOW', 'LIST', 'FIND', 'VIEW', 'DISPLAY', 'INSPECT',
            'GET', 'THE', 'A', 'AN', 'FOR', 'WITH', 'PERCENT', 'PERCENTAGE', 'DISCOUNT', 'AMOUNT',
        }
        return next((match for match in matches if match not in ignored), None)

    def _get_coupon(self, code):
        if not code:
            return None, 'Include a coupon code, for example “pause SAVE15”.'
        try:
            return Coupon.objects.get(code=code), None
        except Coupon.DoesNotExist:
            return None, f'I could not find a coupon called {code}.'

    def _list_coupons(self, command):
        coupons = list(Coupon.objects.all())
        if 'active' in command:
            coupons = [coupon for coupon in coupons if coupon.status == 'Active']
        elif 'scheduled' in command:
            coupons = [coupon for coupon in coupons if coupon.status == 'Scheduled']
        if not coupons:
            return 'There are no matching coupons.', []
        summary = ', '.join(f'{coupon.code} ({coupon.discount_display}, {coupon.status.lower()})' for coupon in coupons[:8])
        if len(coupons) > 8:
            summary += f' and {len(coupons) - 8} more'
        return f'I found {len(coupons)} coupon(s): {summary}.', [coupon.code for coupon in coupons]

    def _set_active(self, text, active):
        coupon, error = self._get_coupon(self._code(text))
        if error:
            return error, []
        coupon.is_active = active
        coupon.save(update_fields=['is_active', 'updated_at'])
        action = 'activated' if active else 'paused'
        return f'{coupon.code} is now {action}.', [coupon.code]

    def _delete(self, text):
        code = self._code(text)
        coupon, error = self._get_coupon(code)
        if error:
            return error, []
        coupon.delete()
        return f'{code} was deleted immediately.', [code]

    def _create(self, text):
        code = self._code(text)
        if not code:
            return 'Include a code, for example “create a 15% coupon called SAVE15”.', []
        percentage = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent|percentage)', text, re.IGNORECASE)
        fixed = re.search(r'(?:\$|usd\s*)(\d+(?:\.\d+)?)|(?:fixed|amount)\s+(?:of\s+)?(?:\$|usd\s*)?(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if percentage:
            discount_type, value = Coupon.PERCENTAGE, percentage.group(1)
        elif fixed:
            discount_type, value = Coupon.FIXED, fixed.group(1) or fixed.group(2)
        else:
            return 'Include a discount, such as 15% or $10.', []
        try:
            discount_value = Decimal(value)
        except InvalidOperation:
            return 'I could not read that discount value.', []
        if Coupon.objects.filter(code=code).exists():
            return f'{code} already exists. Try a different code.', []
        coupon = Coupon(code=code, description='Created by Coupon Agent', discount_type=discount_type,
                        discount_value=discount_value, expires_at=timezone.now() + timedelta(days=30))
        try:
            coupon.full_clean()
            coupon.save()
        except Exception as error:
            return str(error), []
        return f'Created {coupon.code} with a {coupon.discount_display} discount, active for 30 days.', [coupon.code]