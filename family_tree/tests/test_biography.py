# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.family import Family
from family_tree.models.person import Person

class BiographyTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for all model logic for a Biography
    '''


    def setUp(self):

        self.family = Family()
        self.family.save()

        super(BiographyTestCase, self).setUp()


    def test_biography_can_be_written_in_non_latic_characters(self):
        """
        Tests that a biography name can be written in non-latin characters
        """

        #Traditional Chinese
        person = Person(name='nonlatin', gender='M', email='nonlatin@example.com', family_id=self.family.id, biography='傳記')
        person.save()

        #Simplified Chinese
        person.biography = '传记'
        person.save()

        #Polish
        person.biography = 'zabójstwo'
        person.save()


