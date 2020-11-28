from django.db import models
import threading

class Gallery(models.Model):
    '''
    Represents a gallery object uses some principes from
    https://github.com/jdriscoll/django-photologue/blob/master/photologue/models.py
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'gallery'
        verbose_name_plural = "Galleries"
        unique_together = (('title', 'family'),)
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['family']),
            models.Index(fields=['creation_date'])
        ]

    title = models.CharField(max_length=50, null=False, blank=False)
    family = models.ForeignKey('family_tree.Family', null=False, on_delete=models.CASCADE) #Use of model string name to prevent circular import

    description = models.TextField(blank=True)

    thumbnail = models.ImageField(blank=True, null=False)

    # width_field='thumbnail_width', height_field='thumbnail_height'
    # Unlinked to prevent opening and saving again
    thumbnail_height = models.IntegerField(null=True)
    thumbnail_width = models.IntegerField(null=True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return str(self.family_id) + ': ' + self.title


    def delete_all_images(self):
        '''
        Deletes all related images in the gallery
        '''
        from gallery.models import Image

        images = Image.objects.filter(gallery_id = self.id)

        #Delete actual files
        for im in images:
            try:
                im.delete_local_image_files()
                threading.Thread(target=im.delete_remote_image_files).start()                
            except:
                pass

        #Delete database records
        images.delete()
