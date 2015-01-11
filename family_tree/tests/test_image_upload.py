from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings

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
        self.client.login(email='jfairy_fellar@email.com', password='masterstroke')
        response = self.client.get('/upload_profile_photo={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/image_upload.html')