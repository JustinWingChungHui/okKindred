from django.test import TestCase
from custom_user.models import User
from gallery.models import Gallery, Image, Tag
from family_tree.models import Family, Person
from django.test.utils import override_settings
from django.conf import settings
from django.core import serializers
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@override_settings(SSLIFY_DISABLE=True)
class TestImageViews(TestCase): # pragma: no cover
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

        self.another_family = Family.objects.create()
        self.another_user = User.objects.create_user(email='queen_of_hearts@queenonline.com',
                                password='Off With Their Heads', name='Queen Of Hearts', family_id=self.another_family.id)



    def test_get_tags_on_an_image(self):
        '''
        Tests that the images load for a gallery
        '''
        Tag.objects.create(image=self.image, person=self.person, x1=1, x2=2, y1=3, y2=4)
        Tag.objects.create(image=self.image, person=self.person2, x1=5, x2=6, y1=7, y2=8)

        self.client.login(email='white_queen@queenonline.com', password='AsItBegan')
        response = self.client.get('/image={0}/tags/get/'.format(self.image.id))


        self.assertEqual(200, response.status_code)

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)

        self.assertEqual(True, b'3' in response.content)
        self.assertEqual(True, b'8' in response.content)
        self.assertEqual(True, b'White Queen' in response.content)
        self.assertEqual(True, b'Black Queen' in response.content)


    def test_get_tags_different_family(self):
        '''
        Checks that another family cannot get the tags for a family
        '''
        Tag.objects.create(image=self.image, person=self.person2, x1=5, x2=6, y1=7, y2=8)

        self.client.login(email='queen_of_hearts@queenonline.com', password='Off With Their Heads')
        response = self.client.get('/image={0}/tags/get/'.format(self.image.id))

        self.assertEqual(404, response.status_code)


    def test_delete_tag(self):
        '''
        Tests tag deletion api
        '''
        image =Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                    )
        image.save()
        tag = Tag.objects.create(image=image, person=self.person, x1=1, x2=2, y1=3, y2=4)


        self.client.login(email='white_queen@queenonline.com', password='AsItBegan')
        response = self.client.post('/tag={0}/delete/'.format(tag.id))


        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Tag.objects.filter(id=tag.id).count())


    def test_delete_tag_fails_for_different_family(self):
        '''
        Tests tag deletion api
        '''
        image =Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                    )
        image.save()
        tag = Tag.objects.create(image=image, person=self.person, x1=1, x2=2, y1=3, y2=4)


        self.client.login(email='queen_of_hearts@queenonline.com', password='Off With Their Heads')
        response = self.client.post('/tag={0}/delete/'.format(tag.id))

        self.assertEqual(404, response.status_code)

    def test_create_tag(self):
        '''
        Tests create tag api
        '''
        image =Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                    )
        image.save()

        self.client.login(email='white_queen@queenonline.com', password='AsItBegan')
        response = self.client.post('/image={0}/tags/create/'.format(self.image.id)
        ,   {
                'person': self.person.id,
                'x1': 0.314159,
                'y1': 0.1,
                'x2': 0.6,
                'y2': 0.2,
            })

        self.assertEqual(200, response.status_code)
        tag = Tag.objects.get(x1=0.314159)
        self.assertEqual(self.person.id, tag.person_id)
        self.assertEqual(0.2, tag.y2)

    def test_create_tag_fails_for_another_family(self):
        '''
        Tests create tag api fails if in wrong family
        '''
        image =Image(
                    gallery=self.gallery,
                    family=self.family,
                    original_image=self.test_image_destination,
                    thumbnail=self.test_image_destination,
                    large_thumbnail=self.test_image_destination
                    )
        image.save()

        self.client.login(email='queen_of_hearts@queenonline.com', password='Off With Their Heads')
        response = self.client.post('/image={0}/tags/create/'.format(self.image.id),
           {
                'person': self.person.id,
                'x1': 0.314159,
                'y1': 0.1,
                'x2': 0.6,
                'y2': 0.2,
            })

        self.assertEqual(404, response.status_code)
