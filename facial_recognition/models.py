from django.db import models
from sklearn import neighbors
from family_tree.models import Family

import math
import pickle

# Create your models here.
class FaceModel(models.Model):

    family = models.OneToOneField(
        Family,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    fit_data_faces = models.BinaryField(null = False, blank = False)
    fit_data_person_ids = models.BinaryField(null = False, blank = False)

    n_neighbors = models.IntegerField(null = False, blank = False)
    trained_knn_model = models.BinaryField(null = False, blank = False)

    def __str__(self): # __unicode__ on Python 2
        return 'Family:{0} n:{1}'.format(self.family_id, self.n_neighbors)


    def update_knn_classifier(self, X, y):
        '''
        Updates the face recognition model
        '''
        # Good estimate
        n_neighbors = int(round(math.sqrt(len(X))))

        # Creating and training the KNN classifier
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')

        
        knn_clf.fit(X, y)

        # 'Pickling and saving to db
        self.fit_data_faces = pickle.dumps(X)
        self.fit_data_person_ids = pickle.dumps(y)
        self.n_neighbors = n_neighbors
        self.trained_knn_model = pickle.dumps(knn_clf)
        self.save()



