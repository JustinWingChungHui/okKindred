from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from gallery.models import Image, Gallery, Tag
from family_tree.models import Family, Person
from facial_recognition.models import FaceModel
from facial_recognition.file_downloader import clear_directory
from facial_recognition.train import process_family
from facial_recognition.profile_photo_process import profile_photo_process
from message_queue.models import Queue, Message
import os
import pickle
import shutil
import threading

@override_settings(SSLIFY_DISABLE=True,
            MEDIA_ROOT=settings.MEDIA_ROOT_TEST,
            FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR = settings.FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR,
            FACE_RECOG_TRAIN_TEMP_DIR = settings.FACE_RECOG_TRAIN_TEST_DIR)
class ProfilePhotoProcessTest(TestCase): # pragma: no cover

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
        self.test_image2_destination  = settings.MEDIA_ROOT + 'profile_photos/test_image_woman_and_baby.jpg'


        # Create a trained model
        process_family(self.family.id)



    def tearDown(self):
        self.image.delete_local_image_files()
        threading.Thread(target=self.image.delete_remote_image_files).start()

        try:
            os.remove(self.test_image_destination)
        except:
            pass

        try:
            os.remove(self.test_image2_destination)
        except:
            pass

        self.person.remove_local_images()
        threading.Thread(target=self.person.remove_remote_images).start()



    def test_profile_photo_process(self):

        # Copy to test area
        shutil.copy2(self.test_image2, self.test_image2_destination)

        # Add profile photo
        self.person.set_profile_image_crop_rotate_resize(self.test_image2_destination, 372, 406, 878, 1378, 0, True)
        self.person.save()

        profile_photo_process_id = Queue.objects.get(name='profile_photo_process').id


        message = Message.objects.create(queue_id=profile_photo_process_id, integer_data = self.person.id)

        profile_photo_process([message])
        face_model = FaceModel.objects.filter(family_id=self.family.id).first()

        X = pickle.loads(face_model.fit_data_faces)

        message = Message.objects.get(pk=message.id)

        self.assertEqual(1, len(X))
        self.assertEqual(False, message.error)







