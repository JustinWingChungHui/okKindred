from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from custom_user.models import User
from family_tree.models import Family, Person

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class UserApiTestCase(TestCase):
    '''
    Tests for the user API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='user@example.com',
                                        password='user',
                                        name='user',
                                        family = self.family)

        self.user2 = User.objects.create_user(email='user2@example.com',
                                        password='user2',
                                        name='user2',
                                        family = self.family)

        self.family2 = Family()
        self.family2.save()

        self.user3 = User.objects.create_user(email='user3@example.com',
                                        password='user3',
                                        name='user3',
                                        family = self.family2)

        super(UserApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/users/'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/users/'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'user@example.com' in response.content)
        self.assertTrue(b'user2@example.com' in response.content)
        self.assertFalse(b'user3@example.com' in response.content)


    def test_get_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/user_settings/'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/user_settings/'
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'receive_update_emails' in response.content)


    def test_update(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'language': 'fi',
            'receive_update_emails': True,
            'receive_photo_update_emails': True,
        }

        url = '/api/user_settings/'
        response = client.patch(url, data, format='json')

        self.user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'fi' in response.content)
        self.assertTrue(self.user.receive_update_emails)


    def test_cannot_update_other_user_values(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'language': 'fi',
            'receive_update_emails': True,
            'receive_photo_update_emails': True,
            'is_superuser': True,
        }

        url = '/api/user_settings/'
        response = client.patch(url, data, format='json')

        self.user = User.objects.get(id=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.is_superuser)


    def test_change_password_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/password_change/'
        data= {
            'old_password': 'user1',
            'new_password': 'user1a'
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_change_password_success(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/password_change/'
        data= {
            'old_password': 'user',
            'new_password': 'user12345'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(id=self.user.id)
        result = user.check_password('user12345')
        self.assertTrue(result)


    def test_change_password_missing_parameters(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/password_change/'
        data= {}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_password_invalid_old_password(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/password_change/'
        data= {
            'old_password': 'not valid',
            'new_password': 'user12345'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_change_password_too_short(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/password_change/'
        data= {
            'old_password': 'user',
            'new_password': 'u'
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_account_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/delete_account/'
        response = client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_account_no_password(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/delete_account/'
        data= {
            'password': '',
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_account_last_user(self):

        person3 = Person.objects.create(
                name='User3',
                gender='M',
                email='user3@example.com',
                family_id=self.family2.id,
                language='en',
                user_id=self.user3.id)


        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user3)
        url = '/api/delete_account/'
        data= {
            'password': 'user3',
        }
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Person.objects.filter(id=person3.id).count())
        self.assertEqual(0, User.objects.filter(id=self.user3.id).count())


    def test_delete_account_multi_user_leave_profile(self):

        person = Person.objects.create(
                name='User',
                gender='M',
                email='user@example.com',
                family_id=self.family.id,
                language='en',
                user_id=self.user.id)


        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/delete_account/'
        data= {
            'password': 'user',
            'delete_profile': False
        }

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Person.objects.filter(id=person.id).count())
        self.assertEqual(0, User.objects.filter(id=self.user.id).count())


    def test_delete_account_multi_user_delete_profile(self):

        person = Person.objects.create(
                name='User',
                gender='M',
                email='user@example.com',
                family_id=self.family.id,
                language='en',
                user_id=self.user.id)


        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/delete_account/'
        data= {
            'password': 'user',
            'delete_profile': True
        }

        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Person.objects.filter(id=person.id).count())
        self.assertEqual(0, User.objects.filter(id=self.user.id).count())
