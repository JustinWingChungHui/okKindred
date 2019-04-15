from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient
import json
import time

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class JWTAuthTest(TestCase):
    '''
    Tests JWT auth
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='gracehopper@example.com',
                                        password='compiler',
                                        name='Grace Hopper',
                                        family_id = self.family.id)

        self.person = Person(name='Grace Hopper',
                        gender='F',
                        email='gracehopper@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person.save()

    def test_jwt_auth_and_refresh_token_created_on_correct_auth_details(self):
        client = APIClient()
        auth_details = {
            'email': 'gracehopper@example.com',
            'password': 'compiler'
        }
        response = client.post('/api/auth/obtain_token/', auth_details, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = json.loads(response.content)["access"]
        refresh_token = json.loads(response.content)["refresh"]

        auth_token = {
            'refresh': refresh_token
        }

        # Sleep to ensure new token is different
        time.sleep(1)
        refresh_response = client.post('/api/auth/refresh_token/', auth_token, format='json')
        refresh_token = json.loads(refresh_response.content)["access"]

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(refresh_token, access_token)

        # Check verify token
        new_auth_token ={#
            'token': refresh_token
        }

        verify_new_token_response = client.post('/api/auth/verify_token/', new_auth_token, format='json')
        self.assertEqual(verify_new_token_response.status_code, status.HTTP_200_OK)


    def test_jwt_fails_on_auth_incorrect_password(self):
        client = APIClient()
        payload = {
            'email': 'gracehopper@example.com',
            'password': 'COBOL'
        }
        response = client.post('/api/auth/obtain_token/', payload, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


    def test_verify_fails_on_invalid_token(self):
        client = APIClient()

        invalid_auth_token ={#
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjM1ODU0ODc3LWQyZjQtNDIxZS04ZDI5LWY3YTgxNTk3NzdhYyIsImlhdCI6MTU1NDM4NzU4NCwiZXhwIjoxNTU0MzkxMTg0fQ.yIr0TMbalatx7alU1TMGIxxaelqquMJfz3m4H7AA9v4'
        }
        verify_old_token_response = client.post('/api/auth/verify_token/', invalid_auth_token, format='json')
        self.assertNotEqual(verify_old_token_response.status_code, status.HTTP_200_OK)


    def test_account_locks_out_on_multiple_invalid_login_attempts(self):

        self.user = User.objects.create_user(email='adelegoldberg@example.com',
                                password='smalltalk',
                                name='Adele Goldberg',
                                family_id = self.family.id)

        client = APIClient()

        wrong_auth_details = {
            'email': 'adelegoldberg@example.com',
            'password': 'compiler'
        }

        for x in range(0, 6):
            client.post('/api/auth/obtain_token/', wrong_auth_details, format='json')

        correct_auth_details = {
            'email': 'adelegoldberg@example.com',
            'password': 'smalltalk'
        }

        final_response = client.post('/api/auth/obtain_token/', correct_auth_details, format='json')

        self.assertNotEqual(final_response.status_code, status.HTTP_200_OK)