from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from message_queue.models import Queue, Message

from facial_recognition.resize_tags import resize_tags

import os
import shutil

@override_settings(SSLIFY_DISABLE=True,
            MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
            MEDIA_URL=settings.MEDIA_URL_TEST,
            AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST,
            FACE_RECOG_TRAIN_TEMP_DIR = settings.FACE_RECOG_TRAIN_TEST_DIR)
class ResizeTagsTestCase(TestCase): # pragma: no cover

    def setUp(self):
        '''
        Need to create a family and a gallery
        '''
        self.family = Family()
        self.family.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        self.test_image = os.path.join(settings.BASE_DIR, 'facial_recognition/tests/test_image_woman.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])
        self.test_image_s3_key = ''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.image = Image(gallery=self.gallery, family=self.family, original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        self.image.save()
        self.image.upload_files_to_s3()

        self.person = Person(name='Wallace', gender='M', email='wallace@creaturecomforts.com', family_id=self.family.id, language='en')
        self.person.save()

        self.tag = Tag.objects.create(image_id=self.image.id, x1=0.3, y1=0.2, x2=0.5, y2=0.4, person_id=self.person.id)


    def tearDown(self):
        self.image.delete_local_image_files()
        self.image.delete_remote_image_files()

        try:
            os.remove(self.test_image_destination)
        except:
            pass




    def test_tag_resizes(self):

        # Create a message to resize tag
        resize_tag_queue_id = Queue.objects.get(name='resize_tag').id
        message = Message.objects.create(queue_id=resize_tag_queue_id, integer_data = self.tag.id)

        resize_tags([message])

        resized_tag = Tag.objects.get(pk=self.tag.id)

        self.assertTrue(abs(0.2875 - resized_tag.x1) < 0.001)
        self.assertTrue(abs(0.1951 - resized_tag.y1) < 0.001)
        self.assertTrue(abs(0.5575 - resized_tag.x2) < 0.001)
        self.assertTrue(abs(0.3959 - resized_tag.y2) < 0.001)


