from django.test import TestCase
from email_confirmation.models import EmailConfirmation
from custom_user.models import User
from family_tree.models import Person, Family
from django.utils import timezone
from datetime import timedelta
from django.test.utils import override_settings


@override_settings(SSLIFY_DISABLE=True)
class EmailConfirmationTestCase(TestCase):
    '''
    Tests for this app
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='zandra_rhodes@email.com', password='killer queen', name='Zandra Rhodes', family_id=self.family.id)
        self.person = Person.objects.create(name='Tim Staffell', gender='M', family_id=self.family.id, language='en')


    def test_generate_confirmation_key(self):
        '''
        Tests generate_confirmation_key function creates a confirmation key without errors
        '''

        ec = EmailConfirmation(email_address='tim_staffell@smile.com', person_id = self.person.id, user_who_invited_person_id=self.user.id)
        ec.generate_confirmation_key()

        self.assertNotEqual(None, ec.confirmation_key)
        self.assertEqual(True, len(ec.confirmation_key) > 10)


    def test_create_email_body_html(self):
        '''
        Tests that this generates a valid email body
        '''
        ec = EmailConfirmation(email_address='tim_staffell@smile.com', person = self.person
                                , user_who_invited_person_id=self.user.id, confirmation_key='earth')

        email_body = ec._create_email_body_html()

        self.assertEqual(True, 'invited by Zandra Rhodes' in email_body)
        self.assertEqual(True, '<a href="https://www.okkindred.com/accounts/confirmation=earth/">https://www.okkindred.com/accounts/confirmation=earth/</a>' in email_body)
        self.assertEqual(True, 'Hello Tim Staffell' in email_body)


    def test_send_email(self):
        '''
        Tests that an email is created and sent
        '''

        ec = EmailConfirmation(email_address='tim_staffell@smile.com', person = self.person
                                , user_who_invited_person_id=self.user.id, confirmation_key='da5ee09f3823893df60a5ccfdb6bfda8c64c880657d9560a6739cd1dbf67c3de')

        before = timezone.now()
        ec.send_email()
        after = timezone.now()

        self.assertEqual(True, ec.sent >= before)
        self.assertEqual(True, ec.sent <= after)


    def test_remove_expired_email_confirmations(self):
        '''
        Tests that email confirmations that are over a week old are removed
        '''
        before_person = Person.objects.create(name='before', gender='M', family_id=self.family.id, language='en')

        email_to_be_deleted = EmailConfirmation.objects.create(email_address='before@example.com'
                                                                , person = before_person
                                                                , user_who_invited_person_id=self.user.id
                                                                , confirmation_key='12345'
                                                                , sent=timezone.now() - timedelta(days=14))


        after_person = Person.objects.create(name='after', gender='M', family_id=self.family.id, language='en')

        email_to_be_kept = EmailConfirmation.objects.create(email_address='after@example.com'
                                                                , person = after_person
                                                                , user_who_invited_person_id=self.user.id
                                                                , confirmation_key='12345'
                                                                , sent=timezone.now() - timedelta(days=4))

        EmailConfirmation.objects.remove_expired_email_confirmations()

        self.assertEqual(0,  EmailConfirmation.objects.filter(id=email_to_be_deleted.id).count())
        self.assertEqual(1,  EmailConfirmation.objects.filter(id=email_to_be_kept.id).count())


    def test_confirm_invite_view_loads(self):
        '''
        Tests that the view for confirming an invite is loaded for a valid confirmation key
        '''
        person = Person.objects.create(name='Great King Rat', gender='M', family_id=self.family.id, language='en')

        invite = EmailConfirmation.objects.create(email_address='great_king_rat@example.com'
                                                                , person = person
                                                                , user_who_invited_person_id=self.user.id
                                                                , sent=timezone.now())

        response = self.client.get('/accounts/confirmation={0}/'.format(invite.confirmation_key))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/confirm_invite.html')
        self.assertEqual(True, b'Great King Rat' in response.content)
        self.assertEqual(True, b'Zandra Rhodes' in response.content)


    def test_expired_invite_view_loads(self):
        '''
        Tests that the view for an expired invite loads
        '''
        response = self.client.get('/accounts/invalid_expired/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/invalid_expired.html')


    def test_confirm_invite_view_does_not_load_with_invalid_confirmation_code(self):
        '''
        Tests that the view for confirming an invite shows invalid/expired page
        '''

        response = self.client.get('/accounts/confirmation=not_a_real_confirmation_code/')

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/invalid_expired.html')


    def test_confirm_invite_view_post_does_all_the_correct_stuff(self):
        '''
        Tests that confirming invite
        1. Loads
        2. Creates a user correctly
        3. Assigns the user to a person
        4. Deletes the invite
        5. Logs in and displays home page
        '''

        person = Person.objects.create(name='Mike Stone', gender='M', family_id=self.family.id, language='en', email='mike_stone@example.com')

        invite = EmailConfirmation.objects.create(email_address='mike_stone@example.com'
                                                                , person = person
                                                                , user_who_invited_person_id=self.user.id
                                                                , sent=timezone.now())

        response = self.client.post('/accounts/confirmation={0}/'.format(invite.confirmation_key),{'password': 'My Fairy King'})

        self.assertEqual(False, response.status_code == 404)

        new_user = User.objects.get(email='mike_stone@example.com')
        self.assertEqual('Mike Stone', new_user.name)
        self.assertEqual(self.family.id, new_user.family_id)
        self.assertEqual('en', new_user.language)

        person = Person.objects.get(id=person.id)
        self.assertEqual(new_user.id, person.user_id)

        self.assertEqual(0, EmailConfirmation.objects.filter(email_address='mike_stone@example.com').count())


        #Diverted to home page
        self.assertRedirects(response, '/home/', status_code=302, target_status_code=200, msg_prefix='')

        #check confirmation address no longer valid
        response = self.client.get('/accounts/confirmation={0}/'.format(invite.confirmation_key))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/invalid_expired.html')

        response = self.client.post('/accounts/confirmation={0}/'.format(invite.confirmation_key),{'password': 'My Fairy King'})
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/invalid_expired.html')


    def test_confirm_invite_view_post_404_with_incorrect_confirmation_key(self):
        '''
        Check we can't be too easily hacked
        '''
        response = self.client.post('/accounts/confirmation=not_a_real_confirmation_code/',{'password': 'My Fairy King'})

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'email_confirmation/invalid_expired.html')


    def test_invite_person_creates_fails_for_existing_user(self):
        '''
        test for invite person post request
        '''
        user = User.objects.create_user(email='existing_user@email.com', password='existing_user', name='Existing User')
        person = Person.objects.create(name='existing_user', gender='M', family_id=self.family.id, language='en', email='existing_user@email.com', user_id=user.id)

        self.client.login(email='existing_user@email.com', password='existing_user')
        response = self.client.post('/accounts/invite_person={0}/'.format(person.id))
        self.assertEqual(404, response.status_code)


    def test_invite_person_fails_if_pending_invite(self):
        '''
        test for invite person post request
        '''
        person = Person.objects.create(name='Norman Sheffield', gender='M', family_id=self.family.id, language='en', email='norman_sheffield@email.com')

        EmailConfirmation.objects.create(email_address='norman_sheffield@email.com'
                                                                , person = person
                                                                , user_who_invited_person_id=self.user.id
                                                                , sent=timezone.now())

        self.client.login(email='zandra_rhodes@email.com', password='killer queen')

        response = self.client.post('/accounts/invite_person={0}/'.format(person.id))
        self.assertEqual(404, response.status_code)


    def test_invite_person_successfully_creates_invite(self):
        '''
        test for invite person post request
        '''
        person = Person.objects.create(name='Jim Beach', gender='M', family_id=self.family.id, language='en', email='jim_beach@email.com')

        self.client.login(email='zandra_rhodes@email.com', password='killer queen')

        response = self.client.post('/accounts/invite_person={0}/'.format(person.id))
        self.assertRedirects(response, '/profile={0}/'.format(person.id), status_code=302, target_status_code=200, msg_prefix='')

        invite =  EmailConfirmation.objects.get(person_id=person.id)
        self.assertEqual('jim_beach@email.com', invite.email_address)
        self.assertEqual(self.user.id, invite.user_who_invited_person.id)
