# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, PARTNERED, RAISED_BY
from chinese_relation_name.path import Path
from chinese_relation_name.node import Node


class PathTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the solver class
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()

        self.daughter = Node(Person.objects.create(name='daughter', gender='F', family_id=self.family.id))
        self.person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        self.mum = Node(Person.objects.create(name='mum', gender='F', family_id=self.family.id))
        self.dad = Node(Person.objects.create(name='dad', gender='M', family_id=self.family.id))
        self.grandma = Node(Person.objects.create(name='grandma', gender='F', family_id=self.family.id))
        self.grandpa = Node(Person.objects.create(name='grandpa', gender='M', family_id=self.family.id))
        self.great_grandma = Node(Person.objects.create(name='great grandma', gender='F', family_id=self.family.id))

        self.daughter.relations.append((RAISED_BY, self.person))
        self.person.relations.append((RAISED, self.daughter))

        self.person.relations.append((RAISED_BY, self.mum))
        self.mum.relations.append((RAISED, self.person))
        self.mum.relations.append((RAISED_BY, self.grandma))
        self.mum.relations.append((RAISED_BY, self.grandpa))

        self.person.relations.append((RAISED_BY, self.dad))
        self.dad.relations.append((RAISED, self.person))

        self.grandma.relations.append((RAISED, self.mum))
        self.grandma.relations.append((PARTNERED, self.grandpa))

        self.grandpa.relations.append((PARTNERED, self.grandma))
        self.grandpa.relations.append((RAISED, self.mum))

        self.grandma.relations.append((RAISED_BY, self.great_grandma))
        self.great_grandma.relations.append((RAISED, self.grandma))


    def test_add_nodes_and_duplicate(self):

        path = Path()
        path.set_goals(self.person, self.grandma)
        path.add_node(self.mum, RAISED_BY)

        self.assertEqual(1, len(path.steps))
        self.assertEqual(2, len(path.nodes))

        path.add_node(self.grandma, RAISED_BY)

        self.assertEqual(2, len(path.steps))
        self.assertEqual(3, len(path.nodes))
        self.assertTrue(path.success)

        duplicate = path.duplicate()
        path.add_node(self.grandpa, PARTNERED)

        self.assertEqual(2, len(duplicate.steps))
        self.assertEqual(3, len(duplicate.nodes))
        self.assertTrue(duplicate.success)


    def test_create_next_level_paths(self):
        path = Path()
        path.set_goals(self.person, self.great_grandma)
        path.add_node(self.mum, RAISED_BY)

        new_paths = path.create_next_level_paths()
        self.assertEqual(2, len(new_paths))
        self.assertEqual(2, len(new_paths[0].steps))
        self.assertEqual(2, len(new_paths[1].steps))


    def test_step_title_mother(self):
        path = Path()
        path.set_goals(self.person, self.mum)
        path.add_node(self.mum, RAISED_BY)

        self.assertEqual("Mother", path.steps[0].step_title())


    def test_step_title_father(self):
        path = Path()
        path.set_goals(self.person, self.dad)
        path.add_node(self.dad, RAISED_BY)

        self.assertEqual("Father", path.steps[0].step_title())


    def test_step_title_husband(self):
        path = Path()
        path.set_goals(self.grandma, self.grandpa)
        path.add_node(self.grandpa, PARTNERED)

        self.assertEqual("Husband", path.steps[0].step_title())

    def test_step_title_wife(self):
        path = Path()
        path.set_goals(self.grandpa, self.grandma)
        path.add_node(self.grandma, PARTNERED)

        self.assertEqual("Wife", path.steps[0].step_title())


    def test_step_title_son(self):
        path = Path()
        path.set_goals(self.mum, self.person)
        path.add_node(self.person, RAISED)

        self.assertEqual("Son", path.steps[0].step_title())

    def test_step_title_daughter(self):
        path = Path()
        path.set_goals(self.person, self.daughter)
        path.add_node(self.daughter, RAISED)

        self.assertEqual("Daughter", path.steps[0].step_title())