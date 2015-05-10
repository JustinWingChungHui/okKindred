from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery, Image, Tag
from family_tree.models import Family, Person
from django.test.utils import override_settings
from django.conf import settings
from django.core import serializers
from django.core.files import File
import os
import shutil
import json

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SSLIFY_DISABLE=True)
class TestImageViews(TestCase):
    '''
    Test class for the gallery views
    '''

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='badger@queenonline.com', password='save the badgers', name='badger', family_id=self.family.id)

        self.gallery = Gallery.objects.create(family_id=self.family.id, title="gallery")

        self.test_image = os.path.join(settings.BASE_DIR, 'gallery/tests/test_image.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.images = []

        for i in range(0,20):
            self.images.append  (
                                Image(
                                    gallery=self.gallery,
                                    family=self.family,
                                    original_image=self.test_image_destination,
                                    thumbnail=self.test_image_destination,
                                    large_thumbnail=self.test_image_destination
                                    )
                                )

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='weebl@queenonline.com', password='mushroom', name='weebl', family_id=self.another_family.id)

    def test_gallery_loads(self):
        '''
        Tests the gallery view loads and uses the correct template
        '''

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery.html')

    def test_gallery_does_not_load_for_another_family(self):
        '''
        Tests gallery does not lad for another family
        '''
        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/gallery={0}/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_first_page_of_images_loaded(self):
        '''
        Tests that the images load for a gallery
        '''
        for i in self.images:
            i.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/image_data=1/'.format(self.gallery.id))

        #Clear up
        for i in self.images:
            i.delete()

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'test_image.jpg' in response.content)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)


    def test_second_page_of_images_loaded(self):
        '''
        Tests that the images load for page 2 of a gallery
        '''
        for i in self.images:
            i.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/image_data=2/'.format(self.gallery.id))

        #Clear up
        for i in self.images:
            i.delete()

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'test_image.jpg' in response.content)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)


    def test_get_hundredth_page_gives_blank_response(self):
        '''
        Tests that requests for 100th page gives blank response
        '''
        for i in self.images:
            i.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/image_data=100/'.format(self.gallery.id))

        #Clear up
        for i in self.images:
            i.delete()

        self.assertEqual(200, response.status_code)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)


    def test_images_cannot_be_seen_by_another_family(self):
        '''
        Tests that the images cannot be loaded by someone form another family
        '''
        another_family = Family.objects.create()
        User.objects.create_user(email='chris_lintott@queenonline.com', password='bang', name='Chris Lintott', family_id=another_family.id)

        self.client.login(email='chris_lintott@queenonline.com', password='bang')
        response = self.client.get('/gallery={0}/image_data=1/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)


    def test_upload_images_view_loads(self):
        '''
        Tests that the upload images view loads
        '''

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/gallery={0}/upload_images/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 200)


    def test_upload_images_view_does_not_load_for_another_family(self):
        '''
        Tests that the upload images view loads
        '''

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/gallery={0}/upload_images/'.format(self.gallery.id))

        self.assertEqual(response.status_code, 404)

    def test_process_image(self):
        '''
        test that we can process an image file without errors
        '''
        from gallery.views.image_views import process_image

        with open(self.test_image, 'rb') as fp:
            result = process_image(self.test_image, File(fp), self.gallery)

        self.assertEqual("test_image", result["name"])
        self.assertEqual(False, 'error' in result)

        filename = settings.MEDIA_ROOT + 'galleries/' + str(self.family.id) + '/' + str(self.gallery.id) + '/' + result['filename']
        os.remove(filename)

    def test_upload_single_photo_via_post(self):
        '''
        test we can upload single photo via post
        '''
        self.client.login(email='badger@queenonline.com', password='save the badgers')
        with open(self.test_image, 'rb') as fp:
            response = self.client.post('/gallery={0}/upload_images_post/'.format(self.gallery.id),{'files': fp})

        self.assertEqual(200, response.status_code)

        #Check file has been uploaded and remove it
        json.loads(response.content.decode('utf-8'))


    def test_upload_single_photo_via_post_for_another_family_fails(self):
        '''
        test we can upload single photo via post
        '''
        self.client.login(email='weebl@queenonline.com', password='mushroom')
        with open(self.test_image, 'rb') as fp:
            response = self.client.post('/gallery={0}/upload_images_post/'.format(self.gallery.id),{'files': fp})

        self.assertEqual(404, response.status_code)


    def test_image_detail_view_loads(self):
        '''
        Test that the image detail view loads
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/image={0}/details/'.format(im.id))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/image_tagging.html')

    def test_image_detail_view_does_not_load_for_another_family(self):
        '''
        Test that the image detail view loads
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/image={0}/details/'.format(im.id))

        self.assertEqual(404, response.status_code)

    def test_image_detail_update(self):
        '''
        Tests that you can update a field on the image using api
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.post('/image={0}/update/'.format(im.id), {'pk': im.id, 'name': 'title', 'value': 'the show must go on'})

        #Reload image
        im = Image.objects.get(id=im.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual('the show must go on', im.title)

    def test_image_detail_update_does_not_update_for_another_family(self):
        '''
        Tests that you can update a field on the image using api
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination,
                    title='innuendo'

                )
        im.save()

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.post('/image={0}/update/'.format(im.id), {'pk': im.id, 'name': 'title', 'value': 'the show must go on'})

        #Reload image
        im = Image.objects.get(id=im.id)

        self.assertEqual(404, response.status_code)

    def test_image_detail_update_does_not_update_for_non_whitelisted_field(self):
        '''
        Tests that you can update a field on the image using api
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination,
                    title='innuendo'

                )
        im.save()

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.post('/image={0}/update/'.format(im.id), {'pk': im.id, 'name': 'id', 'value': 1})

        self.assertEqual(404, response.status_code)

    def test_image_delete(self):
        '''
        Tests that you can delete an image through api
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.post('/image={0}/delete/'.format(im.id))

        self.assertEqual(302, response.status_code)
        self.assertEqual(0, Image.objects.filter(id=im.id).count())

    def test_image_delete_another_family(self):
        '''
        Tests that you can't delete another family's image
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.post('/image={0}/delete/'.format(im.id))

        self.assertEqual(404, response.status_code)


    def test_make_image_gallery_thumbnail(self):
        '''
        Tests that you can assign a thumbnail to a gallery
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.post('/image={0}/make_gallery_thumbnail/'.format(im.id))

        self.assertEqual(302, response.status_code)
        self.assertEqual(im.thumbnail, Gallery.objects.get(id=self.gallery.id).thumbnail)


    def test_make_image_gallery_thumbnail_another_family(self):
        '''
        Tests that you can't assign another family's gallery thumbnail
        '''
        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.post('/image={0}/make_gallery_thumbnail/'.format(im.id))

        self.assertEqual(404, response.status_code)


    def test_person_gallery_view_loads(self):
        '''
        Test that the person gallery view loads
        '''
        p = Person.objects.create(name='badger', family_id=self.family.id)
        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/person={0}/photos/'.format(p.id))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/person_gallery.html')

    def test_person_gallery_view_does_not_load_for_another_family(self):
        '''
        Test that the person gallery view does not load for another family
        '''
        p = Person.objects.create(name='mrs badger', family_id=self.family.id)
        self.client.login(email='weebl@queenonline.com', password='mushroom')
        response = self.client.get('/person={0}/photos/'.format(p.id))

        self.assertEqual(404, response.status_code)

    def test_person_gallery_with_auto_open_image_loads(self):
        '''
        Tests that the person gallery view loads when a photo to open by
        is specified
        '''
        p = Person.objects.create(name='badger', family_id=self.family.id)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        im = Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                )
        im.save()

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/person={0}/photos/image={1}/'.format(p.id, im.id))

        im.delete_image_files()

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'gallery/person_gallery.html')


    def test_person_gallery_with_auto_open_image_does_not_load_for_another_family(self):
        '''
        Tests specified photo does not open if in another family
        '''

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        image = Image(
                    gallery=self.gallery,
                    family=self.another_family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                    )

        p = Person.objects.create(name='badger', family_id=self.family.id)
        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/person={0}/photos/image={1}/'.format(p.id, image.id))

        self.assertEqual(404, response.status_code)

        image.delete_image_files()

    def test_person_gallery_data_loads(self):
        '''
        Tests that the image data for a person gallery loads
        '''
        p = Person.objects.create(name='grandpa badger', family_id=self.family.id)

        for i in self.images:
            i.save()
            Tag.objects.create(image=i, person=p, x1=0.1, x2=0.2, y1=0.2, y2=0.3)

        self.client.login(email='badger@queenonline.com', password='save the badgers')
        response = self.client.get('/person={0}/photos/image_data=1/'.format(p.id))

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'test_image.jpg' in response.content)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)

        #Clear up
        for i in self.images:
            i.delete_image_files()

        #Check cannot be loaded by another family
        self.client.login(email='weebl@queenonline.com', password='mushroom')
        new_response = self.client.get('/person={0}/photos/image_data=1/'.format(p.id))
        self.assertEqual(404, new_response.status_code)

