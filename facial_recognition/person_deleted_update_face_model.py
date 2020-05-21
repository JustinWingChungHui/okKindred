from facial_recognition.models import FaceModel
from facial_recognition.train import process_family


import json
import pickle


def person_deleted_update_face_model(messages):
    try:
        people = []

        for message in messages:
            if message.string_data:
                person = json.loads(message.string_data)
                people.append(person)

        # Group into families
        people_by_family_id = {}
        for person in people:
            family_id = person['family_id']
            if not family_id in people_by_family_id:
                people_by_family_id[family_id] = []

            people_by_family_id[family_id].append(person)

        for family_id in people_by_family_id.keys():
            update_family_model(family_id, people_by_family_id[family_id])

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

    # Getting Face Models for family
    face_model = FaceModel.objects.filter(family_id=family_id).first()

    if face_model is None:
        # No face model, create new one
        process_family(family_id)

    else:
        X = pickle.loads(face_model.fit_data_faces)
        y = pickle.loads(face_model.fit_data_person_ids)

        index_removed = False

        # Removing people from face models
        for person in people:
            person_id = person['person_id']
            while person_id in y:
                index = y.index(person_id)
                y.pop(index)
                X.pop(index)
                index_removed = True

        if index_removed:
            face_model.update_knn_classifier(X, y)







