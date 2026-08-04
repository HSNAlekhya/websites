from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class HomePageTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Women\'s Wear', slug='womens-wear', description='Trendy women fashion')
        self.product = Product.objects.create(
            name='Floral Kurti',
            slug='floral-kurti',
            category=self.category,
            price=1299,
            description='Elegant festive wear',
            badge='New',
            is_featured=True,
            brand='Zara',
            colour='Pink',
            discount=20,
            size='M',
            stock=8,
            material='Cotton',
            delivery_days=3,
        )
        for index in range(20):
            Product.objects.create(
                name=f'Catalog Item {index + 1}',
                slug=f'catalog-item-{index + 1}',
                category=self.category,
                price=1000 + index,
                description='Seasonal fashion',
                badge='Bestseller',
                is_featured=True,
                brand='StyleHub',
                colour='Black',
                discount=15,
                size='S',
                stock=10,
                material='Cotton',
                delivery_days=4,
            )

    def test_home_page_renders_storefront(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Premium fashion made easy')
        self.assertContains(response, 'Fresh styles for every mood and moment.')
        self.assertContains(response, 'href="#featured"')
        self.assertContains(response, 'href="#deals"')
        self.assertContains(response, "Women's Wear")
        self.assertContains(response, "Men's Wear")

    def test_category_page_shows_products(self):
        response = self.client.get(reverse('category_products', args=['womens-wear']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Floral Kurti')
        self.assertGreaterEqual(len(response.context['products']), 20)

    def test_product_detail_page_shows_details(self):
        response = self.client.get(reverse('product_detail', args=['womens-wear', 'floral-kurti']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product details')
        self.assertContains(response, 'Zara')
        self.assertContains(response, 'Pink')

    def test_category_page_creates_missing_category(self):
        response = self.client.get(reverse('category_products', args=['summer-collection']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Summer Collection')
        self.assertContains(response, 'Showing up to 20 items from this category.')

    def test_category_page_seeds_20_items_for_new_category(self):
        response = self.client.get(reverse('category_products', args=['mens-wear']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 20)
        self.assertContains(response, 'Mens Wear')

    def test_products_without_images_get_a_name_based_image(self):
        product = Product.objects.create(
            name='Fallback Image Product',
            slug='fallback-image-product',
            category=self.category,
            price=1299,
            description='Should show an image',
            image_url='',
            brand='StyleHub',
            colour='Blue',
            size='M',
            stock=3,
            material='Cotton',
            delivery_days=2,
        )

        response = self.client.get(reverse('product_detail', args=['womens-wear', product.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/static/shop/images/')
        self.assertNotContains(response, 'source.unsplash.com')
        self.assertIn('/static/shop/images/', response.context['product'].image_url)

    def test_kurti_and_dress_images_use_clothing_shapes(self):
        product = Product.objects.create(
            name='Floral Kurti',
            slug='floral-kurti-shape-test',
            category=self.category,
            price=1499,
            description='Should show a realistic garment illustration',
            image_url='',
            brand='StyleHub',
            colour='Pink',
            size='M',
            stock=4,
            material='Cotton',
            delivery_days=2,
        )

        response = self.client.get(reverse('product_detail', args=['womens-wear', product.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('/static/shop/images/', response.context['product'].image_url)
        self.assertIn('.svg', response.context['product'].image_url.lower())
        self.assertNotIn('data:image', response.context['product'].image_url.lower())

    def test_product_detail_page_assigns_name_based_image_when_missing(self):
        product = Product.objects.create(
            name='Blue Denim Jacket',
            slug='blue-denim-jacket',
            category=self.category,
            price=2499,
            description='Cool everyday style',
            image_url='',
            brand='StyleHub',
            colour='Blue',
            size='M',
            stock=5,
            material='Cotton',
            delivery_days=3,
        )

        response = self.client.get(reverse('product_detail', args=['womens-wear', product.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/static/shop/images/')
        self.assertNotContains(response, 'source.unsplash.com')
        self.assertIn('/static/shop/images/', response.context['product'].image_url)

    def test_cart_page_shows_added_items(self):
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 1)

        cart_response = self.client.get(reverse('cart'))
        self.assertEqual(cart_response.status_code, 200)
        self.assertContains(cart_response, 'Floral Kurti')
