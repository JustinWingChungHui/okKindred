from django.test import TestCase
from emailer.models import Email, FamilyNewsLetterEvents


class EmailTestCase(TestCase):
    '''
    Tests for the email class
    '''

    def test_can_send_email(self):
        '''
        Test to ensure that an email can be sent without errors
        '''
        email = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_can_send_email'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )

        email.send()

        self.assertEqual(True, email.send_successful)


    def test_process_emails(self):
        '''
        Test to ensure that multiple queued emails can be sent without errors
        '''
        email1 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email1.save()

        email2 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email2.save()

        email3 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                    ,send_attempts = 4
                )
        email3.save()

        email4 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                    ,send_successful = True
                )
        email4.save()

        Email.objects._process_emails()

        #reload objects
        email1 = Email.objects.get(id=email1.id)
        email2 = Email.objects.get(id=email2.id)
        email3 = Email.objects.get(id=email3.id)

        self.assertEqual(True, email1.send_successful)
        self.assertEqual(True, email2.send_successful)
        self.assertEqual(False, email3.send_successful)
        self.assertEqual(0, Email.objects.filter(id=email4.id).count())


    def test_create_news_letter_events_first_time(self):
        '''
        Tests that the correct news events are created
        '''
        #Flush database

        FamilyNewsLetterEvents.objects.all().delete()

        from family_tree.models import Person, Family
        family = Family()
        family.save()

        Person.objects.all().delete()

        p1 = Person.objects.create(name='Connor Macleod', gender='M',family_id=family.id)
        p1.save()
        p2 = Person.objects.create(name='The Kurgan', gender='M',family_id=family.id)
        p2.save()

        FamilyNewsLetterEvents.objects.create_news_letter_events()

        self.assertEqual(2,FamilyNewsLetterEvents.objects.count())



    def test_get_new_and_updated_people(self):
        '''
        Tests get new and updated people creates two lists correctly
        '''

        FamilyNewsLetterEvents.objects.all().delete()
        n1 = FamilyNewsLetterEvents(family_id=1, person_id=1, person_name='Mustapha Ibrahim', new_member=True )
        n1.save()

        n2 = FamilyNewsLetterEvents(family_id=1, person_id=2, person_name='Waggoner Will', new_member=True )
        n2.save()

        n3 = FamilyNewsLetterEvents(family_id=2, person_id=3, person_name='Tatterdemalion ', new_member=True )
        n3.save()


        u1 = FamilyNewsLetterEvents(family_id=1, person_id=1, person_name='Mustapha Ibrahim', new_member=False )
        u1.save()

        new_people, updated_people = Email.objects._get_new_and_updated_people(1)

        self.assertEqual(2,len(new_people))
        self.assertEqual(1,len(updated_people))



    def test_get_distinct_families_and_languages(self):
        '''
        Tests that we get the languages and families involved in the newsletters
        '''
        from family_tree.models import Family
        family = Family()
        family.save()

        from custom_user.models import User
        user = User.objects.create_user(email='fabio_testi@email.com', password='a lot of surveillance', name='Fabio Testi', language='en', family_id= family.id)
        user.save()

        user2 = User.objects.create_user(email='ron_nummi@email.com', password='a bit of surveillance', name='Ron Nummi', language='pl', family_id= family.id)
        user2.save()

        FamilyNewsLetterEvents.objects.all().delete()
        n1 = FamilyNewsLetterEvents(family_id=family.id, person_id=1, person_name='Mustapha Ibrahim', new_member=True )
        n1.save()

        rows = Email.objects._get_distinct_families_and_languages()

        self.assertEqual(2,len(rows))



    def test_create_single_language_emails(self):
        '''
        Tests that we create emails in batches for sections of families in their who share
        a first language
        '''
        from family_tree.models import Family
        family = Family()
        family.save()

        from custom_user.models import User
        User.objects.all().delete()
        user = User.objects.create_user(email='fabio_testi@email.com', password='a lot of surveillance', name='Fabio Testi', language='pl', family_id= family.id)
        user.is_confirmed = True
        user.save()

        user2 = User.objects.create_user(email='ron_nummi@email.com', password='a bit of surveillance', name='Ron Nummi', language='pl', family_id= family.id)
        user2.is_confirmed = True
        user2.save()

        Email.objects.all().delete()
        Email.objects._create_single_language_emails('pl', family.id, "subject", "content's","content's html") #use ' to check injection errors


        self.assertEqual(2,Email.objects.all().count())


    def test_create_emails(self):
        '''
        Tests that we create emails in batches for sections of families in their who share
        a first language
        '''
        from family_tree.models import Family
        family = Family()
        family.save()

        from custom_user.models import User
        User.objects.all().delete()
        user = User.objects.create_user(email='fabio_testi@email.com', password='a lot of surveillance', name='Fabio Testi', language='pl', family_id= family.id)
        user.is_confirmed = True
        user.save()

        user2 = User.objects.create_user(email='ron_nummi@email.com', password='a bit of surveillance', name='Ron Nummi', language='pl', family_id= family.id)
        user2.is_confirmed = True
        user2.save()

        FamilyNewsLetterEvents.objects.all().delete()
        n1 = FamilyNewsLetterEvents(family_id=family.id, person_id=1, person_name='Fabio Testi', new_member=True )
        n1.save()

        n2 = FamilyNewsLetterEvents(family_id=family.id, person_id=1, person_name='Ron Nummii', new_member=False )
        n2.save()

        Email.objects.all().delete()
        Email.objects._create_emails()



        self.assertEqual(2,Email.objects.all().count())


    def test_get_number_of_emails_to_send(self):
        '''
        Tests that the correct number of emails is ascertained
        '''
        #Ensure we have a clean table
        Email.objects.all().delete()

        email1 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email1.save()

        email2 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email2.save()

        email3 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email3.save()

        email4 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email4.save()

        self.assertEqual(2, Email.objects._get_number_of_emails_to_send(11))
        self.assertEqual(1, Email.objects._get_number_of_emails_to_send(1))
        self.assertEqual(4, Email.objects._get_number_of_emails_to_send(12))


    def test_get_number_of_emails_to_send_when_some_have_already_been_sent(self):
        '''
        Tests that the correct number of emails is ascertained
        '''
        #Ensure we have a clean table
        Email.objects.all().delete()

        email1 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email1.save()

        email2 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                    ,send_successful = True
                )
        email2.save()

        email3 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                )
        email3.save()

        email4 = Email(
                    recipient = 'info@okkindred.com'
                    ,subject = 'test_process_emails'
                    ,content = ' emailer.tests.py'
                    ,content_html = ' emailer.tests.py html'
                    ,send_attempts = 4
                )
        email4.save()

        self.assertEqual(1, Email.objects._get_number_of_emails_to_send(11))
        self.assertEqual(1, Email.objects._get_number_of_emails_to_send(1))
        self.assertEqual(2, Email.objects._get_number_of_emails_to_send(12))