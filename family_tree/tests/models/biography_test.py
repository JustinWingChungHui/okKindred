# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.biography import Biography

class BiographyTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Biography
    '''


    def setUp(self):

        self.person = Person(name='test', gender='M', email='biogrphytests@example.com')
        self.person.save()

        super(BiographyTestCase, self).setUp()


    def test_biography_can_be_written_in_non_latic_characters(self):
        """
        Tests that a biography name can be written in non-latin characters
        """


        #Traditional Chinese
        traditional_chinese = Biography(person_id = self.person.id, language = 'zh-hk', content='傳記')
        traditional_chinese.save()


        #Simplified Chinese
        simplified_chinese = Biography(person_id = self.person.id, language = 'zh-cn', content='传记')
        simplified_chinese.save()

        #Polish
        polish = Biography(person_id = self.person.id, language = 'pl', content='zabójstwo')
        polish.save()


