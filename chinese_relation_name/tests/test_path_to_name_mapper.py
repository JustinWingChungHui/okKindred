# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.family import Family
from family_tree.models.person import Person
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path
from chinese_relation_name.path_to_name_mapper import get_name


class PathToNameMapperTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the Path to name mapper
    '''
    def setUp(self):
        self.family = Family()
        self.family.save()


    def test_1_relation_apart(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))

        path = Path(person, mum)
        path.add_node(mum, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Mother', result[0])


    def test_maternal_grandmother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        paternal_grandmother = Node(Person.objects.create(name='paternal_grandmother', gender='F', family_id=self.family.id))

        path = Path(person, paternal_grandmother)
        path.add_node(mum, RAISED_BY)
        path.add_node(paternal_grandmother, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Maternal Grandmother', result[0])


    def test_paternal_grandfather(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        paternal_grandfather = Node(Person.objects.create(name='paternal_grandfather', gender='M', family_id=self.family.id))

        path = Path(person, paternal_grandfather)
        path.add_node(dad, RAISED_BY)
        path.add_node(paternal_grandfather, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Paternal Grandfather', result[0])


    def test_generic_grandparent(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='parent', gender='O', family_id=self.family.id))
        grandparent = Node(Person.objects.create(name='grandparent', gender='O', family_id=self.family.id))

        path = Path(person, grandparent)
        path.add_node(parent, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)

        result = get_name(path)

        self.assertTrue('Paternal Grandfather' in result)
        self.assertTrue('Paternal Grandmother' in result)
        self.assertTrue('Maternal Grandfather' in result)
        self.assertTrue('Maternal Grandmother' in result)


    def test_stepmother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        stepmother = Node(Person.objects.create(name='stepmother', gender='F', family_id=self.family.id))

        path = Path(person, stepmother)
        path.add_node(dad, RAISED_BY)
        path.add_node(stepmother, PARTNERED)

        result = get_name(path)
        self.assertEqual('Stepmother', result[0])


    def test_father_in_law_wifes_side(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        wife = Node(Person.objects.create(name='wife', gender='F', family_id=self.family.id))
        father_in_law = Node(Person.objects.create(name='father_in_law', gender='M', family_id=self.family.id))

        path = Path(person, father_in_law)
        path.add_node(wife, PARTNERED)
        path.add_node(father_in_law, RAISED_BY)

        result = get_name(path)
        self.assertEqual("Wife's Father", result[0])

