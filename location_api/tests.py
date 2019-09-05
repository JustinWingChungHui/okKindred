from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from family_tree.models.family import Family
from custom_user.models import User

@override_settings(
    SECURE_SSL_REDIRECT=False,
    AXES_BEHIND_REVERSE_PROXY=False)
class LocationApiTestCase(TestCase):
    '''
    Tests for the Location API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='location@example.com',
                                        password='location',
                                        name='location',
                                        family = self.family)


    def test_get(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/location/?address=warrington,uk'
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'53' in response.content)
        self.assertTrue(b'-2' in response.content)


    def test_get_no_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/location/?address=warrington,uk'
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_no_address(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/location/'
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

