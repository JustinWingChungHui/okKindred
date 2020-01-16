from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient


@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class ChineseRelationNameViewsTestCase(TestCase):

    def test_family_member_names_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/family_member_names/'

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b"po4 po2" in response.content)
