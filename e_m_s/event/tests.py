from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Event


class EventViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')

    def test_home_page_requires_login(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_home_page_lists_events_for_logged_in_user(self):
        self.client.force_login(self.user)
        Event.objects.create(title='Launch Party', description='Community event', date=date(2026, 8, 1), status='Planned')

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Launch Party')

    def test_create_event(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('event-create'), {
            'title': 'Hackathon',
            'description': 'Build something useful',
            'date': '2026-09-01',
            'status': 'Planned',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(title='Hackathon').exists())
