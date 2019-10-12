import pickle
from django.test import TestCase

from family_tree.models import Family
from facial_recognition.models import FaceModel

class FacialRecognitionTestCase(TestCase): # pragma: no cover


    def setUp(self):

        self.family = Family()
        self.family.save()


    def test_create_model(self):


        array1 = [(1 , 2), ('no', 'yes'), 'blah']
        array2 = [1, 2]
        obj1 = {
            'stuff': 'yes',
            'notstuff': 'no',
        }


        FaceModel.objects.create(
                            family=self.family,
                            fit_data_faces=pickle.dumps(array1),
                            fit_data_person_ids=pickle.dumps(array2),
                            n_neighbors=3,
                            trained_knn_model = pickle.dumps(obj1))


        result = FaceModel.objects.get(family=self.family)
        self.assertEqual(array1, pickle.loads(result.fit_data_faces))
        self.assertEqual(array2, pickle.loads(result.fit_data_person_ids))
        self.assertEqual(obj1, pickle.loads(result.trained_knn_model))

