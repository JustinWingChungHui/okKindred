from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery
from family_tree.models import Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestGalleryViews(TestCase): # pragma: no cover
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

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='mack@queenonline.com', password='theworks', name='mack', family_id=self.another_family.id)


    def test_gallery_index_loads(self):
        '''
        Tests the gallery index view loads and uses the correct template
        '''

        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/gallery_index.html')

    def test_gallery_data_returns_only_data_for_my_family(self):
        '''
        Tests that user only gets the galleries associated with users family
        '''
        self.client.login(email='mack@queenonline.com', password='theworks')
        response = self.client.get('/gallery/gallery_data=1/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(b'[]', response.content)

    def test_gallery_data_returns_first_page(self):
        '''
        Tests that the gallery data returns correct json data
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=1/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'title1' in response.content)
        self.assertEqual(True, b'title12' in response.content)

    def test_gallery_data_returns_nth_page(self):
        '''
        Tests that the gallery data returns correct json data
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=2/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'title13' in response.content)

        self.assertEqual(True, b'title19' in response.content)

    def test_gallery_data_returns_blank_at_end(self):
        '''
        Tests that the gallery data returns a blank data if at end
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery/gallery_data=3/')

        self.assertEqual(200, response.status_code)
        self.assertEqual(b'[]', response.content)

    def test_new_gallery_loads(self):
        '''
        Tests the gallery index view loads and uses the correct template
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/new_gallery/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/edit_gallery.html')


    def test_edit_gallery_loads(self):
        '''
        Tests the edit gallery view loads and uses the correct template
        '''
        gallery = Gallery.objects.get(title="title1")

        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.get('/gallery={0}/edit/'.format(gallery.id))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/edit_gallery.html')


    def test_edit_gallery_does_not_load_for_different_family(self):
        '''
        Tests page does not load for another family
        '''
        gallery = Gallery.objects.get(title="title1")

        self.client.login(email='mack@queenonline.com', password='theworks')
        response = self.client.get('/gallery={0}/edit/'.format(gallery.id))

        self.assertEqual(404, response.status_code)


    def test_edit_gallery_creates_new_gallery(self):
        '''
        test we can create a new gallery
        '''
        self.client.login(email='delilah@queenonline.com', password='meow')

        response = self.client.post('/new_gallery/', {'id': 0, 'title': 'new test gallery', 'description': 'new gallery description'})

        gallery = Gallery.objects.get(title="new test gallery")
        self.assertEqual(True, gallery.id > 0)
        self.assertEqual('new gallery description', gallery.description)
        self.assertEqual(self.family.id, gallery.family_id)

        self.assertEqual(302, response.status_code)


    def test_edit_gallery_edits_existing_gallery(self):
        '''
        test we can edit an existing gallery
        '''
        gallery = Gallery.objects.get(title="title1")

        self.client.login(email='delilah@queenonline.com', password='meow')

        response = self.client.post('/gallery={0}/edit/'.format(gallery.id), {'title': 'new test gallery edit', 'description': 'new gallery description edit'})

        gallery = Gallery.objects.get(id=gallery.id)
        self.assertEqual(True, gallery.id > 0)
        self.assertEqual('new test gallery edit', gallery.title)
        self.assertEqual('new gallery description edit', gallery.description)
        self.assertEqual(self.family.id, gallery.family_id)

        self.assertEqual(302, response.status_code)


    def test_cannot_edit_another_familys_gallery(self):
        '''
        test we can edit an existing gallery
        '''
        gallery = Gallery.objects.get(title="title1")

        self.client.login(email='mack@queenonline.com', password='theworks')

        response = self.client.post('/gallery={0}/edit/'.format(gallery.id), {'id': gallery.id, 'title': 'new test gallery', 'description': 'new gallery description'})

        self.assertEqual(404, response.status_code)


    def test_cannot_delete_gallery_created_by_another_family(self):
        '''
        test that noone can delete a gallery of another family
        '''
        gallery_to_delete = Gallery.objects.create(family_id=self.family.id, title="title")

        self.client.login(email='mack@queenonline.com', password='theworks')
        response = self.client.post('/gallery={0}/delete/'.format(gallery_to_delete.id))

        self.assertEqual(404, response.status_code)

    def test_can_delete_gallery(self):
        '''
        test that noone can delete a gallery of another family
        '''
        gallery_to_delete = Gallery.objects.create(family_id=self.family.id, title="title")

        self.client.login(email='delilah@queenonline.com', password='meow')
        response = self.client.post('/gallery={0}/delete/'.format(gallery_to_delete.id))

        self.assertEqual(302, response.status_code)
        self.assertEqual(0, Gallery.objects.filter(id=gallery_to_delete.id).count())