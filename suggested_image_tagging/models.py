from django.db import models
from gallery.models import Image, Tag

# Create your models here.
class SuggestedTag(models.Model):
    '''
    Defines the model for a message queue
    '''

    class Meta:
        indexes = [
            models.Index(fields=['image']),
        ]

    image = models.ForeignKey(Image, blank=False, null=False, on_delete=models.CASCADE)

    #Use of model string name to prevent circular import
    # Nullable field because we might not be able to identify person
    person = models.ForeignKey('family_tree.Person', null=True, on_delete=models.CASCADE)
    probability = models.FloatField(null=True)

    #Box coordinates in the photo normalised to 1 (ie [(0,0),(1,1)] is entire photo
    x1 = models.FloatField(blank=False, null=False)
    y1 = models.FloatField(blank=False, null=False)
    x2 = models.FloatField(blank=False, null=False)
    y2 = models.FloatField(blank=False, null=False)


    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return '{0}_{1}'.format(self.image.title, self.id)

    def convertToTag(self, person_id):
        new_tag = Tag(image_id = self.image_id,
                        person_id = person_id,
                        x1 = self.x1,
                        y1 = self.y1,
                        x2 = self.x2,
                        y2 = self.y2,
                        face_detected = True)

        new_tag.save()
        self.delete()

        return new_tag


