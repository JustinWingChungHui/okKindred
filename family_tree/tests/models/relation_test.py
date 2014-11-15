from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.relation import Relation, RAISED, RAISED_BY, PARTNERED

class RelationTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Relation
    '''


    def setUp(self):
        super(RelationTestCase, self).setUp()


    def test_raised_by_relation_resolves_to_raised(self):
        '''
        Tests when a relation that a child is raised by parent, it resolves to parent raised child
        '''
        parent = Person(name="parent", gender="F")
        parent.save()

        child = Person(name="child", gender="O")
        child.save()

        relation = Relation(from_person_id = child.id, to_person_id = parent.id, relation_type = RAISED_BY)
        relation.normalise()


        self.assertEqual(RAISED, relation.relation_type)
        self.assertEqual(parent.id, relation.from_person_id)
        self.assertEqual(child.id, relation.to_person_id)


    def test_partnered_male_to_female_resolves_to_female_to_male(self):
        '''
        Tests when a male partners a female, it resolves to females partners a male
        '''
        male = Person(name="male", gender="M")
        male.save()

        female = Person(name="female", gender="F")
        female.save()

        relation = Relation(from_person_id = male.id, to_person_id = female.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)

        self.assertEqual(male.id, relation.to_person_id)


    def test_partnered_other_to_female_resolves_to_female_to_other(self):
        '''
        Tests when an other gender partners a female, it resolves to females partners an other gender
        '''
        other = Person(name="other", gender="O")
        other.save()

        female = Person(name="female", gender="F")
        female.save()

        relation = Relation(from_person_id = other.id, to_person_id = female.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)
        self.assertEqual(other.id, relation.to_person_id)



    def test_partnered_other_to_male_resolves_to_male_to_other(self):
        '''
        Tests when a male partners an other gender, it resolves to other partners a male
        '''

        other = Person(name="other", gender="O")
        other.save()

        male = Person(name="male", gender="M")
        male.save()

        relation = Relation(from_person_id = other.id, to_person_id = male.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(male.id, relation.from_person_id)

        self.assertEqual(other.id, relation.to_person_id)


    def test_partnered_female_to_male_stays_the_same(self):
        '''
        Tests when a female partners a male, the relationship does not change
        '''

        female = Person(name="female", gender="F")
        female.save()

        male = Person(name="male", gender="M")
        male.save()


        relation = Relation(from_person_id = female.id, to_person_id = male.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)

        self.assertEqual(male.id, relation.to_person_id)
