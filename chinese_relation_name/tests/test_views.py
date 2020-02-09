from django.test import TestCase
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from custom_user.models import User
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, PARTNERED, RAISED_BY

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class ChineseRelationNameViewsTestCase(TestCase):

    def test_family_member_names_list(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/family_member_names/'

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b"po4 po2" in response.content)

    def test_family_member_names_single(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/family_member_names/?name=Mother'

        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b"maa4 maa1" in response.content)
        self.assertFalse(b"po4 po2" in response.content)


    def test_get_relation_name_not_authenticated(self):
        family = Family()
        family.save()

        User.objects.create_user(email='margaret_knight@example.com',
                                        password='inventor',
                                        name='Margaret Knight',
                                        family = family)

        person = Person.objects.create(name='patient zero', gender='M', family_id=family.id)

        wife = Person.objects.create(name='wife', gender='F', family_id=family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/relation_name/{0}/{1}/'.format(person.id, wife.id)
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_relation_name_not_available_to_another_family(self):
        family = Family()
        family.save()

        family2 = Family()
        family2.save()

        user = User.objects.create_user(email='margaret_knight@example.com',
                                        password='inventor',
                                        name='Margaret Knight',
                                        family = family2)

        person = Person.objects.create(name='patient zero', gender='M', family_id=family.id)

        wife = Person.objects.create(name='wife', gender='F', family_id=family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=user)
        url = '/api/relation_name/{0}/{1}/'.format(person.id, wife.id)
        response = client.get(url, format='json')

        self.assertFalse(b"Wife" in response.content)


    def test_get_relation_name(self):
        family = Family()
        family.save()

        user = User.objects.create_user(email='margaret_knight@example.com',
                                        password='inventor',
                                        name='Margaret Knight',
                                        family = family)

        person = Person.objects.create(name='patient zero', gender='M', family_id=family.id)

        wife = Person.objects.create(name='wife', gender='F', family_id=family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M', family_id=family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)


        daughter = Person.objects.create(name='daughter', gender='F', family_id=family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum', gender='F', family_id=family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)


        dad = Person.objects.create(name='dad', gender='M', family_id=family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma', gender='F', family_id=family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        grandson = Person.objects.create(name='grandson', gender='M', family_id=family.id)
        Relation.objects.create(from_person=son, to_person=grandson, relation_type=RAISED)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=user)
        url = '/api/relation_name/{0}/{1}/'.format(person.id, grandson.id)
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b"syun1" in response.content)

