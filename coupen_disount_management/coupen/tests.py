from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Coupon
from .agent import CouponAgent


class CouponManagementTests(TestCase):
	def valid_payload(self, **overrides):
		payload = {
			'code': 'WELCOME10',
			'description': 'A welcome discount',
			'discount_type': 'percentage',
			'discount_value': '10',
			'minimum_purchase': '25',
			'usage_limit': '100',
			'starts_at': timezone.now().strftime('%Y-%m-%dT%H:%M'),
			'expires_at': (timezone.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M'),
			'is_active': 'on',
		}
		payload.update(overrides)
		return payload

	def test_create_coupon_and_show_it_on_dashboard(self):
		response = self.client.post(reverse('coupon_create'), self.valid_payload())

		self.assertRedirects(response, reverse('dashboard'))
		self.assertTrue(Coupon.objects.filter(code='WELCOME10').exists())
		dashboard = self.client.get(reverse('dashboard'))
		self.assertContains(dashboard, 'WELCOME10')
		self.assertContains(dashboard, '10%')

	def test_percentage_discount_cannot_exceed_one_hundred(self):
		coupon = Coupon(**self.valid_payload(discount_value='101'))

		with self.assertRaisesMessage(Exception, 'Percentage discounts cannot exceed 100%'):
			coupon.full_clean()

	def test_agent_creates_and_pauses_coupon(self):
		message, affected = CouponAgent().run('create a 15 percent coupon named SAVE15')

		self.assertIn('Created SAVE15', message)
		self.assertEqual(affected, ['SAVE15'])
		pause_message, _ = CouponAgent().run('pause SAVE15')
		self.assertEqual(pause_message, 'SAVE15 is now paused.')
		self.assertEqual(Coupon.objects.get(code='SAVE15').status, 'Paused')

	def test_agent_view_alias_returns_existing_coupons(self):
		Coupon.objects.create(code='VIEW10', discount_type=Coupon.PERCENTAGE,
		                      discount_value=10, expires_at=timezone.now() + timedelta(days=1))

		message, affected = CouponAgent().run('view all coupons')

		self.assertIn('VIEW10', message)
		self.assertEqual(affected, ['VIEW10'])

	def test_agent_endpoint_executes_the_submitted_task(self):
		response = self.client.post(reverse('agent_task'), {'command': 'create a $10 coupon named SAVE10'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Created SAVE10')
		self.assertTrue(Coupon.objects.filter(code='SAVE10', discount_type=Coupon.FIXED).exists())

	def test_agent_deletes_coupon_immediately(self):
		coupon = Coupon.objects.create(code='REMOVE10', discount_type=Coupon.PERCENTAGE,
		                              discount_value=10, expires_at=timezone.now() + timedelta(days=1))

		message, _ = CouponAgent().run('delete REMOVE10')
		self.assertEqual(message, 'REMOVE10 was deleted immediately.')
		self.assertFalse(Coupon.objects.filter(pk=coupon.pk).exists())
