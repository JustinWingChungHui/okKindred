from rest_framework import serializers
from suggested_image_tagging.models import SuggestedTag

class SuggestedTagSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialized for a Tag
    '''

    person_name = serializers.CharField(source='person.name', allow_null=True)

    class Meta:
        model = SuggestedTag
        fields = ('id', 'image_id', 'person_id', 'person_name',
                    'probability', 'x1', 'x2', 'y1', 'y2',
                    'creation_date', 'last_updated_date')