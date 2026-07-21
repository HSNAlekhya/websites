from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactCrudTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Alice Johnson',
            email='alice@example.com',
            phone='1234567890',
            information='Primary contact',
        )

    def test_list_contacts(self):
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Johnson')

    def test_create_contact(self):
        response = self.client.post(
            reverse('contact_create'),
            {
                'name': 'Bob Smith',
                'email': 'bob@example.com',
                'phone': '0987654321',
                'information': 'New contact',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('contact_list'))
        self.assertTrue(Contact.objects.filter(name='Bob Smith').exists())

    def test_update_contact(self):
        response = self.client.post(
            reverse('contact_update', args=[self.contact.pk]),
            {
                'name': 'Alice Updated',
                'email': 'alice@example.com',
                'phone': '1234567890',
                'information': 'Updated contact',
            },
            follow=True,
        )
        self.assertRedirects(response, reverse('contact_list'))
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Alice Updated')

    def test_delete_contact(self):
        response = self.client.post(reverse('contact_delete', args=[self.contact.pk]), follow=True)
        self.assertRedirects(response, reverse('contact_list'))
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())
