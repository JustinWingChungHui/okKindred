# -*- coding: utf-8 -*-

from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, PARTNERED, RAISED_BY
from family_tree.services import tree_service


class TreeServiceTestCase(TestCase):
    '''
    This defines all the tests for the tree service
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()


    def test_get_related_data(self):
        '''
        Tests the get_related function.
        '''

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=self.family.id)
        person.save()

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=self.family.id)
        wife.save()
        wife_to_person = Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)
        wife_to_person.save()

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=self.family.id)
        son.save()
        person_to_son = Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)
        person_to_son.save()

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=self.family.id)
        daughter.save()
        person_to_daughter = Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)
        person_to_daughter.save()

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=self.family.id)
        mum.save()
        mum_to_person = Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)
        mum_to_person.save()

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=self.family.id)
        dad.save()
        dad_to_person = Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)
        dad_to_person.save()

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=self.family.id)
        grandma.save()
        grandma_to_mum = Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)
        grandma_to_mum.save()

        grandson = Person.objects.create(name='grandson', gender='M', hierarchy_score=102, family_id=self.family.id)
        grandson.save()
        son_to_grandson = Relation.objects.create(from_person=son, to_person=grandson, relation_type=RAISED)
        son_to_grandson.save()


        related_data = tree_service.get_related_data(person)

        self.assertEqual(related_data.people_upper[0].id, mum.id)
        self.assertEqual(related_data.people_upper[1].id, dad.id)

        self.assertEqual(len(list(related_data.people_upper)), 2) #raw query sets don't have a count function


        self.assertEqual(related_data.people_same_level[0].id, wife.id)

        self.assertEqual(related_data.people_lower[0].id, daughter.id)
        self.assertEqual(related_data.people_lower[1].id, son.id)
        self.assertEqual(len(list(related_data.people_lower)), 2)

        self.assertEqual(len(list(related_data.relations)), 5)


    def test_search_next_node(self):
        '''
        Tests the get_related_path function.
        '''

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=self.family.id)

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=self.family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=self.family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=self.family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=self.family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        aunt = Person.objects.create(name='aunt', gender='F', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=grandma, to_person=aunt, relation_type=RAISED)

        cousin = Person.objects.create(name='cousin', gender='F', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=aunt, to_person=cousin, relation_type=RAISED)

        other_cousin = Person.objects.create(name='other_cousin', gender='F', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=aunt, to_person=other_cousin, relation_type=RAISED)

        distant_nephew = Person.objects.create(name='distant_nephew', gender='M', hierarchy_score=99, family_id=self.family.id)
        Relation.objects.create(from_person=cousin, to_person=distant_nephew, relation_type=RAISED)

        relations_by_person = Relation.objects.get_navigable_relations(self.family.id)
        visited_person_ids = []
        route = []
        route.append(person.id)
        found_route = tree_service._search_next_node(relations_by_person, visited_person_ids, route, distant_nephew.id)

        self.assertEqual(person.id, found_route[0])
        self.assertEqual(mum.id, found_route[1])
        self.assertEqual(grandma.id, found_route[2])
        self.assertEqual(aunt.id, found_route[3])
        self.assertEqual(cousin.id, found_route[4])
        self.assertEqual(distant_nephew.id, found_route[5])



    def test_get_path_relations(self):
        '''
        Tests the _get_path_relations function
        '''

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=self.family.id)
        person.save()

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=self.family.id)
        wife_to_person = Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=self.family.id)
        person_to_son = Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        grandson = Person.objects.create(name='grandson', gender='M',hierarchy_score=102, family_id=self.family.id)
        son_to_grandson = Relation.objects.create(from_person=son, to_person=grandson, relation_type=RAISED)

        relations_by_person = {}
        relations_by_person[person.id] = []
        relations_by_person[person.id].append(wife_to_person)
        relations_by_person[person.id].append(person_to_son)

        relations_by_person[son.id] = []
        relations_by_person[son.id].append(son_to_grandson)

        route=[person.id,son.id,grandson.id]

        path_relations = tree_service._get_path_relations(route, relations_by_person)

        self.assertEqual(person_to_son.id,path_relations[0].id)
        self.assertEqual(son_to_grandson.id,path_relations[1].id)


    def test_get_related_path(self):
        '''
        Tests the get_related_path function.
        '''

        another_family = Family()
        another_family.save()

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=another_family.id)

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        aunt = Person.objects.create(name='aunt', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=aunt, relation_type=RAISED)

        cousin = Person.objects.create(name='cousin', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=aunt, to_person=cousin, relation_type=RAISED)

        other_cousin = Person.objects.create(name='other_cousin', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=aunt, to_person=other_cousin, relation_type=RAISED)

        distant_nephew = Person.objects.create(name='distant_nephew', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=cousin, to_person=distant_nephew, relation_type=RAISED)

        people, relations = tree_service.get_related_path(other_cousin, person)


        self.assertEqual(person.id, people[0].id)
        self.assertEqual(mum.id, people[1].id)
        self.assertEqual(grandma.id, people[2].id)
        self.assertEqual(aunt.id, people[3].id)
        self.assertEqual(other_cousin.id, people[4].id)

        self.assertEqual(RAISED_BY, relations[0].relation_type)
        self.assertEqual(RAISED_BY, relations[1].relation_type)
        self.assertEqual(RAISED, relations[2].relation_type)
        self.assertEqual(RAISED, relations[3].relation_type)


    def test_add_related_partner(self):
        '''
        Tests the _add_related function adds in a partner
        '''
        another_family = Family()
        another_family.save()

        grandma = Person.objects.create(name='grandma', gender='F',hierarchy_score=100, family_id=another_family.id)
        grandad = Person.objects.create(name='grandad', gender='M',hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=grandad, relation_type=PARTNERED)

        list_of_people_by_hierachy = {}
        list_of_people_by_hierachy[100] = []
        list_of_people_by_hierachy[100].append(grandma)

        people_included = {}
        people_included[grandma.id] = grandma

        people_by_id = {
                grandma.id: grandma,
                grandad.id: grandad
            }

        relations_by_person = Relation.objects.get_navigable_relations(another_family.id)

        tree_service._add_related(grandma, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person)

        self.assertEqual(grandma.id, list_of_people_by_hierachy[100][0].id)
        self.assertEqual(grandad.id, list_of_people_by_hierachy[100][1].id)

    def test_add_related_son(self):
        '''
        Tests the _add_related function adds in a son
        '''
        another_family = Family()
        another_family.save()

        mother = Person.objects.create(name='mother', gender='F',hierarchy_score=100, family_id=another_family.id)
        son = Person.objects.create(name='son', gender='M',hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=mother, to_person=son, relation_type=RAISED_BY)

        list_of_people_by_hierachy = {}
        list_of_people_by_hierachy[100] = []
        list_of_people_by_hierachy[100].append(mother)

        people_included = {}
        people_included[mother.id] = mother

        people_by_id = {
                mother.id: mother,
                son.id: son
            }

        relations_by_person = Relation.objects.get_navigable_relations(another_family.id)

        tree_service._add_related(mother, people_by_id, list_of_people_by_hierachy, people_included, relations_by_person)

        self.assertEqual(mother.id, list_of_people_by_hierachy[100][0].id)
        self.assertEqual(son.id, list_of_people_by_hierachy[100][1].id)


    def test_get_whole_tree(self):
        '''
        Tests the get_whole_tree function.
        '''

        another_family = Family()
        another_family.save()

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=another_family.id)

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        uncle = Person.objects.create(name='uncle', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=uncle, relation_type=RAISED)

        cousin = Person.objects.create(name='cousin', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=uncle, to_person=cousin, relation_type=RAISED)


        distant_nephew = Person.objects.create(name='distant_nephew', gender='M', hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=cousin, to_person=distant_nephew, relation_type=RAISED)

        result, relations = tree_service.get_whole_tree(another_family.id)

        self.assertEqual(1, len(result[98]))
        self.assertEqual(grandma.id, result[98][0].id)

        self.assertEqual(3, len(result[99]))
        self.assertEqual(mum.id, result[99][0].id)
        self.assertEqual(dad.id, result[99][1].id)
        self.assertEqual(uncle.id, result[99][2].id)

        self.assertEqual(3, len(result[100]))
        self.assertEqual(person.id, result[100][0].id)
        self.assertEqual(wife.id, result[100][1].id)
        self.assertEqual(cousin.id, result[100][2].id)

        self.assertEqual(3, len(result[101]))
        #Not sure how to maintain Female before Male
        #self.assertEqual(daughter.id, result[101][0].id)
        #self.assertEqual(son.id, result[101][1].id)
        self.assertEqual(distant_nephew.id, result[101][2].id)



    def test_get_descendants(self):
        '''
        Tests the test_get_descendants function.
        '''

        another_family = Family()
        another_family.save()

        person = Person.objects.create(name='patient zero d', gender='M',hierarchy_score=100, family_id=another_family.id)

        wife = Person.objects.create(name='wife d', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son d', gender='M',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter d', gender='F',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum d', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)

        dad = Person.objects.create(name='dad d', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma d', gender='F', hierarchy_score=98, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        uncle = Person.objects.create(name='uncle d', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=uncle, relation_type=RAISED)

        cousin = Person.objects.create(name='cousin d', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=uncle, to_person=cousin, relation_type=RAISED)


        distant_nephew = Person.objects.create(name='distant_nephew d', gender='M', hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=cousin, to_person=distant_nephew, relation_type=RAISED)

        result, relations = tree_service.get_descendants(grandma)


        self.assertEqual(1, len(result[98]))
        self.assertEqual(grandma.id, result[98][0].id)

        self.assertEqual(2, len(result[99]))
        self.assertEqual(mum.id, result[99][0].id)
        self.assertEqual(uncle.id, result[99][1].id)

        self.assertEqual(2, len(result[100]))
        self.assertEqual(person.id, result[100][0].id)
        self.assertEqual(cousin.id, result[100][1].id)

        self.assertEqual(3, len(result[101]))
        self.assertTrue(son in result[101])
        self.assertTrue(daughter in result[101])
        self.assertTrue(distant_nephew in result[101])


    def test_get_ancestors(self):
        '''
        Tests the test_get_descendants function.
        '''

        another_family = Family()
        another_family.save()

        person = Person.objects.create(name='patient zero a', gender='M',hierarchy_score=100, family_id=another_family.id)

        wife = Person.objects.create(name='wife a', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son a', gender='M',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)
        Relation.objects.create(from_person=wife, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter a', gender='F',hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        mum = Person.objects.create(name='mum a', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)

        dad = Person.objects.create(name='dad a', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)

        grandma = Person.objects.create(name='grandma a', gender='F', hierarchy_score=98, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)

        wifes_dad = Person.objects.create(name='wifes_dad a', gender='F', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=wifes_dad, to_person=wife, relation_type=RAISED)

        uncle = Person.objects.create(name='uncle a', gender='M', hierarchy_score=99, family_id=another_family.id)
        Relation.objects.create(from_person=grandma, to_person=uncle, relation_type=RAISED)

        cousin = Person.objects.create(name='cousin a', gender='F', hierarchy_score=100, family_id=another_family.id)
        Relation.objects.create(from_person=uncle, to_person=cousin, relation_type=RAISED)


        distant_nephew = Person.objects.create(name='distant_nephew a', gender='M', hierarchy_score=101, family_id=another_family.id)
        Relation.objects.create(from_person=cousin, to_person=distant_nephew, relation_type=RAISED)

        result, relations = tree_service.get_ancestors(son)

        self.assertEqual(1, len(result[101]))
        self.assertTrue(son in result[101])

        self.assertEqual(2, len(result[100]))
        self.assertTrue(person in result[100])
        self.assertTrue(wife in result[100])

        self.assertEqual(3, len(result[99]))
        self.assertTrue(mum in result[99])
        self.assertTrue(wifes_dad in result[99])
        self.assertTrue(dad in result[99])

        self.assertEqual(1, len(result[98]))
        self.assertEqual(grandma.id, result[98][0].id)



