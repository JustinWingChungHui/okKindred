from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestCustomUserViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.user = User.objects.create_user(email='bruce_lee@email.com', password='enter the dragon', name='Bruce Lee' )

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
        response = self.client.get('/settings/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'custom_user/settings.html')

    def test_can_change_password(self):
        '''
        Test can receive post request to change password and check new password works
        '''
        User.objects.create_user(email='stephen_chow@email.com', password='god of cookery', name='Stephen Chow' )
        self.client.login(email='stephen_chow@email.com', password='god of cookery')
        self.client.post('/accounts/change_password/',{'password': 'shaolin soccer'})
        self.client.login(email='stephen_chow@email.com', password='shaolin soccer')

    def test_can_update_language(self):
        '''
        Test can receive post request to change language
        '''

        self.client.login(email='bruce_lee@email.com', password='enter the dragon')
        self.client.post('/accounts/update_settings/',{'name': 'language', 'value': 'pl'})

        self.user = User.objects.get(pk=self.user.id)
        self.assertEqual('pl', self.user.language)


    def test_can_delete_account_without_deleting_profile(self):
        '''
        Test that a user can delete their account without deleting their profile
        '''
        family = Family()
        family.save()

        user = User.objects.create_user(email='lau_fok_wing@email.com', password='infernal afffairs', name='Lau Fok Wing' )
        Person.objects.create(name='Lau Fok Wing', gender='M', family_id=family.id, user_id = user.id)

        self.client.login(email='lau_fok_wing@email.com', password='infernal afffairs')
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

        user = User.objects.create_user(email='andy_lau@email.com', password='infernal afffairs', name='Andy Lau' )
        Person.objects.create(name='Andy Lau', gender='M', family_id=family.id, user_id = user.id)

        self.client.login(email='andy_lau@email.com', password='infernal afffairs')
        self.client.post('/accounts/delete/',{'delete_profile': '1',})

        self.assertEqual(0, Person.objects.filter(name='Lau Fok Wing').count())
        self.assertEqual(0, User.objects.filter(email='andy_lau@email.com').count())