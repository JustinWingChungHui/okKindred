from django.test import TestCase
from emailer.models import Email


class EmailTestCase(TestCase):
    '''
    Tests for the email class
    '''

    def test_can_send_email(self):
        '''
        Test to ensure that an email can be sent without errors
        '''
        email = Email(
                    email_type = 'N'
                    ,recipient = 'info@okkindred.com'
                    ,subject = 'test_can_send_email'
                    ,content = ' emailer.tests.py'
                )

        email.send()

        self.assertEqual(True, email.send_successful)


    def test_process_emails(self):
        '''
        Test to ensure that multiple queued emails can be sent without errors
        '''
        email1 = Email(
                    email_type = 'N'
                    ,recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                )
        email1.save()

        email2 = Email(
                    email_type = 'N'
                    ,recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                )
        email2.save()

        email3 = Email(
                    email_type = 'N'
                    ,recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,send_attempts = 4
                )
        email3.save()

        email4 = Email(
                    email_type = 'N'
                    ,recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,send_successful = True
                )
        email4.save()

        Email.objects.process_emails()

        #reload objects
        email1 = Email.objects.get(id=email1.id)
        email2 = Email.objects.get(id=email2.id)
        email3 = Email.objects.get(id=email3.id)

        self.assertEqual(True, email1.send_successful)
        self.assertEqual(True, email2.send_successful)
        self.assertEqual(False, email3.send_successful)
        self.assertEqual(0, Email.objects.filter(id=email4.id).count())
