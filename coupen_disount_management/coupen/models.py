from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
	PERCENTAGE = 'percentage'
	FIXED = 'fixed'
	DISCOUNT_TYPES = ((PERCENTAGE, 'Percentage'), (FIXED, 'Fixed amount'))

	code = models.CharField(max_length=40, unique=True)
	description = models.CharField(max_length=180, blank=True)
	discount_type = models.CharField(max_length=12, choices=DISCOUNT_TYPES, default=PERCENTAGE)
	discount_value = models.DecimalField(max_digits=10, decimal_places=2)
	minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	usage_limit = models.PositiveIntegerField(null=True, blank=True)
	used_count = models.PositiveIntegerField(default=0)
	starts_at = models.DateTimeField(default=timezone.now)
	expires_at = models.DateTimeField()
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created_at',)

	def clean(self):
		errors = {}
		if self.discount_value <= 0:
			errors['discount_value'] = 'Discount value must be greater than zero.'
		if self.discount_type == self.PERCENTAGE and self.discount_value > 100:
			errors['discount_value'] = 'Percentage discounts cannot exceed 100%.'
		if self.minimum_purchase < 0:
			errors['minimum_purchase'] = 'Minimum purchase cannot be negative.'
		if self.expires_at and self.starts_at and self.expires_at <= self.starts_at:
			errors['expires_at'] = 'Expiration must be after the start date.'
		if errors:
			raise ValidationError(errors)

	@property
	def status(self):
		now = timezone.now()
		if not self.is_active:
			return 'Paused'
		if self.expires_at <= now:
			return 'Expired'
		if self.starts_at > now:
			return 'Scheduled'
		if self.usage_limit and self.used_count >= self.usage_limit:
			return 'Used up'
		return 'Active'

	@property
	def discount_display(self):
		if self.discount_type == self.PERCENTAGE:
			value = format(self.discount_value, 'f').rstrip('0').rstrip('.')
			return f'{value}%'
		return f'${self.discount_value:,.2f}'

	def __str__(self):
		return self.code
