from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
import json

from family_tree.models.family import Family
from family_tree.models.person import Person
from custom_user.models import User
from email_confirmation.models import EmailConfirmation

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class InviteEmailApiTestCase(TestCase):
    '''
    Tests for the Invite Email API
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='matttong@example.com',
                                        password='algiers',
                                        name='Matt Tong',
                                        family = self.family)

        self.person = Person(name='Matt Tong',
                        gender='M',
                        email='matttong@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person.save()

        self.new_person = Person(name='Taka Hirose',
                        gender='M',
                        email='takahirose@example.com',
                        family_id=self.family.id,
                        language='en')

        self.new_person.save()

        self.family2 = Family()
        self.family2.save()

        self.user2 = User.objects.create_user(email='hermanli@example.com',
                                        password='Dragonforce',
                                        name='Herman Li',
                                        family = self.family2)

        self.person2 = Person(name='Herman Li',
                        gender='M',
                        email='hermanli@example.com',
                        family_id=self.family2.id,
                        language='en',
                        user_id=self.user2.id)
        self.person2.save()

        super(InviteEmailApiTestCase, self).setUp()

        self.invite = EmailConfirmation(email_address='matttong@example.com',
                            person_id = self.person.id,
                            user_who_invited_person_id=self.user.id,
                            sent=timezone.now())

        self.invite.save()


    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        invite = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.invite.person_id, invite["person_id"])
        json.loads(response.content)


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/invite_email/{0}/'.format(self.person.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }

        response = client.post(url, data,  format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invite = json.loads(response.content)
        self.assertEqual(self.new_person.id, invite["person_id"])

    def test_create_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }

        response = client.post(url, data,  format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_create_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user2)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }

        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create_invalid_person_id(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': '',
        }

        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_user_already_exists(self):

        self.new_person.user = self.user
        self.new_person.save()

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }
        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)



    def test_create_no_email(self):

        self.new_person.email = ''
        self.new_person.save()

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }
        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)



    def test_create_invite_exists_same_email(self):

        EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }
        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)



    def test_create_invite_exists_different_email(self):

        EmailConfirmation.objects.create(
                        email_address='some_other@email.net',
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/invite_email/'

        data = {
            'person_id': self.new_person.id,
        }
        response = client.post(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invite = json.loads(response.content)
        self.assertEqual(self.new_person.id, invite["person_id"])
        json.loads(response.content)


    def test_confirmation_partial_update(self):

        invite = EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        data = {
            'password': 'bestpasswordever',
        }
        response = client.patch(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.new_person = Person.objects.get(pk=self.new_person.id)

        # Check user assigned
        newUser = User.objects.get(name=self.new_person.name)
        self.assertIsNotNone(newUser)
        json.loads(response.content)



    def test_confirmation_partial_update_block_ip_after_unsuccessful_attempts(self):

        invite = EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.2')
        url = '/api/invite_email_confirmation/{0}/'.format('invalid_key')
        data = {
            'password': 'bestpasswordever',
        }

        for x in range(0, 6):
            response = client.patch(url, data,  format='json')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        # Check ip blocked after multiple failed attempts with correct key
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        response = client.patch(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_confirmation_partial_update_password_too_short(self):

        invite = EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        data = {
            'password': 'short',
        }
        response = client.patch(url, data,  format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)


    def test_confirmation_partial_update_email_address_mismatch(self):

        invite = EmailConfirmation.objects.create(
                        email_address='eh@eh.eh',
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        data = {
            'password': 'bestpasswordever',
        }
        response = client.patch(url, data,  format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)


    def test_confirmation_retrieve(self):
        invite = EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        response = client.get(url,  format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'takahirose@example.com' in response.content)
        self.assertTrue(b'Taka Hirose' in response.content)
        json.loads(response.content)


    def test_confirmation_retrieve_block_ip_after_unsuccessful_attempt(self):
        invite = EmailConfirmation.objects.create(
                        email_address=self.new_person.email,
                        person_id=self.new_person.id,
                        user_who_invited_person=self.user)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.19')
        url = '/api/invite_email_confirmation/{0}/'.format('not_a_proper_key')

        for x in range(0, 6):
            response = client.get(url,  format='json')
            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        # Check ip blocked after multiple failed attempts with correct key
        url = '/api/invite_email_confirmation/{0}/'.format(invite.confirmation_key)
        response = client.get(url,  format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


