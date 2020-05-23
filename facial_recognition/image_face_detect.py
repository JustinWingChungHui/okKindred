from django.conf import settings
from gallery.models import Image
from family_tree.models import Person
from facial_recognition.file_downloader import download_file, clear_directory
from facial_recognition.models import FaceModel
from facial_recognition.train import process_family
from suggested_image_tagging.models import SuggestedTag

import face_recognition
import datetime
import pickle
import traceback

def image_face_detect(messages):
    '''
    Detects faces in images and suggest who they may be from trained family data
    '''
    try:
        clear_directory(settings.FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR)

        # Get all the image ids
        image_ids = []
        for message in messages:
            if message.integer_data:
                image_ids.append(message.integer_data)

        # Get all database images
        db_images = Image.objects.filter(pk__in=image_ids)


        suggested_tag_count = 0

        face_models = {}

        for db_image in db_images:

            # Download remote image file
            local_file = download_file(settings.FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR, db_image.large_thumbnail)

            # Load image into memory
            image = face_recognition.load_image_file(local_file)

            # Find faces in image
            locations = face_recognition.face_locations(image)

            # Created a suggested tag for each detected face
            for location in locations:
                top, right, bottom, left = location

                # Normalize the location
                x1 = left / db_image.large_thumbnail_width
                x2 = right / db_image.large_thumbnail_width
                y1 = top / db_image.large_thumbnail_height
                y2 = bottom / db_image.large_thumbnail_height

                new_suggested_tag = SuggestedTag(image_id = db_image.id,
                                                    x1 = x1,
                                                    x2 = x2,
                                                    y1 = y1,
                                                    y2 = y2,
                                                    last_updated_date = datetime.datetime.utcnow(),
                                                    creation_date = datetime.datetime.utcnow())

                # Load the face model for each family
                if db_image.family_id in face_models:
                    face_model = face_models[db_image.family_id]
                else:
                    face_model = FaceModel.objects.get(family_id=db_image.family_id)
                    face_models[db_image.family_id] = face_model

                if face_model:

                    # Find encodings for faces in the image
                    faces_encodings = face_recognition.face_encodings(image, known_face_locations=(location,))

                    # Match a family member to the face

                    # Load the training model (K nearest neighbours)
                    trained_knn_model = pickle.loads(face_model.trained_knn_model)
                    distances, fit_face_indexes = trained_knn_model.kneighbors(faces_encodings, n_neighbors=1)

                    if len(distances) > 0 and len(distances[0]) > 0:
                        fit_data_person_ids = pickle.loads(face_model.fit_data_person_ids)

                        if len(fit_data_person_ids) > fit_face_indexes[0][0]:

                            # Check person exists
                            person_id = fit_data_person_ids[fit_face_indexes[0][0]]
                            if Person.objects.filter(pk=person_id).exists():

                                # Adding matched person
                                new_suggested_tag.probability = distances[0][0]
                                new_suggested_tag.person_id = person_id

                            else:
                                print('Invalid person_id: {}'.format(person_id))

                new_suggested_tag.save()

                suggested_tag_count += 1

        # Messages processed
        for message in messages:
            message.processed = True
            message.save()

    except:
        print(traceback.format_exc())

        for message in messages:
            message.error = True
            message.error_message = str(traceback.format_exc())[:512]
            message.save()




