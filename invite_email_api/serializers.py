from rest_framework import serializers
from email_confirmation.models import EmailConfirmation

class InviteEmailSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Defines fields to be serialized for an invite email
    '''
    person_name = serializers.CharField(source='person.name', read_only=True)
    username_who_invited_person = serializers.CharField(source='user_who_invited_person.name', read_only=True)
    language = serializers.CharField(source='person.language', read_only=True)

    class Meta:
        model = EmailConfirmation
        fields = ('person_id', 'person_name', 'email_address', 'sent', 'username_who_invited_person', 'language')
