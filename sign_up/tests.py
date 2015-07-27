from django.test import TestCase
from django.test.utils import override_settings
from sign_up.models import SignUp
from family_tree.models import Family, Person
from custom_user.models import User

@override_settings(SSLIFY_DISABLE=True)
class SignUpTestCase(TestCase): # pragma: no cover


    def test_remove_expired_sign_ups(self):
        '''
        Test the signups are removed correctly
        '''
        sign_up1 = SignUp.objects.create(
                        name='sign_up1',
                        gender = 'M',
                        language = 'en',
                        email_address = 'stephen_hawking@spaceandtime.com',
                        confirmation_key = '123456789')

        sign_up2 = SignUp.objects.create(
                        name='sign_up2',
                        gender = 'M',
                        language = 'en',
                        email_address = 'chris_lintott@spaceandtime.com',
                        confirmation_key = '12345678a')


        SignUp.objects.remove_expired_sign_ups(0)

        self.assertEqual(0, SignUp.objects.filter(id = sign_up1.id).count())
        self.assertEqual(0, SignUp.objects.filter(id = sign_up2.id).count())


    def test_complete_registration(self):
        '''
        Tests that the registration completes and creates all the required objects
        '''

        sign_up = SignUp.objects.create(
                name='Edwin Hubble',
                gender = 'M',
                language = 'en',
                email_address = 'edwin_hubble@spaceandtime.com')

        self.assertEqual(True, len(sign_up.confirmation_key) > 0)

        sign_up.complete_registration('password')

        #Check family created
        family = Family.objects.get(description = 'edwin_hubble@spaceandtime.com')

        #Check User created
        user = User.objects.get(email = 'edwin_hubble@spaceandtime.com')
        self.assertEqual('edwin_hubble@spaceandtime.com', user.email)
        self.assertEqual('Edwin Hubble', user.name)
        self.assertEqual(family.id, user.family_id)
        self.assertEqual('en', user.language)

        #Check person created
        person = Person.objects.get(email = 'edwin_hubble@spaceandtime.com')
        self.assertEqual(family.id, person.family_id)
        self.assertEqual(user.id, person.user_id)
        self.assertEqual('en', person.language)
        self.assertEqual('Edwin Hubble', person.name)
        self.assertEqual('M', person.gender)

        #Check sign up is deleted
        self.assertEqual(0, SignUp.objects.filter(name='Edwin Hubble').count())


    def test_send_email(self):
        '''
        Tests that an email is created correctly
        '''
        sign_up = SignUp(
                            name='Edwin Hubble',
                            gender = 'F',
                            language = 'en',
                            email_address = 'edwin_hubble@spaceandtime.com')

        sign_up.send_email()

    def test_sign_up_view_404_for_logged_in_user(self):
        '''
        Test sign up 404 for logged in user
        '''
        family = Family.objects.create(description="johnny two accounts")
        User.objects.create_user(email='john2accounts@email.com', password='fraudster', name='johnny two accounts', family_id=family.id)

        self.client.login(email='john2accounts@email.com', password='fraudster')
        response = self.client.get('/accounts/sign_up/')

        self.assertEqual(404, response.status_code)


    def test_sign_up_view_loads(self):
        '''
        Tests the sign up view loads
        '''
        response = self.client.get('/accounts/sign_up/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sign_up/sign_up.html')


    def test_sign_up_post_invalid_email(self):
        '''
        Tests the sign up with invalid email returns invalid email page
        '''
        response = self.client.post('/accounts/sign_up/',
                                    {
                                        'name': 'name',
                                        'email': 'notanemail',
                                        'gender': 'O',
                                        'language': 'en'
                                    })

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sign_up/invalid_email.html')


    def test_sign_up_post_email_in_use(self):
        '''
        Tests the sign up with invalid email returns invalid email page
        '''
        family = Family.objects.create(description = 'test_sign_up_post_invalid_email')
        Person.objects.create(family = family, name = 'name', gender = 'F', email = 'inuse@email.com')

        response = self.client.post('/accounts/sign_up/',
                                    {
                                        'name': 'name',
                                        'email': 'inuse@email.com',
                                        'gender': 'O',
                                        'language': 'en'
                                    })

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sign_up/email_in_use.html')

    def test_sign_up_post_create_new_sign_up(self):
        '''
        Tests the sign up with invalid email returns invalid email page
        '''
        response = self.client.post('/accounts/sign_up/',
                                    {
                                        'name': 'name',
                                        'email': 'a_new_email@email.com',
                                        'gender': 'O',
                                        'language': 'en'
                                    })

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sign_up/check_email.html')

        self.assertEqual(1, SignUp.objects.filter(email_address = 'a_new_email@email.com').count())


    def test_sign_up_confirmation_invalid_confirmation_key(self):
        '''
        Tests that a 404 is raised for an invalid confirmation key
        '''
        response = self.client.get('/accounts/sign_up_confirmation=not_a_validkey/')

        self.assertEqual(404, response.status_code)


    def test_sign_up_confirmation_displays_password_form(self):
        '''
        Tests that a password form is displayed for an valid confirmation key
        '''
        sign_up = SignUp.objects.create(
                name='a new user',
                gender = 'M',
                language = 'en',
                email_address = 'anewuser@iamanewuser.com')


        response = self.client.get('/accounts/sign_up_confirmation={0}/'.format(sign_up.confirmation_key))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sign_up/choose_password.html')

    def test_sign_up_confirmation_post_creates_user(self):
        '''
        Tests that a we create a new user when we enter a password
        '''

        sign_up = SignUp.objects.create(
                name='joining user',
                gender = 'M',
                language = 'en',
                email_address = 'joininguser@iamanewuser.com')

        response = self.client.post('/accounts/sign_up_confirmation={0}/'.format(sign_up.confirmation_key), {'password' : 'letmeinplease'})

        self.assertEqual(True, User.objects.filter(email='joininguser@iamanewuser.com').count() == 1)
        self.assertNotEqual(404, response.status_code)


