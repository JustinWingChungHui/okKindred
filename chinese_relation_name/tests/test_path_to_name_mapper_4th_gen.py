# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.family import Family
from family_tree.models.person import Person
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path
from chinese_relation_name.path_to_name_mapper import get_name


class PathToNameMapper4thGenTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the Path to name mapper
    '''
    def setUp(self):
        self.family = Family()
        self.family.save()



    def test_maternal_grandmothers_sister(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        great_grandmother = Node(Person.objects.create(name='great_grandmother', gender='F', family_id=self.family.id))
        great_aunt = Node(Person.objects.create(name='great_aunt', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, great_aunt)
        path.add_node(mum, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(great_grandmother, RAISED_BY)
        path.add_node(great_aunt, RAISED)

        result = get_name(path)

        self.assertEqual(1, len(result))
        self.assertEqual("Maternal Grandmother's Sister", result[0])


    def test_maternal_grandfathers_elder_brother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        grandfather = Node(Person.objects.create(name='grandfather', gender='M', family_id=self.family.id, birth_year=1950))
        great_grandmother = Node(Person.objects.create(name='great_grandmother', gender='F', family_id=self.family.id))
        great_uncle = Node(Person.objects.create(name='great_uncle', gender='M', family_id=self.family.id, birth_year=1949))

        path = Path()
        path.set_goals(person, great_uncle)
        path.add_node(mum, RAISED_BY)
        path.add_node(grandfather, RAISED_BY)
        path.add_node(great_grandmother, RAISED_BY)
        path.add_node(great_uncle, RAISED)

        result = get_name(path)

        self.assertEqual(1, len(result))
        self.assertEqual("Maternal Grandfather's Elder Brother", result[0])


    def test_paternal_grandfathers_younger_brothers_wife(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        grandfather = Node(Person.objects.create(name='grandfather', gender='M', family_id=self.family.id, birth_year=1950))
        great_grandmother = Node(Person.objects.create(name='great_grandmother', gender='F', family_id=self.family.id))
        great_uncle = Node(Person.objects.create(name='great_uncle', gender='M', family_id=self.family.id, birth_year=1951))
        great_aunt = Node(Person.objects.create(name='great_aunt', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, great_aunt)
        path.add_node(dad, RAISED_BY)
        path.add_node(grandfather, RAISED_BY)
        path.add_node(great_grandmother, RAISED_BY)
        path.add_node(great_uncle, RAISED)
        path.add_node(great_aunt, PARTNERED)

        result = get_name(path)

        self.assertEqual(1, len(result))
        self.assertEqual("Paternal Grandfather's Younger Brother's Wife", result[0])


    def test_unknownlineage_grandparents_siblings_partner(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='parent', gender='O', family_id=self.family.id))
        grandparent = Node(Person.objects.create(name='grandparent', gender='O', family_id=self.family.id))
        great_grandparent = Node(Person.objects.create(name='great_grandparent', gender='O', family_id=self.family.id))
        grandparents_sibling = Node(Person.objects.create(name='grandparent_sibling', gender='O', family_id=self.family.id))
        grandparents_siblings_partner = Node(Person.objects.create(name='grandparents_siblings_partner', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, grandparents_siblings_partner)
        path.add_node(parent, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(great_grandparent, RAISED_BY)
        path.add_node(grandparents_sibling, RAISED)
        path.add_node(grandparents_siblings_partner, PARTNERED)

        result = get_name(path)

        self.assertEqual(10, len(result))
        self.assertTrue("Paternal Grandfather's Younger Brother's Wife" in result)
        self.assertTrue("Paternal Grandfather's Elder Brother's Wife" in result)
        self.assertTrue("Maternal Grandmother's Sister's Husband" in result)