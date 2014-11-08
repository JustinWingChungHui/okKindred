# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from django.contrib.auth.models import User

class PersonTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Person
    '''

    def setUp(self):
        super(PersonTestCase, self).setUp()


    def test_is_valid_email(self):
        """
        test that a valid email passes, and an invalid fails
        """
        person = Person.objects.create(name='John Wong', gender='M')
        self.assertEqual(True, person.is_valid_email('adrianwas@amassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzb.us'))
        self.assertEqual(False, person.is_valid_email('adrianwasamassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzb.us'))
        self.assertEqual(False, person.is_valid_email('adrianwas@amassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzbus'))



    def test_create_user_with_no_email(self):
        """
        Tests that a user is not created when a person is created with no email
        """

        num_users = User.objects.all().count()

        person = Person.objects.create(name='John Wong', gender='M')
        person.create_update_user()

        self.assertEqual(num_users,User.objects.all().count())
        self.assertIsNone(person.user)


    def test_create_user_with_email(self):
        """
        Tests that a user is created when a person is created with an email
        """

        person = Person(name='John Wong', gender='M', email='john1.wong@example.com')
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(username='john1.wong@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(username='john1.wong@example.com').id)


    def test_update_user_when_email_changed(self):
        """
        Tests that a user is updated when a person's email is modified
        """
        person = Person(name='John Wong', gender='M', email='john.wong2@example.com')
        person.create_update_user()
        person.save()

        person.email = 'a_different_email@example.com'
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(username='a_different_email@example.com').count())
        self.assertEqual(0, User.objects.filter(username='john.wong2@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(username='a_different_email@example.com').id)


    def test_person_name_can_be_in_non_latic_characters(self):
        """
        Tests that a users name can be written in non-latin characters
        """

        #Traditional Chinese
        person = Person(name='實驗', gender='M', email='sdvbs@example.com')
        person.save()

        #Simplified Chinese
        person = Person(name='实验', gender='M', email='dgg@example.com')
        person.save()

        #Polish
        person = Person(name='kiełbasa', gender='M', email='sdvdgdsgdsgbs@example.com')
        person.save()


