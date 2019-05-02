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

    def test_invalid_login_with_incorrect_password(self):
        '''
        Test user cannot login with invalid password
        '''
        response = self.client.post('/accounts/auth/',  {'username': 'bruce_lee@email.com', 'password': 'game of death'}, follow=True)
        self.assertEqual(True, ('/accounts/invalid', 302) in response.redirect_chain)


    def test_can_login_with_uppercase_email(self):
        '''
        Test user can login with case insensitive email
        '''
        response = self.client.post('/accounts/auth/',  {'username': 'Bruce_Lee@email.com', 'password': 'enter the dragon'}, follow=True)
        self.assertTrue('Your account has now been locked' in response.body)


    def test_locked_out_with_multiple_incorrect_password_attempts(self):
        '''
        Test user cannot login with after muliple attempts with invalid password
        '''

        for i in range(5):
            self.client.post('/accounts/auth/',  {'username': 'bruce_lee@email.com', 'password': 'game of death'}, follow=True, HTTP_X_REAL_IP='127.0.0.3')

        response = self.client.post('/accounts/auth/',  {'username': 'bruce_lee@email.com', 'password': 'enter the dragon'}, follow=True, HTTP_X_REAL_IP='127.0.0.3')
        self.assertTrue(b'Your account has now been locked' in response.content)


    def test_settings_view_displays(self):
        '''
        Test that the settings view is displayed correctly
        '''
        self.client.post('/accounts/auth/',  {'username': 'bruce_Lee@email.com', 'password': 'enter the dragon'})
        response = self.client.get('/settings/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'custom_user/settings.html')


    def test_can_change_password(self):
        '''
        Test can receive post request to change password and check new password works
        '''
        user = User.objects.create_user(email='stephen_chow@email.com', password='god of cookery', name='Stephen Chow' )
        Person.objects.create(name='Stephen Chow', gender='M', email='stephen_chow@email.com', family_id=self.family.id, language='en', user_id=user.id)

        self.client.post('/accounts/auth/',  {'username': 'stephen_chow@email.com', 'password': 'god of cookery'})
        self.client.post('/accounts/change_password/',{'password': 'shaolin soccer'})
        response = self.client.post('/accounts/auth/',  {'username': 'stephen_chow@email.com', 'password': 'shaolin soccer'}, follow=True)
        self.assertEqual(False, ('/accounts/invalid', 302) in response.redirect_chain)


    def test_can_update_language(self):
        '''
        Test can receive post request to change language
        '''

        self.client.post('/accounts/auth/',  {'username': 'bruce_Lee@email.com', 'password': 'enter the dragon'})
        self.client.post('/accounts/update_settings/',{'name': 'language', 'value': 'pl'})

        self.user = User.objects.get(pk=self.user.id)
        self.assertEqual('pl', self.user.language)


    def test_can_delete_account_without_deleting_profile(self):
        '''
        Test that a user can delete their account without deleting their profile
        '''
        family = Family()
        family.save()

        user = User.objects.create_user(email='lau_fok_wing@email.com', password='infernal affairs', name='Lau Fok Wing' )
        Person.objects.create(name='Lau Fok Wing', gender='M', family_id=family.id, user_id = user.id)

        self.client.post('/accounts/auth/',  {'username': 'lau_fok_wing@email.com', 'password': 'infernal affairs'})
        self.client.post('/accounts/delete/',{'delete_profile': '0',})

        self.assertEqual(1, Person.objects.filter(name='Lau Fok Wing').count())
        self.assertEqual(None, Person.objects.get(name='Lau Fok Wing').user_id)
        self.assertEqual(0, User.objects.filter(email='lau_fok_wing@email.com').count())



    def test_can_delete_account_and_profile(self):
        '''
        Test that a user can delete their account and their profile
        '''
        family = Family()
        family.save()

        user = User.objects.create_user(email='andy_lau@email.com', password='infernal affairs', name='Andy Lau' )
        Person.objects.create(name='Andy Lau', gender='M', family_id=family.id, user_id = user.id)

        self.client.post('/accounts/auth/',  {'username': 'andy_lau@email.com', 'password': 'infernal affairs'})
        self.client.post('/accounts/delete/',{'delete_profile': '1',})

        self.assertEqual(0, Person.objects.filter(name='Lau Fok Wing').count())
        self.assertEqual(0, User.objects.filter(email='andy_lau@email.com').count())


    def test_login_view_loads(self):
        '''
        Tests that the login view loads
        '''
        response = self.client.get('/accounts/login/')
        self.assertEqual(200, response.status_code)


    def test_next_parameter_sent_to_login(self):
        '''
        Tests that the next parameter appears as a hidden parameter in the login form
        '''
        response = self.client.get('/accounts/login/?next=/nexturl/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, b'nexturl' in response.content)
