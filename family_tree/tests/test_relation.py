from django.test import TestCase
from family_tree.models.person import Person
from family_tree.models.family import Family
from family_tree.models.relation import Relation, RAISED, RAISED_BY, PARTNERED

class RelationTestCase(TestCase):
    '''
    This defines all the tests for all model logic for a Relation
    '''


    def setUp(self):

        self.family = Family()
        self.family.save()

        super(RelationTestCase, self).setUp()


    def test_raised_by_relation_resolves_to_raised(self):
        '''
        Tests when a relation that a child is raised by parent, it resolves to parent raised child
        '''
        parent = Person(name="parent", gender="F", family_id=self.family.id)
        parent.save()

        child = Person(name="child", gender="O", family_id=self.family.id)
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
        male = Person(name="male", gender="M", family_id=self.family.id)
        male.save()

        female = Person(name="female", gender="F", family_id=self.family.id)
        female.save()

        relation = Relation(from_person_id = male.id, to_person_id = female.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)

        self.assertEqual(male.id, relation.to_person_id)


    def test_partnered_other_to_female_resolves_to_female_to_other(self):
        '''
        Tests when an other gender partners a female, it resolves to females partners an other gender
        '''
        other = Person(name="other", gender="O", family_id=self.family.id)
        other.save()

        female = Person(name="female", gender="F", family_id=self.family.id)
        female.save()

        relation = Relation(from_person_id = other.id, to_person_id = female.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)
        self.assertEqual(other.id, relation.to_person_id)



    def test_partnered_other_to_male_resolves_to_male_to_other(self):
        '''
        Tests when a male partners an other gender, it resolves to other partners a male
        '''

        other = Person(name="other", gender="O", family_id=self.family.id)
        other.save()

        male = Person(name="male", gender="M", family_id=self.family.id)
        male.save()

        relation = Relation(from_person_id = other.id, to_person_id = male.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(male.id, relation.from_person_id)

        self.assertEqual(other.id, relation.to_person_id)


    def test_partnered_female_to_male_stays_the_same(self):
        '''
        Tests when a female partners a male, the relationship does not change
        '''

        female = Person(name="female", gender="F", family_id=self.family.id)
        female.save()

        male = Person(name="male", gender="M", family_id=self.family.id)
        male.save()

        relation = Relation(from_person_id = female.id, to_person_id = male.id, relation_type = PARTNERED)
        relation.normalise()

        self.assertEqual(female.id, relation.from_person_id)

        self.assertEqual(male.id, relation.to_person_id)


    def test_existing_relations_get_replaced(self):
        '''
        Tests that when a relations is added between two people, it replaces any existing relations between them
        '''
        existing1 = Person(name="existing1", gender="F", family_id=self.family.id)
        existing1.save()

        existing2 = Person(name="existing2", gender="F", family_id=self.family.id)
        existing2.save()

        relation = Relation(from_person_id = existing1.id, to_person_id = existing2.id, relation_type = RAISED)
        relation.save()

        new_relation = Relation(from_person_id = existing1.id, to_person_id = existing2.id, relation_type = PARTNERED)
        new_relation.save()

        self.assertEqual(1, Relation.objects.filter(from_person_id = existing1.id, to_person_id = existing2.id).count())
        self.assertEqual(PARTNERED, Relation.objects.get(from_person_id = existing1.id, to_person_id = existing2.id).relation_type)


    def test_create_inverted_relation(self):
        '''
        Tests an inverted relationship is correctly created when using manager function
        '''
        from_person = Person(name="from_person", gender="F", family_id=self.family.id)
        from_person.save()

        to_person = Person(name="to_person", gender="F", family_id=self.family.id)
        to_person.save()

        relation = Relation(from_person_id = from_person.id, to_person_id = to_person.id, relation_type = RAISED)

        inverted = Relation.objects._create_inverted_relation(relation)

        self.assertEqual(from_person.id, inverted.to_person_id)
        self.assertEqual(to_person.id, inverted.from_person_id)
        self.assertEqual(RAISED_BY, inverted.relation_type)


    def test_get_navigable_relations(self):

        my_family = Family()
        my_family.save()

        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100, family_id=my_family.id)

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=my_family.id)
        Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=my_family.id)
        Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=my_family.id)
        Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)

        paths_by_person = Relation.objects.get_navigable_relations(my_family.id)

        self.assertEqual(3, len(paths_by_person[person.id]))
        self.assertEqual(1, len(paths_by_person[son.id]))
        self.assertEqual(Relation, type(paths_by_person[son.id][0]))
