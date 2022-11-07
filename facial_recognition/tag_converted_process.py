from django.conf import settings
from gallery.models import Tag
from common.file_downloader import clear_directory
from facial_recognition.models import FaceModel
from facial_recognition.train import process_family, process_file, get_file_for_tag

import pickle

def tag_converted_process(messages):
    try:
        tag_ids = []

        for message in messages:
            if message.integer_data:
                tag_ids.append(message.integer_data)

        # Get all face detected tags
        tags = Tag.objects.select_related('image'
            ).filter(pk__in=tag_ids)

        # Group into families
        families = {}
        for tag in tags:
            if not tag.image.family_id in families:
                families[tag.image.family_id] = []

            families[tag.image.family_id].append(tag)

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



def update_family_model(family_id, tags):

    clear_directory(settings.FACE_RECOG_TRAIN_TEMP_DIR)

    # Getting Face Models for family
    face_model = FaceModel.objects.filter(family_id= family_id).first()

    if not face_model:
        # No face model, create new one
        process_family(family_id)

    else:
        X = pickle.loads(face_model.fit_data_faces)
        y = pickle.loads(face_model.fit_data_person_ids)

        files = []
        for tag in tags:
            if tag.image.large_thumbnail:
                file = get_file_for_tag(tag, tag.image, settings.FACE_RECOG_TRAIN_TEMP_DIR)
                files.append(file)

                process_file(file, X, y, tag.person_id)

        if len(files) > 0:
            face_model.update_knn_classifier(X, y)


