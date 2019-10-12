from django.db import models

from family_tree.models import Family

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