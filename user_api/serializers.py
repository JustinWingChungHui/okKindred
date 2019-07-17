from custom_user.models import User
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialised for a User
    '''
    class Meta:
        model = User
        fields = ('language', 'receive_update_emails', 'receive_photo_update_emails', 'date_joined')


