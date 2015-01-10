# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.family import Family
from family_tree.models.person import Person
from family_tree.models.biography import Biography

class BiographyTestCase(TestCase):
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

        person = Person(name='nonlatin', gender='M', email='nonlatin@example.com', family_id=self.family.id)
        person.save()

        #Traditional Chinese
        traditional_chinese = Biography(person_id = person.id, language = 'zh-hk', content='傳記')
        traditional_chinese.save()


        #Simplified Chinese
        simplified_chinese = Biography(person_id = person.id, language = 'zh-cn', content='传记')
        simplified_chinese.save()

        #Polish
        polish = Biography(person_id = person.id, language = 'pl', content='zabójstwo')
        polish.save()


    def test_get_biography(self):
        '''
        Tests get_biography
        '''
        person = Person(name='test_get_biography', gender='M', email='test_get_biography@example.com', family_id=self.family.id)
        person.save()

        english = Biography(person_id = person.id, language = 'en', content='biography in english')
        english.save()

        polish = Biography(person_id = person.id, language = 'pl', content='biography in polish')
        polish.save()

        simplified_chinese = Biography(person_id = person.id, language = 'zh-cn', content='biography in simplified chinese')
        simplified_chinese.save()

        #Test when requested language passed in
        biog = Biography.objects.get_biography(person_id = person.id, requested_language = 'pl')
        self.assertEqual(polish.id, biog.id)

        #Test when default language passed in and no requested language
        biog = Biography.objects.get_biography(person_id = person.id, default_language = 'zh-cn')
        self.assertEqual(simplified_chinese.id, biog.id)

        #Test when requested language specified but biography does not exist
        biog = Biography.objects.get_biography(person_id = person.id, requested_language = 'zh-hk')
        self.assertEqual(None, biog)

        #Test when default language exists
        biog = Biography.objects.get_biography(person_id = person.id, default_language = 'zh-cn')
        self.assertEqual(simplified_chinese.id, biog.id)

        #Test english returned when default language does not exist
        biog = Biography.objects.get_biography(person_id = person.id, default_language = 'zh-hk')
        self.assertEqual(english.id, biog.id)


    def test_get_biography_no_requested_no_default_no_english(self):
        '''
        Tests get_biography when no default, requested or english language exists, function returns whatever it can
        '''
        person = Person(name='no_requested_no_default_no_english', gender='M', email='test_get_biography_no_requested_no_default_no_english@example.com', family_id=self.family.id)
        person.save()

        polish = Biography(person_id = person.id, language = 'pl', content='biography in polish')
        polish.save()

        biog = Biography.objects.get_biography(person_id = person.id, default_language = 'zh-hk')
        self.assertEqual(polish.id, biog.id)

    def test_get_biography_no_biographies_at_all(self):
        '''
        Tests get_biography when no biographies exist at all
        '''
        person = Person(name='test_get_biography_no_biographies_at_all', gender='M', email='test_get_biography_no_biographies_at_all@example.com', family_id=self.family.id)
        person.save()

        biog = Biography.objects.get_biography(person_id = person.id, requested_language = 'zh-hk', default_language = 'zh-hk')
        self.assertEqual(None, biog)

