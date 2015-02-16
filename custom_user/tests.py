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

    def test_invalid_login_with_incorrect_password(self):
        '''
        Test user cannot login with invalid password
        '''
        response = self.client.post('/accounts/auth/',  {'username': 'bruce_lee@email.com', 'password': 'game of death'}, follow=True)
        self.assertEqual(True, ('http://testserver/accounts/invalid', 302) in response.redirect_chain)


    def test_can_login_with_uppercase_email(self):
        '''
        Test user can login with case insensitive password
        '''
        response = self.client.post('/accounts/auth/',  {'username': 'Bruce_Lee@email.com', 'password': 'enter the dragon'}, follow=True)
        self.assertEqual(False, ('http://testserver/accounts/invalid', 302) in response.redirect_chain)


    def test_settings_view_displays(self):
        '''
        Test that the settings view is displayed correctly
        '''
        self.client.login(email='bruce_lee@email.com', password='enter the dragon')
        response = self.client.get('/en/settings/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'custom_user/settings.html')
