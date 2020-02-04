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

        path = Path()
        path.set_goals(person, mum)
        path.add_node(mum, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Mother', result[0])


    def test_maternal_grandmother(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        paternal_grandmother = Node(Person.objects.create(name='paternal_grandmother', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, paternal_grandmother)
        path.add_node(mum, RAISED_BY)
        path.add_node(paternal_grandmother, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Maternal Grandmother', result[0])


    def test_paternal_grandfather(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        paternal_grandfather = Node(Person.objects.create(name='paternal_grandfather', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, paternal_grandfather)
        path.add_node(dad, RAISED_BY)
        path.add_node(paternal_grandfather, RAISED_BY)

        result = get_name(path)

        self.assertEqual('Paternal Grandfather', result[0])


    def test_generic_grandparent(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='parent', gender='O', family_id=self.family.id))
        grandparent = Node(Person.objects.create(name='grandparent', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, grandparent)
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

        path = Path()
        path.set_goals(person, stepmother)
        path.add_node(dad, RAISED_BY)
        path.add_node(stepmother, PARTNERED)

        result = get_name(path)
        self.assertEqual('Stepmother', result[0])


    def test_father_in_law_wifes_side(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        wife = Node(Person.objects.create(name='wife', gender='F', family_id=self.family.id))
        father_in_law = Node(Person.objects.create(name='father_in_law', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, father_in_law)
        path.add_node(wife, PARTNERED)
        path.add_node(father_in_law, RAISED_BY)

        result = get_name(path)
        self.assertEqual("Wife's Father", result[0])

    def test_elder_sister(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=1982))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        sister = Node(Person.objects.create(name='sister', gender='F', family_id=self.family.id, birth_year=1980))

        path = Path()
        path.set_goals(person, sister)
        path.add_node(dad, RAISED_BY)
        path.add_node(sister, RAISED)

        result = get_name(path)

        self.assertEqual("Elder Sister", result[0])

    def test_brother_unknown_age(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=1982))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        brother = Node(Person.objects.create(name='brother', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, brother)
        path.add_node(dad, RAISED_BY)
        path.add_node(brother, RAISED)

        result = get_name(path)

        self.assertTrue("Elder Brother" in result)
        self.assertTrue("Younger Brother" in result)


    def test_younger_sibling(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=1982))
        dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        sibling = Node(Person.objects.create(name='sibling', gender='O', family_id=self.family.id, birth_year=1990))

        path = Path()
        path.set_goals(person, sibling)
        path.add_node(dad, RAISED_BY)
        path.add_node(sibling, RAISED)

        result = get_name(path)

        self.assertTrue("Younger Brother" in result)
        self.assertTrue("Younger Sister" in result)

    def test_stepson(self):
        person = Node(Person.objects.create(name='patient zero', gender='F', family_id=self.family.id))
        partner = Node(Person.objects.create(name='partner', gender='F', family_id=self.family.id))
        stepson = Node(Person.objects.create(name='stepson', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, stepson)
        path.add_node(partner, PARTNERED)
        path.add_node(stepson, RAISED)

        result = get_name(path)

        self.assertTrue("Stepson" in result)

    def test_daughter_in_law(self):
        person = Node(Person.objects.create(name='patient zero', gender='F', family_id=self.family.id))
        son = Node(Person.objects.create(name='son', gender='M', family_id=self.family.id))
        daughter_in_law = Node(Person.objects.create(name='daughter in law', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, daughter_in_law)
        path.add_node(son, RAISED)
        path.add_node(daughter_in_law, PARTNERED)

        result = get_name(path)

        self.assertTrue("Daughter In Law" in result)


    def test_grandson_daughters_side(self):
        person = Node(Person.objects.create(name='patient zero', gender='F', family_id=self.family.id))
        daughter = Node(Person.objects.create(name='daughter', gender='F', family_id=self.family.id))
        grandson = Node(Person.objects.create(name='grandson', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, grandson)
        path.add_node(daughter, RAISED)
        path.add_node(grandson, RAISED)

        result = get_name(path)

        self.assertTrue("Grandson Daughter's Side" in result)


    def test_granddaughter_unknown_side(self):
        person = Node(Person.objects.create(name='patient zero', gender='F', family_id=self.family.id))
        child = Node(Person.objects.create(name='child', gender='O', family_id=self.family.id))
        granddaughter = Node(Person.objects.create(name='granddaughter', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, granddaughter)
        path.add_node(child, RAISED)
        path.add_node(granddaughter, RAISED)

        result = get_name(path)

        self.assertTrue("Granddaughter Daughter's Side" in result)
        self.assertTrue("Granddaughter Son's Side" in result)
