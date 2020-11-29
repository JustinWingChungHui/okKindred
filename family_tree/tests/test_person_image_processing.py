# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from family_tree.models.person import Person
from family_tree.models.family import Family
from PIL import Image


@override_settings(SSLIFY_DISABLE=True, 
                    AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST, 
                    MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
                    MEDIA_URL=settings.MEDIA_URL_TEST)
class PersonImageProcessingTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for all model logic for a Person
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()



    def test_set_profile_image_crop_rotate_resize(self):
        '''
        Tests that the function correctly sets sets the photo field on a person and converts an image.
        '''
        from django.conf import settings

        path = settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg'

        #Copy test image to media area
        import shutil
        import os
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), path)
        person = Person(name='陳港生', gender='M', family_id=self.family.id)
        person.save()
        person.set_profile_image_crop_rotate_resize(path, 10, 20, 200, 200, 90, test = True)

        #Check small image is valid
        small_image = Image.open(settings.MEDIA_ROOT + str(person.small_thumbnail))
        small_image.verify()
        width, height = small_image.size

        self.assertEqual(80, width)
        self.assertEqual(80, height)


        #Check large image is valid
        large_thumbnail = Image.open(settings.MEDIA_ROOT + str(person.large_thumbnail))
        large_thumbnail.verify()
        width, height = large_thumbnail.size

        self.assertEqual(200, width)
        self.assertEqual(200, height)

        #Clear up mess afterwards
        os.remove(path)
        person.remove_local_images()
        person.remove_remote_images()


    def test_set_profile_image_crop_rotate_resize_replaces_existing(self):
        '''
        Tests that the function correctly sets sets the photo field on a person and converts an image.
        '''
        from django.conf import settings

        path = settings.MEDIA_ROOT + 'profile_photos/large_test_image1.jpg'
        path2 = settings.MEDIA_ROOT + 'profile_photos/large_test_image2.jpg'

        #Copy test image to media area
        import shutil
        import os
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), path)
        person = Person(name='陳港生', gender='M', family_id=self.family.id)
        person.set_profile_image_crop_rotate_resize(path, 10, 20, 200, 200, 90)

        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), path2)
        person = Person(name='陳港生', gender='M', family_id=self.family.id)
        person.set_profile_image_crop_rotate_resize(path2, 10, 20, 200, 200, 90)





