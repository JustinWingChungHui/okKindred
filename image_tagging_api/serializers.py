from rest_framework import serializers
from gallery.models import Tag

class TagSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialized for a Tag
    '''

    person_name = serializers.CharField(source='person.name')

    class Meta:
        model = Tag
        fields = ('id', 'image_id', 'person_id', 'person_name',
                    'x1', 'x2', 'y1', 'y2',
                    'creation_date', 'last_updated_date')