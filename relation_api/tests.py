from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient
import json

from custom_user.models import User
from family_tree.models.family import Family
from family_tree.models.person import Person
from family_tree.models.relation import Relation, RAISED, PARTNERED

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class RelationApiTestCase(TestCase):
    '''
    Tests for the relation API
    '''

    def setUp(self):
        self.family = Family()
        self.family.save()

        self.family2 = Family()
        self.family2.save()

        self.user = User.objects.create_user(email='edithclarke@example.com',
                                        password='electricalengineering',
                                        name='Edith Clarke',
                                        family = self.family)

        self.person1 = Person(name='Edith Clarke',
                        gender='F',
                        email='edithclarke@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person1.save()


        self.person2 = Person(name='someone else',
                        gender='O',
                        email='anon@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person2.save()


        self.person3 = Person(name='another person',
                        gender='O',
                        email='anon2@example.com',
                        family_id=self.family.id,
                        language='en',
                        user_id=self.user.id)
        self.person3.save()

        self.relation1 = Relation.objects.create(from_person=self.person1, to_person=self.person2, relation_type=PARTNERED)
        self.relation1.save()

        self.relation2 = Relation.objects.create(from_person=self.person1, to_person=self.person3, relation_type=RAISED)
        self.relation2.save()

        self.otherFamilyUser = User.objects.create_user(email='anotherfamilyuser@example.com',
                                        password='anotherfamily',
                                        name='Another Family',
                                        family = self.family2)

        self.otherFamilyPerson = Person(name='another family',
                        gender='O',
                        email='anotherfamily@example.com',
                        family_id=self.family2.id,
                        language='en',
                        user_id=self.user.id)
        self.otherFamilyPerson.save()


        self.otherFamilyPerson2 = Person(name='another family 2',
                    gender='O',
                    email='anotherfamily2@example.com',
                    family_id=self.family2.id,
                    language='en',
                    user_id=self.user.id)
        self.otherFamilyPerson2.save()

        self.relation3 = Relation.objects.create(from_person=self.otherFamilyPerson, to_person=self.otherFamilyPerson2, relation_type=PARTNERED)
        self.relation3.save()

        super(RelationApiTestCase, self).setUp()


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        response = client.get('/api/relation/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        response = client.get('/api/relation/', format='json')

        relations = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(relations))
        self.assertNotEqual(self.relation3.id, relations[0]["id"])
        self.assertNotEqual(self.relation3.id, relations[1]["id"])
        json.loads(response.content)


    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.get(url, format='json')
        relation = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.relation1.id, relation["id"])
        json.loads(response.content)


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation3.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_delete_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_delete_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation3.id)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_delete(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        count = Relation.objects.filter(pk = self.relation1.id).count()
        self.assertEqual(0, count)
        json.loads(response.content)


    def test_create(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/'
        data = {
            'from_person_id': self.person2.id,
            'to_person_id': self.person3.id,
            'relation_type': RAISED
        }

        response = client.post(url, data, format='json')
        relation = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(relation, None)
        json.loads(response.content)


    def test_create_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/relation/'
        data = {
            'from_person_id': self.person2.id,
            'to_person_id': self.person3.id,
            'relation_type': RAISED
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_create_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.otherFamilyUser)
        url = '/api/relation/'
        data = {
            'from_person_id': self.person2.id,
            'to_person_id': self.person3.id,
            'relation_type': RAISED
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create_invalid_parameter(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/'
        data = {
            'from_person_id': 'invalid parameter',
            'to_person_id': self.person3.id,
            'relation_type': RAISED
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)


    def test_create_invalid_relation_type(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/'
        data = {
            'from_person_id': 'invalid parameter',
            'to_person_id': self.person3.id,
            'relation_type': 50000
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)

    def test_create_related_to_self(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/'
        data = {
            'from_person_id': self.person3.id,
            'to_person_id': self.person3.id,
            'relation_type': RAISED
        }

        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)
