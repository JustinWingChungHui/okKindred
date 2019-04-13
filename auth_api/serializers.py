from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AppTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['language'] = self.user.language

        return data

