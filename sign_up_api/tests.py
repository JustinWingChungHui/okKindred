from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from family_tree.models import Family, Person
from custom_user.models import User
from sign_up.models import SignUp
import json


@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class SignUpApiTestCase(TestCase):
    '''
    Tests for the Sign Up API
    '''

    def test_create_sign_up(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        data = {
            'name': 'name',
            'email': 'email@email.com',
            'gender': 'F',
            'birth_year': 1960,
            'language': 'en',
            'address': 'Coventry, UK',
        }

        url = '/api/sign_up/'
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'name' in response.content)

        new_sign_up = SignUp.objects.get(name='name')
        self.assertNotEqual(None, new_sign_up)
        self.assertEqual('127.0.0.1', new_sign_up.ip_address)
        self.assertEqual(1960, new_sign_up.birth_year)
        self.assertEqual('Coventry, UK', new_sign_up.address)
        json.loads(response.content)

    def test_create_sign_up_blocked_ip(self):
        client = APIClient(HTTP_X_REAL_IP='188.138.188.34')

        data = {
            'name': 'name',
            'email': 'email@email.com',
            'gender': 'F',
            'birth_year': 1960,
            'language': 'en',
            'address': 'Coventry, UK',
        }

        url = '/api/sign_up/'
        response = client.post(url, data, format='json')
        self.assertEqual(404, response.status_code)
        json.loads(response.content)


    def test_create_sign_up_invalid_email(self):
        '''
        Tests the sign up with invalid email returns invalid email error
        '''
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        data = {
            'name': 'name',
            'email': 'obviouslynotanemail',
            'gender': 'F',
            'birth_year': 1960,
            'language': 'en'
        }

        url = '/api/sign_up/'
        response = client.post(url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertTrue(b'Invalid Email' in response.content)
        json.loads(response.content)


    def test_sign_up_post_email_in_use(self):
        '''
        Tests the sign up with invalid email returns invalid email page
        '''
        family = Family.objects.create(description = 'test_sign_up_post_invalid_email')
        Person.objects.create(family = family, name = 'name', gender = 'F', email = 'inuse@email.com')

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        data = {
            'name': 'name',
            'email': 'inuse@email.com',
            'gender': 'F',
            'birth_year': 1960,
            'language': 'en'
        }

        url = '/api/sign_up/'
        response = client.post(url, data, format='json')

        self.assertEqual(400, response.status_code)
        self.assertTrue(b'Email in Use' in response.content)
        json.loads(response.content)


    def test_sign_up_confirmation_creates_user(self):
        '''
        Tests that we create a new user when we enter a password
        '''
        sign_up = SignUp.objects.create(
                    name='joining user',
                    gender = 'M',
                    language = 'en',
                    email_address = 'joininguser@iamanewuser.com')

        url = '/api/sign_up/{0}/'.format(sign_up.confirmation_key)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        data = {
            'password': 'thisisagoodpassword666^!',
        }

        response = client.put(url, data, format='json')

        user = User.objects.get(email='joininguser@iamanewuser.com')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'joininguser@iamanewuser.com' in response.content)
        self.assertNotEqual(None, user)
        json.loads(response.content)


    def test_sign_up_confirmation_invalid_confirmation_key_and_blocks_ip(self):
        '''
        Tests that a 404 is raised for an invalid confirmation key
        '''
        sign_up = SignUp.objects.create(
                            name='joining user',
                            gender = 'M',
                            language = 'en',
                            email_address = 'joininguser@iamanewuser.com')

        url = '/api/sign_up/{0}/'.format('not_proper_key')

        client = APIClient(HTTP_X_REAL_IP='127.0.0.4')
        data = {
            'password': 'thisisagoodpassword666^!',
        }

        for x in range(0, 6):
            response = client.put(url, data, format='json')
            self.assertNotEqual(200, response.status_code)

        # Check ip blocked even with correct key
        url = '/api/sign_up/{0}/'.format(sign_up.confirmation_key)
        response = client.put(url, data, format='json')
        self.assertNotEqual(200, response.status_code)



    def test_sign_up_confirmation_password_too_short(self):
        '''
        Tests that we create a new user when we enter a password
        '''
        sign_up = SignUp.objects.create(
                    name='joining user',
                    gender = 'M',
                    language = 'en',
                    email_address = 'joininguser@iamanewuser.com')

        url = '/api/sign_up/{0}/'.format(sign_up.confirmation_key)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        data = {
            'password': '123456',
        }

        response = client.put(url, data, format='json')

        self.assertEqual(400, response.status_code)
        json.loads(response.content)
