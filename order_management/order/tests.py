from django.test import TestCase

from .models import Order


class OrderCrudTests(TestCase):
	def setUp(self):
		self.order = Order.objects.create(
			customer_name='Taylor Reed',
			customer_email='taylor@example.com',
			product_name='Desk lamp',
			quantity=2,
			unit_price='24.50',
		)

	def test_order_pages_render(self):
		for url in [
			'/',
			f'/orders/{self.order.pk}/',
			f'/orders/{self.order.pk}/edit/',
			f'/orders/{self.order.pk}/delete/',
			'/orders/new/',
		]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 200)

	def test_create_update_and_delete_order(self):
		response = self.client.post('/orders/new/', {
			'customer_name': 'Jamie Chen',
			'customer_email': 'jamie@example.com',
			'product_name': 'Notebook',
			'quantity': 3,
			'unit_price': '12.00',
			'status': 'processing',
		})
		self.assertEqual(response.status_code, 302)
		created_order = Order.objects.get(customer_email='jamie@example.com')
		self.assertEqual(created_order.total_price, 36)

		response = self.client.post(f'/orders/{created_order.pk}/edit/', {
			'customer_name': 'Jamie Chen',
			'customer_email': 'jamie@example.com',
			'product_name': 'Notebook set',
			'quantity': 4,
			'unit_price': '12.00',
			'status': 'shipped',
		})
		self.assertEqual(response.status_code, 302)
		created_order.refresh_from_db()
		self.assertEqual(created_order.product_name, 'Notebook set')
		self.assertEqual(created_order.status, 'shipped')

		response = self.client.post(f'/orders/{created_order.pk}/delete/')
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Order.objects.filter(pk=created_order.pk).exists())
