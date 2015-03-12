# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from custom_user.models import User
from family_tree.models.relation import Relation, RAISED, PARTNERED, RAISED_BY
from PIL import Image

class PersonTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Person
    '''

    def setUp(self):

        self.family = Family()
        self.family.save()

        super(PersonTestCase, self).setUp()



    def test_update_user_when_email_changed(self):
        '''
        Tests that a user is updated when a person's email is modified
        '''

        user = User.objects.create(email='john.wong2@example.com', password='char sui', name='John Wong')
        person = Person(name='John Wong', gender='M', email='john.wong2@example.com', family_id=self.family.id, language='pl', user_id=user.id)
        person.save()


        person.email = 'a_different_email@example.com'
        person.create_update_user()

        self.assertEqual(1, User.objects.filter(email='a_different_email@example.com').count())
        self.assertEqual(0, User.objects.filter(email='john.wong2@example.com').count())
        self.assertEqual(person.user_id, User.objects.get(email='a_different_email@example.com').id)
        self.assertEqual(person.family_id, User.objects.get(email='a_different_email@example.com').family_id)
        self.assertEqual('pl', User.objects.get(email='a_different_email@example.com').language)


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
        self.assertEqual(114.15, round(person.longitude,2))


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
        image = Image.open(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')
        image.verify()
        width, height = image.size

        self.assertEqual(500, width)
        self.assertEqual(343, height) #maintains aspect ratio

        self.assertEqual('profile_photos/large_test_image.jpg', person.photo)

        #Clear up mess afterwards
        os.remove(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')


    def test_crop_and_resize_photo(self):
        '''
        Tests that the function correctly sets two thumbnails of correct size
        '''
        from django.conf import settings

        #Copy test image to media area
        import shutil
        import os
        shutil.copy2(os.path.join(settings.BASE_DIR, 'family_tree/tests/large_test_image.jpg'), settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')

        person = Person(name='譚詠麟', gender='M', family_id=self.family.id)
        person.photo = 'profile_photos/large_test_image.jpg'

        person.crop_and_resize_photo(50, 50, 20, 20, 800)

        #Check small thumbnail is valid
        small = Image.open(settings.MEDIA_ROOT + str(person.small_thumbnail))
        small.verify()
        width, height = small.size

        self.assertEqual(80, width)
        self.assertEqual(80, height)

        #Check large thumbnail is valid
        large = Image.open(settings.MEDIA_ROOT + str(person.large_thumbnail))
        large.verify()
        width, height = large.size

        self.assertEqual(200, width)
        self.assertEqual(200, height)


        #Clear up mess afterwards
        os.remove(settings.MEDIA_ROOT + 'profile_photos/large_test_image.jpg')




