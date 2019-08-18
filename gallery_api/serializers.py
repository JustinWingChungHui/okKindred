from rest_framework import serializers
from gallery.models import Gallery

class GallerySerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialized for a gallery
    '''

    class Meta:
        model = Gallery
        fields = ('id', 'title', 'description', 'thumbnail',
                    'creation_date', 'last_updated_date')