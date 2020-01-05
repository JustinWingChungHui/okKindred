# -*- coding: utf-8 -*-

from django.test import TestCase
from chinese_relation_name.relation_name_dictionary import relation_names


class RelationNameTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the RelationName class
    '''

    def test_equal_number_of_translations(self):
        for key in relation_names:

            relation_name = relation_names[key]

            self.assertEqual(len(relation_name.cantonese),
                            len(relation_name.cantonese_pronounciation),
                            msg="{0} Error with Cantonese".format(key))

            self.assertEqual(len(relation_name.mandarin),
                            len(relation_name.mandarin_pronounciation),
                            msg="{0} Error with Mandarin".format(key))







