# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.family import Family
from family_tree.models.person import Person
from family_tree.models.relation import PARTNERED, RAISED, RAISED_BY
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path
from chinese_relation_name.path_to_name_mapper import get_name


class PathToNameMapper3rdGenTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the Path to name mapper
    '''
    def setUp(self):
        self.family = Family()
        self.family.save()



    def test_maternal_great_grandmother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        maternal_grandmother = Node(Person.objects.create(name='maternal_grandmother', gender='F', family_id=self.family.id))
        maternal_great_grandmother = Node(Person.objects.create(name='maternal_great_grandmother', gender='F', family_id=self.family.id))


        path = Path(person, maternal_great_grandmother)
        path.add_node(mum, RAISED_BY)
        path.add_node(maternal_grandmother, RAISED_BY)
        path.add_node(maternal_great_grandmother, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Maternal Great Grandmother', result[0])


    def test_paternal_great_grandfather(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        paternal_grandmother = Node(Person.objects.create(name='paternal_grandmother', gender='F', family_id=self.family.id))
        paternal_great_grandfather = Node(Person.objects.create(name='paternal_great_grandfather', gender='M', family_id=self.family.id))


        path = Path(person, paternal_great_grandfather)
        path.add_node(dad, RAISED_BY)
        path.add_node(paternal_grandmother, RAISED_BY)
        path.add_node(paternal_great_grandfather, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Paternal Great Grandfather', result[0])


    def test_great_grandfather(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='dad', gender='O', family_id=self.family.id))
        paternal_grandmother = Node(Person.objects.create(name='paternal_grandmother', gender='F', family_id=self.family.id))
        great_grandfather = Node(Person.objects.create(name='great_grandfather', gender='M', family_id=self.family.id))


        path = Path(person, great_grandfather)
        path.add_node(parent, RAISED_BY)
        path.add_node(paternal_grandmother, RAISED_BY)
        path.add_node(great_grandfather, RAISED_BY)

        result = get_name(path)

        self.assertTrue('Paternal Great Grandfather' in result)
        self.assertTrue('Maternal Great Grandfather' in result)


    def test_step_grandparent(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mother = Node(Person.objects.create(name='mother', gender='F', family_id=self.family.id))
        grandparent = Node(Person.objects.create(name='grandparent', gender='F', family_id=self.family.id))
        step_grandparent = Node(Person.objects.create(name='step_grandparent', gender='M', family_id=self.family.id))


        path = Path(person, step_grandparent)
        path.add_node(mother, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(step_grandparent, PARTNERED)

        result = get_name(path)

        self.assertEqual([], result)


    def test_mothers_elder_sister(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mother = Node(Person.objects.create(name='mother', gender='F', family_id=self.family.id, birth_year=1990))
        grandparent = Node(Person.objects.create(name='grandparent', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id, birth_year=1988))


        path = Path(person, aunt)
        path.add_node(mother, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(aunt, RAISED)

        result = get_name(path)

        self.assertTrue("Mother's Elder Sister" in result)
        self.assertTrue("Mother's Sister" in result)


    def test_fathers_younger_brother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        father = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id, birth_year=1990))
        grandparent = Node(Person.objects.create(name='grandparent', gender='F', family_id=self.family.id))
        uncle = Node(Person.objects.create(name='uncle', gender='M', family_id=self.family.id, birth_year=1991))


        path = Path(person, uncle)
        path.add_node(father, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(uncle, RAISED)

        result = get_name(path)

        self.assertTrue("Father's Younger Brother" in result)
        self.assertTrue("Father's Brother" in result)
