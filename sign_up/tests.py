from django.test import TestCase
from django.test.client import Client as HttpClient
from django.test.utils import override_settings
from sign_up.models import SignUp
from family_tree.models import Family, Person
from custom_user.models import User

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class SignUpTestCase(TestCase): # pragma: no cover

    def setUp(self):
        self.client = HttpClient(HTTP_X_REAL_IP='127.0.0.1')


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


    def test_complete_registration_with_optional_data(self):
        '''
        Tests that the registration completes and creates all the required objects
        '''

        sign_up = SignUp.objects.create(
                name='Max Planck',
                gender = 'M',
                language = 'en',
                email_address = 'max_planck@spaceandtime.com',
                birth_year = 1965,
                address = 'Coventry')

        self.assertEqual(True, len(sign_up.confirmation_key) > 0)

        sign_up.complete_registration('password')

        #Check family created
        family = Family.objects.get(description = 'max_planck@spaceandtime.com')

        #Check User created
        user = User.objects.get(email = 'max_planck@spaceandtime.com')
        self.assertEqual('max_planck@spaceandtime.com', user.email)
        self.assertEqual('Max Planck', user.name)
        self.assertEqual(family.id, user.family_id)
        self.assertEqual('en', user.language)

        #Check person created
        person = Person.objects.get(email = 'max_planck@spaceandtime.com')
        self.assertEqual(family.id, person.family_id)
        self.assertEqual(user.id, person.user_id)
        self.assertEqual('en', person.language)
        self.assertEqual('Max Planck', person.name)
        self.assertEqual('M', person.gender)
        self.assertEqual(1965, person.birth_year)
        self.assertEqual('Coventry', person.address)

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




