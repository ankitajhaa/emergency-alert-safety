from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase

from alerts.models import Alert


ALERTS_URL = reverse('alerts-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AlertApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_cannot_create_alert(self):
        user = create_user(
            email='user@test.com',
            password='pass123',
            name='User',
            role='USER'
        )
        self.client.force_authenticate(user)

        payload = {
            'title': 'Fire',
            'description': 'Danger',
            'severity': 'HIGH',
        }

        res = self.client.post(ALERTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_alert(self):
        admin = create_user(
            email='admin@test.com',
            password='pass123',
            name='Admin',
            role='ADMIN'
        )
        self.client.force_authenticate(admin)

        payload = {
            'title': 'Fire',
            'description': 'Danger',
            'severity': 'HIGH',
        }

        res = self.client.post(ALERTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_acknowledge_alert(self):
        user = create_user(
            email='user@test.com',
            password='pass123',
            name='User',
            role='USER'
        )
        self.client.force_authenticate(user)

        alert = Alert.objects.create(
            title='Fire',
            description='Danger',
            severity='HIGH',
            created_by=user,
        )

        url = reverse('alerts-ack', args=[alert.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_ack_twice(self):
        user = create_user(
            email='user@test.com',
            password='pass123',
            name='User',
            role='USER'
        )
        self.client.force_authenticate(user)

        alert = Alert.objects.create(
            title='Fire',
            description='Danger',
            severity='HIGH',
            created_by=user,
        )

        url = reverse('alerts-ack', args=[alert.id])

        self.client.post(url)
        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_sees_only_active_alerts(self):
        user = create_user(
            email='user@test.com',
            password='pass123',
            name='User',
            role='USER'
        )
        self.client.force_authenticate(user)
        
        Alert.objects.create(
            title='Fire',
            description='Danger',
            severity='HIGH',
            status='ACTIVE',
            created_by=user,
        )

        Alert.objects.create(
            title='Old',
            description='Done',
            severity='LOW',
            status='RESOLVED',
            created_by=user,
        )

        res = self.client.get(ALERTS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['status'], 'ACTIVE')
