from django.conf import settings
from family_tree.models import Person
from common.file_downloader import download_file, clear_directory
from facial_recognition.models import FaceModel
from facial_recognition.train import process_family, process_file

import pickle

def profile_photo_process(messages):

    try:
        person_ids = []

        for message in messages:
            if message.integer_data:
                person_ids.append(message.integer_data)

        # Getting people
        people = Person.objects.filter(pk__in=person_ids)

        # Group into families
        families = {}
        for person in people:
            if not person.family_id in families:
                families[person.family_id] = []

            families[person.family_id].append(person)

        # Update each family model
        for family_id in families.keys():
            update_family_model(family_id, families[family_id])

        for message in messages:
            message.processed = True
            message.save()

    except Exception as e:
        print(e)

        for message in messages:
            message.error = True
            message.error_message = str(e)[:512]
            message.save()




def update_family_model(family_id, people):
    # Updating family model
    clear_directory(settings.FACE_RECOG_TRAIN_TEMP_DIR)

    # Getting Face Models for family
    face_model = FaceModel.objects.filter(family_id=family_id).first()

    if not face_model:
        # No face model, create new one
        process_family(family_id)

    else:
        X = pickle.loads(face_model.fit_data_faces)
        y = pickle.loads(face_model.fit_data_person_ids)

        files = []
        for person in people:
            if person.large_thumbnail:
                file = download_file(settings.FACE_RECOG_TRAIN_TEMP_DIR, person.large_thumbnail)
                files.append(file)

                process_file(file, X, y, person.id)

        if len(files) > 0:
            face_model.update_knn_classifier(X, y)





