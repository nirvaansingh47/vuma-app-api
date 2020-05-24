from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import VumaRequest

from vuma.serializers import VumaRequestSerializer


# REQUESTS_URL = reverse('vuma:request-list')
REQUESTS_URL = '/api/vuma/requests/'


class PublicRequestsApiTests(TestCase):
    """Test the publicly available requests API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving requests"""
        res = self.client.get(REQUESTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRequestsApiTests(TestCase):
    """Test the authorized user requests API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@mail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_requests(self):
        """Test retrieving requests"""
        VumaRequest.objects.create(
            user=self.user,
            name='Get order',
            url='https://www.google.com',
            method='GET'
        )
        VumaRequest.objects.create(
            user=self.user,
            name='Get service',
            url='https://www.google.com',
            method='GET'
        )

        res = self.client.get(REQUESTS_URL)

        requests = VumaRequest.objects.all().order_by('-name')
        serializer = VumaRequestSerializer(requests, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_requests_limited_to_user(self):
        """Test that requests returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@mail.com',
            'testpass'
        )
        VumaRequest.objects.create(
            user=user2,
            name='Get order',
            url='https://www.google.com',
            method='GET'
        )
        vuma_request = VumaRequest.objects.create(
            user=self.user,
            name='Get service',
            url='https://www.google.com',
            method='GET'
            )

        res = self.client.get(REQUESTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], vuma_request.name)

    def test_create_request_successful(self):
        """Test creating a new request"""
        payload = {'name': 'Test request'}
        self.client.post(REQUESTS_URL, payload)

        exists = VumaRequest.objects.filter(
            user=self.user,
            name=payload['name']
            ).exists()

        self.assertTrue(exists)
