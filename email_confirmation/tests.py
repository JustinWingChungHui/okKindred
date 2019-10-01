from django.conf import settings
from django.test import TestCase
from django.test.client import Client as HttpClient
from django.test.utils import override_settings
from django.utils import timezone
from datetime import timedelta

from email_confirmation.models import EmailConfirmation
from custom_user.models import User
from family_tree.models import Person, Family

@override_settings(SECURE_SSL_REDIRECT=False, AXES_BEHIND_REVERSE_PROXY=False)
class EmailConfirmationTestCase(TestCase): # pragma: no cover
    '''
    Tests for this app
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='zandra_rhodes@email.com', password='killer queen', name='Zandra Rhodes', family_id=self.family.id)
        self.person = Person.objects.create(name='Tim Staffell', gender='M', family_id=self.family.id, language='en')
        self.client = HttpClient(HTTP_X_REAL_IP='127.0.0.1')


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

        link = '<a href="' + settings.DOMAIN + '/#/accounts/invite_confirmation/earth/">' + settings.DOMAIN + '/#/accounts/invite_confirmation/earth/</a>'
        self.assertEqual(True, 'invited by Zandra Rhodes' in email_body)
        self.assertEqual(True, link in email_body)
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
        Tests that email confirmations that are over a month old are removed
        '''
        before_person = Person.objects.create(name='before', gender='M', family_id=self.family.id, language='en')

        email_to_be_deleted = EmailConfirmation.objects.create(email_address='before@example.com'
                                                                , person = before_person
                                                                , user_who_invited_person_id=self.user.id
                                                                , confirmation_key='12345'
                                                                , sent=timezone.now() - timedelta(days=34))


        after_person = Person.objects.create(name='after', gender='M', family_id=self.family.id, language='en')

        email_to_be_kept = EmailConfirmation.objects.create(email_address='after@example.com'
                                                                , person = after_person
                                                                , user_who_invited_person_id=self.user.id
                                                                , confirmation_key='12345'
                                                                , sent=timezone.now() - timedelta(days=4))

        EmailConfirmation.objects.remove_expired_email_confirmations()

        self.assertEqual(0,  EmailConfirmation.objects.filter(id=email_to_be_deleted.id).count())
        self.assertEqual(1,  EmailConfirmation.objects.filter(id=email_to_be_kept.id).count())


