# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, PARTNERED
from chinese_relation_name.solver import Solver


class SolverTestCase(TestCase): # pragma: no cover
    '''
    This defines all the tests for the solver class
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()

        self.person = Person.objects.create(name='patient zero', gender='M', family_id=self.family.id)

        self.wife = Person.objects.create(name='wife', gender='F', family_id=self.family.id)
        Relation.objects.create(from_person=self.wife, to_person=self.person, relation_type=PARTNERED)

        self.son = Person.objects.create(name='son', gender='M', family_id=self.family.id)
        Relation.objects.create(from_person=self.person, to_person=self.son, relation_type=RAISED)


        self.daughter = Person.objects.create(name='daughter', gender='F', family_id=self.family.id)
        Relation.objects.create(from_person=self.person, to_person=self.daughter, relation_type=RAISED)

        self.mum = Person.objects.create(name='mum', gender='F', family_id=self.family.id)
        Relation.objects.create(from_person=self.mum, to_person=self.person, relation_type=RAISED)


        self.dad = Person.objects.create(name='dad', gender='M', family_id=self.family.id)
        Relation.objects.create(from_person=self.dad, to_person=self.person, relation_type=RAISED)

        self.grandma = Person.objects.create(name='grandma', gender='F', family_id=self.family.id)
        Relation.objects.create(from_person=self.grandma, to_person=self.mum, relation_type=RAISED)

        self.grandson = Person.objects.create(name='grandson', gender='M', family_id=self.family.id)
        Relation.objects.create(from_person=self.son, to_person=self.grandson, relation_type=RAISED)


    def test_load_data(self):
        '''
        Tests load data creates correct arrays
        '''

        solver = Solver()
        solver.load_data(self.family.id)

        self.assertTrue(len(solver.nodes) > 0)


    def test_find_path(self):
        '''
        Tests finds path from one node to another
        '''

        solver = Solver()
        solver.load_data(self.family.id)

        solver.find_path(self.grandson.id, self.grandma.id)

        titles = ",".join(solver.result.titles)
        self.assertEqual("Father,Father,Mother,Mother", titles)
        self.assertEqual(-4, solver.result.generation)
        self.assertEqual(0, solver.result.age_diff)





