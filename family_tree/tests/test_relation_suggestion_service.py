from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, PARTNERED, RAISED_BY
from family_tree.services import relation_suggestion_service


class TreeRelationSuggestionService(TestCase):
    '''
    This defines all the tests for the relation suggestion service
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()


    def test_suggests_partner_of_parent(self):
        '''
        Tests service suggests that darth vader is the father of luke skywalker
        given that padme and darth were partnered and padme is lukes mother
        '''
        luke = Person.objects.create(name='luke skywalker', gender='M', family_id=self.family.id)
        darth = Person.objects.create(name='darth vader', gender='M', family_id=self.family.id)
        padme = Person.objects.create(name='padmé amidala', gender='F', family_id=self.family.id)

        Relation.objects.create(from_person=padme, to_person=darth, relation_type=PARTNERED)
        Relation.objects.create(from_person=padme, to_person=luke, relation_type=RAISED)

        suggestions = relation_suggestion_service.get_relation_suggestions(luke)

        #I am your father
        self.assertEqual(luke.id, suggestions[0].from_person_id)
        self.assertEqual(darth.id, suggestions[0].to_person_id)

        #NOOOO!
        self.assertEqual(RAISED_BY, suggestions[0].relation_type)

        suggested_relation, suggested_person = relation_suggestion_service.get_first_relation_suggestion(luke)
        self.assertEqual('darth vader', suggested_person.name)
        self.assertEqual(RAISED_BY, suggested_relation.relation_type)



    def test_suggests_child_of_partner(self):
        '''
        Tests service suggests that leia organa is the child of darth vader
        given that padme and darth were partnered and padme raise leia
        '''
        darth = Person.objects.create(name='darth vader', gender='M', family_id=self.family.id)
        padme = Person.objects.create(name='padmé amidala', gender='F', family_id=self.family.id)
        leia = Person.objects.create(name='leia organa', gender='F', family_id=self.family.id)

        Relation.objects.create(from_person=padme, to_person=darth, relation_type=PARTNERED)
        Relation.objects.create(from_person=padme, to_person=leia, relation_type=RAISED)

        suggestions = relation_suggestion_service.get_relation_suggestions(darth)

        #He is our last hope
        #No there is another
        self.assertEqual(darth.id, suggestions[0].from_person_id)
        self.assertEqual(leia.id, suggestions[0].to_person_id)
        self.assertEqual(RAISED, suggestions[0].relation_type)


    def test_suggests_parent_of_son(self):
        '''
        Tests service suggests that padmé amidala and darth were partners
        give both raise luke skywalker
        '''
        darth = Person.objects.create(name='darth vader', gender='M', family_id=self.family.id)
        padme = Person.objects.create(name='padmé amidala', gender='F', family_id=self.family.id)
        luke = Person.objects.create(name='luke skywalker', gender='F', family_id=self.family.id)

        Relation.objects.create(from_person=darth, to_person=luke, relation_type=RAISED)
        Relation.objects.create(from_person=padme, to_person=luke, relation_type=RAISED)

        suggestions = relation_suggestion_service.get_relation_suggestions(darth)

        #Where is Padmé?
        #You killed her.
        #NOOOO!
        self.assertEqual(darth.id, suggestions[0].from_person_id)
        self.assertEqual(padme.id, suggestions[0].to_person_id)
        self.assertEqual(PARTNERED, suggestions[0].relation_type)

    def test_does_not_suggest_existing_relations(self):
        '''
        Tests service does not suggest existing relations
        '''
        darth = Person.objects.create(name='darth vader', gender='M', family_id=self.family.id)
        padme = Person.objects.create(name='padmé amidala', gender='F', family_id=self.family.id)
        luke = Person.objects.create(name='luke skywalker', gender='F', family_id=self.family.id)
        leia = Person.objects.create(name='leia organa', gender='F', family_id=self.family.id)

        Relation.objects.create(from_person=darth, to_person=luke, relation_type=RAISED)
        Relation.objects.create(from_person=padme, to_person=darth, relation_type=RAISED)
        Relation.objects.create(from_person=padme, to_person=luke, relation_type=RAISED)
        Relation.objects.create(from_person=padme, to_person=leia, relation_type=RAISED)
        Relation.objects.create(from_person=darth, to_person=luke, relation_type=RAISED)
        Relation.objects.create(from_person=darth, to_person=leia, relation_type=RAISED)

        suggestions = relation_suggestion_service.get_relation_suggestions(darth)

        self.assertEqual(0, len(suggestions))
