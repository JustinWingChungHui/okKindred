from rest_framework import serializers
from gallery.models import Gallery

class GallerySerializer(serializers.ModelSerializer):
    '''
    Defines fields to be serialized for a gallery
    '''

    class Meta:
        model = Gallery
        fields = ('id', 'title', 'description',
                    'thumbnail', 'thumbnail_height', 'thumbnail_width',
                    'creation_date', 'last_updated_date')