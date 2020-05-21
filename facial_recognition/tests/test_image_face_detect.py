from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from facial_recognition.file_downloader import clear_directory
from facial_recognition.train import process_family
from facial_recognition.image_face_detect import image_face_detect
from message_queue.models import Queue, Message
from suggested_image_tagging.models import SuggestedTag

import os
import shutil

@override_settings(SSLIFY_DISABLE=True,
            MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
            FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR = settings.FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR)
class ImageFaceDetectTest(TestCase): # pragma: no cover

    def setUp(self):
        '''
        Need to create a family and a gallery
        '''
        self.family = Family()
        self.family.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        clear_directory(settings.FACE_RECOG_TRAIN_FACE_RECOGNITION_TEST_DIR)

        self.test_image = os.path.join(settings.BASE_DIR, 'facial_recognition/tests/test_image_woman.jpg')
        self.test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])
        self.test_image_s3_key = ''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg'])

        directory = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id)])
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Copy test image to media area
        shutil.copy2(self.test_image, self.test_image_destination)

        self.image = Image(gallery=self.gallery, family=self.family,
                            original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image.jpg']))
        self.image.save();
        self.image.upload_files_to_s3()

        self.person = Person(name='Wallace', gender='M', email='wallace@creaturecomforts.com', family_id=self.family.id, language='en')
        self.person.save()

        self.tag = Tag.objects.create(image_id=self.image.id, x1=0.279, y1=0.188, x2=0.536, y2=0.381,
                                                            person_id=self.person.id, face_detected= True)

        # Create a trained model
        process_family(self.family.id)




    def test_image_face_detect(self):

        # Upload new image
        new_test_image = os.path.join(settings.BASE_DIR, 'facial_recognition/tests/test_image_woman_and_baby.jpg')
        new_test_image_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image_woman_and_baby.jpg'])

        # Copy to test area
        shutil.copy2(new_test_image, new_test_image_destination)


        new_image = Image(gallery=self.gallery, family=self.family,
                        original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image_woman_and_baby.jpg']))
        new_image.save();
        new_image.upload_files_to_s3()

        # Create a message to resize tag
        image_face_detect_queue_id = Queue.objects.get(name='image_face_detect').id
        message = Message.objects.create(queue_id=image_face_detect_queue_id, integer_data = new_image.id)

        image_face_detect([message])

        suggested_tags = SuggestedTag.objects.filter(image_id=new_image.id)

        self.assertEqual(2, suggested_tags.count())
        self.assertEqual(self.person.id, suggested_tags[0].person_id)




