from django.test import TestCase
from custom_user.models import User
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestCustomUserViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.user = User.objects.create_user(email='bruce_lee@email.com', password='enter the dragon', name='Bruce Lee' )
        self.user.save()


