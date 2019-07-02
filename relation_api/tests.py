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


    def test_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        response = client.get('/api/relation/', format='json')

        relations = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(relations))
        self.assertNotEqual(self.relation3.id, relations[0]["id"])
        self.assertNotEqual(self.relation3.id, relations[1]["id"])


    def test_retrieve_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation1.id)
        response = client.get(url, format='json')
        relation = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.relation1.id, relation["id"])


    def test_retrieve_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/relation/{0}/'.format(self.relation3.id)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


