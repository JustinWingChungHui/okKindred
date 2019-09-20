from custom_user.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialised for a a list of Users
    '''
    class Meta:
        model = User
        fields = ('email', 'name')

# Serializers define the API representation.
class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialised for a User
    '''
    class Meta:
        model = User
        fields = ('name', 'language', 'receive_update_emails', 'receive_photo_update_emails', 'date_joined')



