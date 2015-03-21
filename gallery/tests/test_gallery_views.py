from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery
from family_tree.models import Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestGalleryViews(TestCase):
    '''
    Test class for the gallery views
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='delilah@queenonline.com', password='meow', name='Delilah', family_id=self.family.id)

        #Create a load of galleries
        for i in range(1,20):
            Gallery.objects.create(family_id=self.family.id, title="title" + str(i))


    def test_gallery_index_loads(self):
        '''
        Tests the gallery index view loads and uses the correct template
        '''

        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery_index.html')

    def test_gallery_data_returns_only_data_for_my_family(self):
        '''
        Tests that user only gets the galleries associated with users family
        '''
        another_family = Family.objects.create()
        User.objects.create_user(email='mack@queenonline.com', password='theworks', name='mack', family_id=another_family.id)

        self.client.login(email='mack@queenonline.com', password='theworks')
        response = self.client.get('/gallery/gallery_data=1/')
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'[]', response.content)

    def test_gallery_data_returns_first_page(self):
        '''
        Tests that the gallery data returns correct json data
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, b'title1' in response.content)
        self.assertEqual(True, b'title12' in response.content)

    def test_gallery_data_returns_nth_page(self):
        '''
        Tests that the gallery data returns correct json data
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=2/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, b'title13' in response.content)
        print(response.content)
        self.assertEqual(True, b'title19' in response.content)

    def test_gallery_data_returns_blank_at_end(self):
        '''
        Tests that the gallery data returns a blank data if at end
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=3/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.content))