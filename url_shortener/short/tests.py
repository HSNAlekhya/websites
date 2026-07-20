from django.test import TestCase
from django.urls import reverse

from .models import ShortURL


class ShortURLTests(TestCase):
    def test_home_page_displays_shortener_form(self):
        response = self.client.get(reverse('short:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shorten a long URL')

    def test_shortening_creates_a_short_link_and_redirects(self):
        response = self.client.post(
            reverse('short:home'),
            {'original_url': 'https://example.com/articles/long-url-example'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'http://testserver/')

        short_url = ShortURL.objects.get(original_url='https://example.com/articles/long-url-example')
        redirect_response = self.client.get(
            reverse('short:redirect', kwargs={'short_code': short_url.short_code})
        )

        self.assertEqual(redirect_response.status_code, 302)
        self.assertEqual(redirect_response.url, 'https://example.com/articles/long-url-example')
