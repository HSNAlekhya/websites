from django.db import models
from django.urls import reverse


class Order(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('processing', 'Processing'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
	]

	customer_name = models.CharField(max_length=120)
	customer_email = models.EmailField()
	product_name = models.CharField(max_length=160)
	quantity = models.PositiveIntegerField(default=1)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	@property
	def total_price(self):
		return self.quantity * self.unit_price

	def __str__(self):
		return f'Order #{self.pk} - {self.customer_name}'

	def get_absolute_url(self):
		return reverse('order-detail', kwargs={'pk': self.pk})
