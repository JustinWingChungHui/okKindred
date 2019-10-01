from django.test import TestCase
from django.test.client import Client as HttpClient
from django.test.utils import override_settings
from custom_user.models import User
from family_tree.models import Person, Family

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class TestCustomUserViews(TestCase): # pragma: no cover

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()
        self.user = User.objects.create_user(email='bruce_lee@email.com', password='enter the dragon', name='Bruce Lee' )
        self.person = Person.objects.create(name='Bruce Lee', gender='M', email='bruce_lee@email.com', family_id=self.family.id, language='en', user_id=self.user.id)

        self.client = HttpClient(HTTP_X_REAL_IP='127.0.0.1')

