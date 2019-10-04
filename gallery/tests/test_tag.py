from django.test import TestCase
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from django.conf import settings
from django.test.utils import override_settings
import os
import shutil

@override_settings(SECURE_SSL_REDIRECT=False,
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST)
class TagTestCase(TestCase): # pragma: no cover
    '''
    Tests for the image class
    '''

    def setUp(self):
        '''
        Need to create a family and a gallery and image
        '''
        self.family = Family()
        self.family.save()

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


    def test_rotate_tag(self):
        '''
        Tests that we can rotate a tag correctly
        '''
        tag = Tag.objects.create(image_id=self.image.id, x1=0.1, y1=0.2, x2=0.3, y2=0.4, person_id=self.person.id)
        tag.rotate(90)

        self.assertTrue(abs(0.2 - tag.x1) < 0.0001)
        self.assertTrue(abs(0.7 - tag.y1) < 0.0001)
        self.assertTrue(abs(0.4 - tag.x2) < 0.0001)
        self.assertTrue(abs(0.9 - tag.y2) < 0.0001)

        #Clear up
        self.image.delete_local_image_files()
        self.image.delete_remote_image_files()






