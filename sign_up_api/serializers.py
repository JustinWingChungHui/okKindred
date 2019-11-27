from rest_framework import serializers
from sign_up.models import SignUp

class SignUpSerializer(serializers.ModelSerializer):
    '''
    Defines fields to be serialized for a sign up model
    '''

    class Meta:
        model = SignUp
        fields = ('name', 'gender', 'language',
                'email_address', 'birth_year', 'address',
                'creation_date')