from family_tree.models import Relation
from rest_framework import serializers

# Serializers define the API representation.
class RelationSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialised for a relation between two people
    '''
    class Meta:
        model = Relation
        fields = ('id', 'from_person_id', 'to_person_id', 'relation_type',
        'creation_date', 'last_updated_date')
