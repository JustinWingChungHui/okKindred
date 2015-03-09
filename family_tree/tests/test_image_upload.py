from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings
from django.conf import settings
import json
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SSLIFY_DISABLE=True)
class TestImageUploadViews(TestCase):

    def setUp(self):
        '''
        Set up a family, user and profile to test with
        '''

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='fairy_fellar@email.com', password='masterstroke', name='Fairy Fellar')
        self.user.save()

        self.person = Person.objects.create(name='Fairy Fellar', gender='M', user_id=self.user.id, email='fairy_fellar@email.com', family_id=self.family.id)
        self.person.save()

        self.another_family = Family()
        self.another_family.save()
        self.another_user = User.objects.create_user(email='dale_arden@email.com', password="flash i love you", name='Dale Arden', family_id=self.another_family.id)
        self.another_user.save()

    def test_upload_image_view_loads(self):
        '''
        tests that the view loads if someone navigates to it
        '''
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')
        response = self.client.get('/edit_profile_photo={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/image_upload.html')



    def test_image_upload_view_does_not_load_for_another_family(self):
        '''
        tests that the view does not load if a person from a different family is trying to access it
        '''
        self.client.login(email='dale_arden@email.com', password='flash i love you')
        response = self.client.get('/edit_profile_photo={0}/'.format(self.person.id))
        self.assertEqual(404, response.status_code)


    def test_image_upload_receives_file(self):
        '''
        test that we can upload a file
        '''
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')


        with open(os.path.join(BASE_DIR, 'tests/test_image_upload.png'), 'rb') as fp:
            response = self.client.post('/image_upload={0}/'.format(self.person.id),{'picture': fp})

        self.assertEqual(200, response.status_code)

        #Check file has been uploaded and remove it
        data = json.loads(response.content.decode('utf-8'))
        filename = settings.MEDIA_ROOT + 'profile_photos/' + data['filename']
        os.remove(filename)

        #Reload object
        self.person = Person.objects.get(pk=self.person.id)
        self.assertEqual('profile_photos/' + data['filename'],self.person.photo)


    def test_image_upload_cannot_receive_file_from_another_family(self):
        '''
        test that we can can't upload file to another family
        '''
        self.client.login(email='dale_arden@email.com', password='flash i love you')

        with open(os.path.join(BASE_DIR, 'tests/test_image_upload.png'), 'rb') as fp:
            response = self.client.post('/image_upload={0}/'.format(self.person.id),{'picture': fp})

        self.assertEqual(404, response.status_code)


    def test_image_upload_does_not_process_image_file(self):
        '''
        test that an invalid file is not processed
        '''
        num_files = len([item for item in os.listdir( settings.MEDIA_ROOT + 'profile_photos/')])

        self.client.login(email='fairy_fellar@email.com', password='masterstroke')
        with open(os.path.join(BASE_DIR, 'tests/test_not_a_real_picture.png'), 'rb') as fp:
            response = self.client.post('/image_upload={0}/'.format(self.person.id),{'picture': fp})

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual('Invalid image!', data['error'])

        #Check no new files
        self.assertEqual(num_files, len([item for item in os.listdir( settings.MEDIA_ROOT + 'profile_photos/')]))


    def test_image_resize_view_loads(self):
        '''
        test that we can upload a file
        '''
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')

        response = self.client.get('/image_resize={0}/'.format(self.person.id))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/image_resize.html')


    def test_image_resize_view_does_not_load_for_another_family(self):
        '''
        tests that the view does not load if a person from a different family is trying to access it
        '''
        self.client.login(email='dale_arden@email.com', password='flash i love you')
        response = self.client.get('/image_resize={0}/'.format(self.person.id))
        self.assertEqual(404, response.status_code)


    def test_image_crop_can_be_posted_to(self):
        '''
        Tests that the image_crop view can posted to
        '''

        #Copy test image to media area
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        self.person.photo = 'profile_photos/large_test_image.jpg'
        self.person.save()
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')

        response = self.client.post('/image_crop={0}/'.format(self.person.id),{'x': 100, 'y': 200, 'w': 300, 'h': 300, 'display_height' : 550})

        #Clear up mess afterwards
        os.remove(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        self.assertEqual(302, response.status_code)

    def test_image_crop_cannot_be_posted_to_for_another_family(self):
        '''
        tests that the view does not load if a person from a different family is trying to access it
        '''
        #Copy test image to media area
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        self.person.photo = 'profile_photos/large_test_image.jpg'
        self.person.save()

        self.client.login(email='dale_arden@email.com', password='flash i love you')
        response = self.client.post('/image_crop={0}/'.format(self.person.id),{'x': 100, 'y': 200, 'w': 300, 'h': 300, 'display_height' : 550})

        #Clear up mess afterwards
        os.remove(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        self.assertEqual(404, response.status_code)
