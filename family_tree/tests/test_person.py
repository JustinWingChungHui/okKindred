# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from custom_user.models import User
from family_tree.models.relation import Relation, RAISED, PARTNERED

class PersonTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Person
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        super(PersonTestCase, self).setUp()


    def test_create_user_with_no_email(self):
        '''
        Tests that a user is not created when a person is created with no email
        '''

        num_users = User.objects.all().count()

        person = Person.objects.create(name='John Wong', gender='M', family_id=self.family.id)
        person.create_update_user()

        self.assertEqual(num_users,User.objects.all().count())
        self.assertIsNone(person.user)


    def test_create_user_with_email(self):
        '''
        Tests that a user is created when a person is created with an email
        '''

        person = Person(name='John Wong', gender='M', email='john1.wong@example.com', family_id=self.family.id)
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(email='john1.wong@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(email='john1.wong@example.com').id)


    def test_update_user_when_email_changed(self):
        '''
        Tests that a user is updated when a person's email is modified
        '''
        person = Person(name='John Wong', gender='M', email='john.wong2@example.com', family_id=self.family.id)
        person.create_update_user()
        person.save()

        person.email = 'a_different_email@example.com'
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(email='a_different_email@example.com').count())
        self.assertEqual(0, User.objects.filter(email='john.wong2@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(email='a_different_email@example.com').id)


    def test_person_name_can_be_in_non_latic_characters(self):
        '''
        Tests that a users name can be written in non-latin characters
        '''

        #Traditional Chinese
        person = Person(name='實驗', gender='M', email='sdvbs@example.com', family_id=self.family.id)
        person.save()

        #Simplified Chinese
        person = Person(name='实验', gender='M', email='dgg@example.com', family_id=self.family.id)
        person.save()

        #Polish
        person = Person(name='kiełbasa', gender='M', email='sdvdgdsgdsgbs@example.com', family_id=self.family.id)
        person.save()


    def test_hierachy_score_set_for_adding_child(self):
        '''
        Ensure that hierachy score is set when adding the child of a parent
        the relation is not passed to the function
        '''

        parent = Person(name='parent', gender='M', hierarchy_score = 100, family_id=self.family.id)
        parent.save()

        child = Person(name='child', gender='M', family_id=self.family.id)
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

        parent = Person(name='parent', gender='M', hierarchy_score = 100, family_id=self.family.id)
        parent.save()

        child = Person(name='child', gender='M', family_id=self.family.id)
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)

        child.set_hierarchy_score(relation)
        self.assertEqual(101, child.hierarchy_score)


    def test_hierachy_score_set_for_adding_parent(self):
        '''
        Ensure that hierachy score is set when adding the parent of a child
        the relation is not passed to the function
        '''

        parent = Person(name='parent', gender='M', family_id=self.family.id)
        parent.save()

        child = Person(name='child', gender='M', hierarchy_score = 100, family_id=self.family.id)
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

        parent = Person(name='parent', gender='M', family_id=self.family.id)
        parent.save()

        child = Person(name='child', gender='M', hierarchy_score = 100, family_id=self.family.id)
        child.save()

        relation = Relation(from_person_id = parent.id, to_person_id = child.id, relation_type = RAISED)

        parent.set_hierarchy_score(relation)

        self.assertEqual(99, parent.hierarchy_score)


    def test_hierachy_score_set_for_adding_partner(self):
        '''
        Ensure that hierachy score is set when adding a partner
        '''

        husband = Person(name='husband', gender='M', family_id=self.family.id)
        husband.save()

        wife = Person(name='wife', gender='F', hierarchy_score = 75, family_id=self.family.id)
        wife.save()

        relation = Relation(from_person_id = husband.id, to_person_id = wife.id, relation_type = PARTNERED)
        relation.save()

        husband.set_hierarchy_score()

        self.assertEqual(75, husband.hierarchy_score)


    def test_get_related_data(self):
        '''
        Tests the get_related function.
        '''

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=self.family.id)
        person.save()

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=self.family.id)
        wife.save()
        wife_to_person = Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)
        wife_to_person.save()

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=self.family.id)
        son.save()
        person_to_son = Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)
        person_to_son.save()

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=self.family.id)
        daughter.save()
        person_to_daughter = Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)
        person_to_daughter.save()

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=self.family.id)
        mum.save()
        mum_to_person = Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)
        mum_to_person.save()

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=self.family.id)
        dad.save()
        dad_to_person = Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)
        dad_to_person.save()

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=self.family.id)
        grandma.save()
        grandma_to_mum = Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)
        grandma_to_mum.save()

        grandson = Person.objects.create(name='grandson', gender='M', hierarchy_score=102, family_id=self.family.id)
        grandson.save()
        son_to_grandson = Relation.objects.create(from_person=son, to_person=grandson, relation_type=RAISED)
        son_to_grandson.save()

        related_data = Person.objects.get_related_data(person)

        self.assertEqual(related_data.people_upper[0].id, mum.id)
        self.assertEqual(related_data.people_upper[1].id, dad.id)

        self.assertEqual(len(list(related_data.people_upper)), 2) #raw query sets don't have a count function


        self.assertEqual(related_data.people_same_level[0].id, wife.id)

        self.assertEqual(related_data.people_lower[0].id, daughter.id)
        self.assertEqual(related_data.people_lower[1].id, son.id)
        self.assertEqual(len(list(related_data.people_lower)), 2)

        self.assertEqual(len(list(related_data.relations)), 5)



    def test_geocode_address_UK(self):
        '''
        Tests that the correct longitude and latitude are returned for a UK location
        '''
        person = Person.objects.create(name='Kate Bush', gender='F', address='Bexleyheath, England', family_id=self.family.id)
        person.geocode_address()

        self.assertEqual(51.45, round(person.latitude,2))
        self.assertEqual(0.14, round(person.longitude,2))


    def test_geocode_address_China(self):
        '''
        Tests that the correct longitude and latitude are returned for a location in China
        '''
        person = Person.objects.create(name='Jackie Chan', gender='M', address='扯旗山 香港', family_id=self.family.id)
        person.geocode_address()

        self.assertEqual(22.28, round(person.latitude,2))
        self.assertEqual(114.14, round(person.longitude,2))


    def test_geocode_address_using_backup_UK(self):
        '''
        Tests that the correct longitude and latitude are returned for a UK address
        using the backup geocoding service
        '''
        person = Person.objects.create(name='Brian Blessed', gender='M', address='Mexborough, Yorkshire', family_id=self.family.id)
        person._geocode_address_using_backup()

        self.assertEqual(53.5, round(person.latitude,1))
        self.assertEqual(-1.3, round(person.longitude,1))


    def test_geocode_address_using_backup_China(self):
        '''
        Tests that the correct longitude and latitude are returned for a location in China
        using the backup geocoding service
        '''
        person = Person.objects.create(name='Sammo Hung', gender='M', address='星光大道 香港', family_id=self.family.id)
        person._geocode_address_using_backup()

        self.assertEqual(22.3, round(person.latitude,1))
        self.assertEqual(114.2, round(person.longitude,1))


    def test_set_hires_photo(self):
        '''
        Tests that the function correctly sets sets the photo field on a person and converts an image.
        '''
        from django.conf import settings

        #Copy test image to media area
        import shutil
        import os
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        person = Person(name='陳港生', gender='M', family_id=self.family.id)
        person.set_hires_photo('large_test_image.jpg')

        self.assertEqual('profile_photos/large_test_image.jpg', person.photo)

        #Check this image is valid
        from PIL import Image
        image = Image.open(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')
        image.verify()
        width, height = image.size

        self.assertEqual(300, width)
        self.assertEqual(206, height) #maintains aspect ratio

        self.assertEqual('profile_photos/large_test_image.jpg', person.photo)

        #Clear up mess afterwards
        os.remove(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')