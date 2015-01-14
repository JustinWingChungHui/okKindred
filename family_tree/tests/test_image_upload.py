from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings
from django.conf import settings
import os
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


    def test_upload_image_view_loads(self):
        '''
        tests that the view loads if someone navigates to it
        '''
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')
        response = self.client.get('/edit_profile_photo={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/image_upload.html')

    def test_image_upload_receives_file(self):
        '''
        test that we can upload a file
        '''
        self.client.login(email='fairy_fellar@email.com', password='masterstroke')


        with open(os.path.join(BASE_DIR, 'tests/test_image_upload.png'), 'rb') as fp:
            response = self.client.post('/image_upload={0}/'.format(self.person.id),{'picture': fp})

        self.assertEqual(200, response.status_code)

        #Check file has been uploaded and remove it
        import json
        data = json.loads(response.content.decode('utf-8'))
        filename = settings.MEDIA_ROOT + 'profile_photos/' + data['filename']
        os.remove(filename)

        #Reload object
        self.person = Person.objects.get(pk=self.person.id)
        self.assertEqual('profile_photos/' + data['filename'],self.person.photo)



    def test_image_upload_does_not_process_image_file(self):
        '''
        test that an invalid file is not processed
        '''
        num_files = len([item for item in os.listdir( settings.MEDIA_ROOT + 'profile_photos/')])

        self.client.login(email='fairy_fellar@email.com', password='masterstroke')
        with open(os.path.join(BASE_DIR, 'tests/test_not_a_real_picture.png'), 'rb') as fp:
            response = self.client.post('/image_upload={0}/'.format(self.person.id),{'picture': fp})

        self.assertEqual(200, response.status_code)
        import json
        data = json.loads(response.content.decode('utf-8'))

        self.assertEqual('Invalid image!', data['error'])

        #Check no new files
        self.assertEqual(num_files, len([item for item in os.listdir( settings.MEDIA_ROOT + 'profile_photos/')]))
