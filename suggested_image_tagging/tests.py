from django.conf import settings
from django.test.utils import override_settings
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from custom_user.models import User
from gallery.models import Image, Gallery
from family_tree.models import Family, Person
from suggested_image_tagging.models import SuggestedTag

import json
import os
import shutil
import threading

@override_settings(SECURE_SSL_REDIRECT=False,
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    MEDIA_URL=settings.MEDIA_URL_TEST,
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST)
class SuggestedTagTestCase(TestCase): # pragma: no cover
    '''
    Tests for the image class
    '''

    def setUp(self):
        '''
        Need to create a family and a gallery and image
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='white_queen@queenonline.com', password='AsItBegan', name='White Queen', family_id=self.family.id)

        self.person = Person(name='Wallace', gender='M', email='wallace@creaturecomforts.com', family_id=self.family.id, language='en')
        self.person.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        self.image.save()

        self.image2 = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        self.image2.save()

        self.another_family = Family()
        self.another_family.save()
        self.another_user = User.objects.create_user(email='queen_of_hearts@queenonline.com',
                                password='Off With Their Heads', name='Queen Of Hearts', family_id=self.another_family.id)

        self.suggested_tag = SuggestedTag.objects.create(image_id=self.image.id, x1=0.1001, y1=0.2, x2=0.3, y2=0.4)


    def tearDown(self):
        self.image.delete_local_image_files()
        threading.Thread(target=self.image.delete_remote_image_files).start()

        self.image2.delete_local_image_files()
        threading.Thread(target=self.image2.delete_remote_image_files).start()

        try:
            os.remove(self.test_image_destination)
        except:
            pass


    def test_convert_to_tag(self):
        '''
        Tests that we can rotate a tag correctly
        '''
        new_tag = self.suggested_tag.convertToTag(person_id = self.person.id)

        self.assertTrue(new_tag.id > 0)
        self.assertEqual(self.person.id, new_tag.person_id)
        self.assertEqual(0.1001, new_tag.x1)


    def test_list_suggested_tags(self):

        SuggestedTag.objects.create(image_id=self.image2.id, x1=0.1123, y1=0.2, x2=0.3, y2=0.4)

        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')

        client.force_authenticate(user=self.user)
        url = '/api/suggested_image_tagging/?image_id={0}'.format(self.image.id)

        response = client.get(url, format='json')

        # Check it contains both tags
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'0.1001' in response.content)
        self.assertFalse(b'0.1123' in response.content)

        json.loads(response.content)


    def test_list_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/suggested_image_tagging/?image_id={0}'.format(self.image.id)
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_list_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.another_user)
        url = '/api/suggested_image_tagging/?image_id={0}'.format(self.image.id)
        response = client.get(url, format='json')

        self.assertFalse(b'0.1001' in response.content)


    def test_destroy(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag.id)

        response = client.delete(url, format='json')

        # Check its deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tags = SuggestedTag.objects.filter(id=self.suggested_tag.id)
        self.assertEqual(0, tags.count())
        json.loads(response.content)


    def test_destroy_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag)
        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_destroy_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.another_user)
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag.id)

        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)


    def test_partial_update(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.user)
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag.id)
        data = {
            'person_id': self.person.id
        }

        response = client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'0.1001' in response.content)

        # Check suggested tag is deleted
        tags = SuggestedTag.objects.filter(id=self.suggested_tag.id)
        self.assertEqual(0, tags.count())
        json.loads(response.content)


    def test_partial_update_requires_authentication(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag.id)
        data = {
            'person_id': self.person.id
        }

        response = client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json.loads(response.content)


    def test_partial_update_other_family(self):
        client = APIClient(HTTP_X_REAL_IP='127.0.0.1')
        client.force_authenticate(user=self.another_user)
        url = '/api/suggested_image_tagging/{0}/'.format(self.suggested_tag.id)
        data = {
            'person_id': self.person.id
        }

        response = client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        json.loads(response.content)