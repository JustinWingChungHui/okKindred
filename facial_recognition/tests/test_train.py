from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from facial_recognition.models import FaceModel

from facial_recognition.train import get_file_for_tag, process_file
from facial_recognition.train import process_person, process_family
from facial_recognition.file_downloader import clear_directory

import os
import shutil
import threading

@override_settings(SSLIFY_DISABLE=True,
            MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
            MEDIA_URL=settings.MEDIA_URL_TEST,
            AWS_STORAGE_BUCKET_NAME=settings.AWS_STORAGE_BUCKET_NAME_TEST, 
            FACE_RECOG_TRAIN_TEMP_DIR = settings.FACE_RECOG_TRAIN_TEST_DIR)
class TrainTestCase(TestCase): # pragma: no cover

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

        self.tag = Tag.objects.create(image_id=self.image.id, x1=0.2875, y1=0.1951, x2=0.5575, y2=0.3959,
                                                            person_id=self.person.id, face_detected= True)


    def tearDown(self):
        self.image.delete_local_image_files()
        threading.Thread(target=self.image.delete_remote_image_files).start()

        try:
            os.remove(self.test_image_destination)
        except:
            pass



    def test_get_file_for_tag(self):

        dir_name = settings.FACE_RECOG_TRAIN_TEST_DIR
        file = get_file_for_tag(self.tag, self.image, dir_name)

        self.assertIsNotNone(file)


    def test_process_file(self):

        X = []
        y = []
        file = self.test_image_destination

        process_file(file, X, y, self.person.id)

        self.assertEqual(1, len(X))
        self.assertEqual(1, len(y))


    def test_process_person(self):
        path = settings.MEDIA_ROOT + 'profile_photos/large_test_image1.jpg'
        shutil.copy2(self.test_image, path)

        self.person.set_profile_image_crop_rotate_resize(path, 1, 1, 380, 380, 0, True)
        self.person.save()

        X = []
        y = []

        process_person(self.person, X, y)

        self.person.remove_local_images()
        self.person.remove_remote_images()

        self.assertEqual(2, len(X))
        self.assertEqual(2, len(y))



    def test_process_family(self):
        path = settings.MEDIA_ROOT + 'profile_photos/large_test_image1.jpg'
        shutil.copy2(self.test_image, path)

        self.person.set_profile_image_crop_rotate_resize(path, 1, 1, 1200, 1700, 0, True)
        self.person.save()

        process_family(self.family.id)

        self.person.remove_local_images()
        self.person.remove_remote_images()

        face_model = FaceModel.objects.get(family_id=self.family.id)

        self.assertTrue(self.person.id in face_model.fit_data_person_ids)
        self.assertIsNotNone(face_model.trained_knn_model)

