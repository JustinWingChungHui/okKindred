from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from family_tree.models import Person

class AppTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        # Get person object associated with user
        person = Person.objects.get(user_id = self.user.id)
        if self.user.family_id != person.family_id:
            raise Http404

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['language'] = self.user.language
        data['person_id'] = person.id

        return data

