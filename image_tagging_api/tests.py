from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APIClient

from custom_user.models import User
from gallery.models import Gallery, Image, Tag
from family_tree.models import Family, Person

import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SECURE_SSL_REDIRECT=False,
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    MEDIA_URL=settings.MEDIA_URL_TEST,
                    AXES_BEHIND_REVERSE_PROXY=False,
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST)
class TestTagViews(TestCase): # pragma: no cover
    '''
    Test class for the gallery views
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='white_queen@queenonline.com', password='AsItBegan', name='White Queen', family_id=self.family.id)
        self.person = Person.objects.create(name='White Queen', family=self.family)
        self.person2 = Person.objects.create(name='Black Queen', family=self.family)
        self.person3 = Person.objects.create(name='As It Began', family=self.family)

        self.gallery = Gallery.objects.create(family_id=self.family.id, title="gallery")

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.image =Image(
                            gallery=self.gallery,
                            family=self.family,
                            original_image=self.test_image_destination,
                            thumbnail=self.test_image_destination,
                            large_thumbnail=self.test_image_destination
                            )
        self.image.save()

        self.tag1 = Tag.objects.create(image=self.image, person=self.person, x1=1, x2=2, y1=3, y2=4)
        self.tag2 = Tag.objects.create(image=self.image, person=self.person2, x1=5, x2=6, y1=7, y2=8)

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='queen_of_hearts@queenonline.com',
                                password='Off With Their Heads', name='Queen Of Hearts', family_id=self.another_family.id)
        self.other_family_person = Person.objects.create(name='Queen Adreena', family=self.another_family)

        self.other_family_gallery = Gallery.objects.create(family_id=self.another_family.id, title="gallery")
        self.other_family_image =Image(
                            gallery=self.other_family_gallery,
                            family=self.another_family,
                            original_image=self.test_image_destination,
                            thumbnail=self.test_image_destination,
                            large_thumbnail=self.test_image_destination
                            )
        self.other_family_image.save()



    def tearDown(self):
        try:
            self.image.delete_local_image_files()
            self.image.delete_remote_image_files()
        except:
            pass

        try:
            os.remove(self.test_image_destination)
        except:
            pass


    def test_list(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        url = '/api/image_tagging/?image_id={0}'.format(self.image.id)

        response = client.get(url, format='json')

        # Check it contains both tags
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'"person_id":1' in response.content)
        self.assertTrue(b'"person_id":2' in response.content)
        json.loads(response.content)


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/image_tagging/?image_id={0}'.format(self.image.id)
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_list_other_family(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.another_user)
        url = '/api/image_tagging/?image_id={0}'.format(self.image.id)

        response = client.get(url, format='json')

        self.assertFalse(b'"person_id":1' in response.content)
        self.assertFalse(b'"person_id":2' in response.content)
        json.loads(response.content)


    def test_list_filter_by_person(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        url = '/api/image_tagging/?image_id={0}&person_id={1}'.format(self.image.id, self.person.id)

        response = client.get(url, format='json')

        # Check it contains both tags
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'"person_id":1' in response.content)
        self.assertFalse(b'"person_id":2' in response.content)
        json.loads(response.content)


    def test_destroy(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        url = '/api/image_tagging/{0}/'.format(self.tag1.id)

        response = client.delete(url, format='json')

        # Check its deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tags = Tag.objects.filter(id=self.tag1.id)
        self.assertEqual(0, tags.count())
        json.loads(response.content)



    def test_destroy_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/image_tagging/{0}/'.format(self.tag1)
        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_destroy_other_family(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.another_user)
        url = '/api/image_tagging/{0}/'.format(self.tag1.id)

        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'person_id': self.person3.id,
            'image_id': self.image.id,
            'x1': 0.1,
            'x2': 0.2,
            'y1': 0.3,
            'y2': 0.4,
        }

        url = '/api/image_tagging/'
        response = client.post(url, data, format='json')

        new_tag = Tag.objects.get(person_id=self.person3.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0.1, new_tag.x1)
        json.loads(response.content)


    def test_create_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        data = {
            'person_id': self.person3.id,
            'image_id': self.image.id,
            'x1': 0.1,
            'x2': 0.2,
            'y1': 0.3,
            'y2': 0.4,
        }

        url = '/api/image_tagging/'
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_create_person_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'person_id': self.other_family_person.id,
            'image_id': self.image.id,
            'x1': 0.1,
            'x2': 0.2,
            'y1': 0.3,
            'y2': 0.4,
        }

        url = '/api/image_tagging/'
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_create_image_other_family(self):

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'person_id': self.person3.id,
            'image_id': self.other_family_image.id,
            'x1': 0.1,
            'x2': 0.2,
            'y1': 0.3,
            'y2': 0.4,
        }

        url = '/api/image_tagging/'
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)



    def test_create_invalid_x1(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)

        data = {
            'person_id': self.person3.id,
            'image_id': self.image.id,
            'x1': 'invalid!',
            'x2': 0.2,
            'y1': 0.3,
            'y2': 0.4,
        }

        url = '/api/image_tagging/'
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        json.loads(response.content)

