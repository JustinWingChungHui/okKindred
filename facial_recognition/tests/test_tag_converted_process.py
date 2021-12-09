from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from facial_recognition.models import FaceModel
from facial_recognition.file_downloader import clear_directory
from facial_recognition.train import process_family
from facial_recognition.tag_converted_process import tag_converted_process
from message_queue.models import Queue, Message

import os
import pickle
import shutil

@override_settings(SSLIFY_DISABLE=True,
            MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
            MEDIA_URL=settings.MEDIA_URL_TEST,
            AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST,
            FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR = settings.FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR,
            FACE_RECOG_TRAIN_TEMP_DIR = settings.FACE_RECOG_TRAIN_TEST_DIR)
class TagConvertedProcessTest(TestCase): # pragma: no cover

    def setUp(self):
        '''
        Need to create a family and a gallery
        '''
        self.family = Family()
        self.family.save()

        self.gallery = Gallery.objects.create(title="test_gallery", family_id=self.family.id)

        clear_directory(settings.FACE_RECOG_TRAIN_TEST_DIR)

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
        self.image.save()
        self.image.upload_files_to_s3()

        self.person = Person(name='Wallace', gender='M', email='wallace@creaturecomforts.com', family_id=self.family.id, language='en')
        self.person.save()

        self.tag = Tag.objects.create(image_id=self.image.id, x1=0.279, y1=0.188, x2=0.536, y2=0.381,
                                                            person_id=self.person.id, face_detected= True)

        # Upload new image
        self.test_image2 = os.path.join(settings.BASE_DIR, 'facial_recognition/tests/test_image_woman_and_baby.jpg')
        self.test_image2_destination = ''.join([settings.MEDIA_ROOT, 'galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image_woman_and_baby.jpg'])

        # Copy to test area
        shutil.copy2(self.test_image2, self.test_image2_destination)


        self.image2 = Image(gallery=self.gallery, family=self.family,
                        original_image=''.join(['galleries/', str(self.family.id), '/', str(self.gallery.id), '/test_image_woman_and_baby.jpg']))
        self.image2.save()
        self.image2.upload_files_to_s3()

        self.person2 = Person(name='Gromit', gender='M', email='gomit@creaturecomforts.com', family_id=self.family.id, language='en')
        self.person2.save()

        # Create a trained model
        process_family(self.family.id)




    def tearDown(self):

        self.image.delete_local_image_files()
        self.image.delete_remote_image_files()

        self.image2.delete_local_image_files()
        self.image2.delete_remote_image_files()

        try:
            os.remove(self.test_image_destination)
        except:
            pass

        try:
            os.remove(self.test_image2_destination)
        except:
            pass


    def test_person_deleted_update_face_model(self):

        # Create tag
        tag2 = Tag.objects.create(image_id=self.image2.id, x1=0.312, y1=0.239, x2=0.732, y2=0.811,
                                                            person_id=self.person2.id, face_detected= True)

        tag_converted_process_id = Queue.objects.get(name='tag_converted_process').id

        message = Message.objects.create(queue_id=tag_converted_process_id, integer_data = tag2.id)

        tag_converted_process([message])
        face_model = FaceModel.objects.filter(family_id=self.family.id).first()

        X = pickle.loads(face_model.fit_data_faces)

        self.assertEqual(2, len(X))


