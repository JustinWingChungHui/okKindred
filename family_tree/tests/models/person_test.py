# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from django.contrib.auth.models import User
from family_tree.models.relation import Relation, RAISED, PARTNERED

class PersonTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Person
    '''

    def setUp(self):
        super(PersonTestCase, self).setUp()


    def test_is_valid_email(self):
        '''
        test that a valid email passes, and an invalid fails
        '''
        person = Person.objects.create(name='John Wong', gender='M')
        self.assertEqual(True, person.is_valid_email('adrianwas@amassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzb.us'))
        self.assertEqual(False, person.is_valid_email('adrianwasamassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzb.us'))
        self.assertEqual(False, person.is_valid_email('adrianwas@amassivegayorgyandcollectedsomuchjizzhehastocarryitinajizzbus'))



    def test_create_user_with_no_email(self):
        '''
        Tests that a user is not created when a person is created with no email
        '''

        num_users = User.objects.all().count()

        person = Person.objects.create(name='John Wong', gender='M')
        person.create_update_user()

        self.assertEqual(num_users,User.objects.all().count())
        self.assertIsNone(person.user)


    def test_create_user_with_email(self):
        '''
        Tests that a user is created when a person is created with an email
        '''

        person = Person(name='John Wong', gender='M', email='john1.wong@example.com')
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(username='john1.wong@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(username='john1.wong@example.com').id)


    def test_update_user_when_email_changed(self):
        '''
        Tests that a user is updated when a person's email is modified
        '''
        person = Person(name='John Wong', gender='M', email='john.wong2@example.com')
        person.create_update_user()
        person.save()

        person.email = 'a_different_email@example.com'
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(username='a_different_email@example.com').count())
        self.assertEqual(0, User.objects.filter(username='john.wong2@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(username='a_different_email@example.com').id)


    def test_person_name_can_be_in_non_latic_characters(self):
        '''
        Tests that a users name can be written in non-latin characters
        '''

        #Traditional Chinese
        person = Person(name='實驗', gender='M', email='sdvbs@example.com')
        person.save()

        #Simplified Chinese
        person = Person(name='实验', gender='M', email='dgg@example.com')
        person.save()

        #Polish
        person = Person(name='kiełbasa', gender='M', email='sdvdgdsgdsgbs@example.com')
        person.save()


    def test_hierachy_score_set_for_adding_child(self):
        '''
        Ensure that hierachy score is set when adding the child of a parent
        the relation is not passed to the function
        '''

        parent = Person(name='parent', gender='M', hierarchy_score = 100)
        parent.save()

        child = Person(name='child', gender='M')
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)
        relation.save()

        child.set_hierarchy_score()
        self.assertEqual(101, child.hierarchy_score)


    def test_hierachy_score_set_for_adding_child_with_relation_as_param(self):
        '''
        Ensure that hierachy score is set when adding the child of a parent
        the relation is passed to the function
        '''

        parent = Person(name='parent', gender='M', hierarchy_score = 100)
        parent.save()

        child = Person(name='child', gender='M')
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)

        child.set_hierarchy_score(relation)
        self.assertEqual(101, child.hierarchy_score)


    def test_hierachy_score_set_for_adding_parent(self):
        '''
        Ensure that hierachy score is set when adding the parent of a child
        the relation is not passed to the function
        '''

        parent = Person(name='parent', gender='M')
        parent.save()

        child = Person(name='child', gender='M', hierarchy_score = 100)
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)
        relation.save()

        parent.set_hierarchy_score()

        self.assertEqual(99, parent.hierarchy_score)


    def test_hierachy_score_set_for_adding_parent_with_relation_as_param(self):
        '''
        Ensure that hierachy score is set when adding the parent of a child
        the relation is passed to the function
        '''

        parent = Person(name='parent', gender='M')
        parent.save()

        child = Person(name='child', gender='M', hierarchy_score = 100)
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)

        parent.set_hierarchy_score(relation)

        self.assertEqual(99, parent.hierarchy_score)


    def test_hierachy_score_set_for_adding_partner(self):
        '''
        Ensure that hierachy score is set when adding a partner
        '''

        husband = Person(name='husband', gender='M')
        husband.save()

        wife = Person(name='wife', gender='F', hierarchy_score = 75)
        wife.save()

        relation = Relation(from_person_id = husband.id, to_person_id = wife.id, relation_type = PARTNERED)
        relation.save()

        husband.set_hierarchy_score()

        self.assertEqual(75, husband.hierarchy_score)