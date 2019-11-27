from rest_framework import serializers
from gallery.models import Image

class ImageSerializer(serializers.ModelSerializer):
    '''
    Defines fields to be serialized for an image
    '''
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.name', read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'gallery_id', 'title', 'description',
                    'original_image', 'original_image_height', 'original_image_width',
                    'thumbnail', 'thumbnail_height', 'thumbnail_width',
                    'large_thumbnail', 'large_thumbnail_height', 'large_thumbnail_width',
                    'date_taken', 'latitude', 'longitude', 'creation_date', 'last_updated_date',
                    'uploaded_by')
