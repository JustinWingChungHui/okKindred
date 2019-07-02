from family_tree.models import Person
from rest_framework import serializers

# Serializers define the API representation.
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialised for a person
    '''
    class Meta:
        model = Person
        fields = ('id', 'name', 'birth_year', 'year_of_death', 'gender', 'locked', 'language', 'photo',
        'small_thumbnail', 'large_thumbnail', 'email', 'telephone_number', 'skype_name',
        'website', 'facebook', 'twitter', 'linkedin', 'occupation', 'spoken_languages',
        'address', 'biography', 'latitude', 'longitude', 'user_id', 'hierarchy_score',
        'creation_date', 'last_updated_date')


class PersonListSerializer(serializers.HyperlinkedModelSerializer):
    '''
    We only want to send limited data back when listing everyone
    '''
    class Meta:
        model = Person
        fields = ('id', 'name', 'birth_year', 'gender',
        'small_thumbnail', 'latitude', 'longitude', 'hierarchy_score')