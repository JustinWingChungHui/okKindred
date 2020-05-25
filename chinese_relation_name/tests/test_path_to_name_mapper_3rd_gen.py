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


        path = Path()
        path.set_goals(person, maternal_great_grandmother)
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


        path = Path()
        path.set_goals(person, paternal_great_grandfather)
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


        path = Path()
        path.set_goals(person, great_grandfather)
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


        path = Path()
        path.set_goals(person, step_grandparent)
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


        path = Path()
        path.set_goals(person, aunt)
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


        path = Path()
        path.set_goals(person, uncle)
        path.add_node(father, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(uncle, RAISED)

        result = get_name(path)

        self.assertTrue("Father's Younger Brother" in result)
        self.assertTrue("Father's Brother" in result)

    def test_fathers_sister(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        father = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id, birth_year=1990))
        grandparent = Node(Person.objects.create(name='grandparent', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id))


        path = Path()
        path.set_goals(person, aunt)
        path.add_node(father, RAISED_BY)
        path.add_node(grandparent, RAISED_BY)
        path.add_node(aunt, RAISED)

        result = get_name(path)

        self.assertTrue("Father's Elder Sister" in result)
        self.assertTrue("Father's Younger Sister" in result)
        self.assertTrue("Father's Sister" in result)


    def test_elder_sisters_husband(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=1990))
        father = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id))
        sister = Node(Person.objects.create(name='sister', gender='F', family_id=self.family.id, birth_year=1989))
        sisters_husband = Node(Person.objects.create(name='sisters_husband', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, sisters_husband)
        path.add_node(father, RAISED_BY)
        path.add_node(sister, RAISED)
        path.add_node(sisters_husband, PARTNERED)

        result = get_name(path)

        self.assertTrue("Elder Sibling's Husband" in result)


    def test_siblings_partner_(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id))
        sibling = Node(Person.objects.create(name='sibling', gender='O', family_id=self.family.id))
        siblings_partner = Node(Person.objects.create(name='siblings_partner', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, siblings_partner)
        path.add_node(parent, RAISED_BY)
        path.add_node(sibling, RAISED)
        path.add_node(siblings_partner, PARTNERED)

        result = get_name(path)

        self.assertTrue("Elder Sibling's Husband" in result)
        self.assertTrue("Younger Sibling's Husband" in result)
        self.assertTrue("Elder Sibling's Wife" in result)
        self.assertTrue("Younger Sibling's Wife" in result)


    def test_brothers_daughter(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id))
        brother = Node(Person.objects.create(name='brother', gender='M', family_id=self.family.id))
        brothers_daughter = Node(Person.objects.create(name='brothers_daughter', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, brothers_daughter)
        path.add_node(parent, RAISED_BY)
        path.add_node(brother, RAISED)
        path.add_node(brothers_daughter, RAISED)

        result = get_name(path)

        self.assertTrue("Brother's Daughter" in result)


    def test_sisters_child(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id))
        sister = Node(Person.objects.create(name='sister', gender='F', family_id=self.family.id))
        sisters_child = Node(Person.objects.create(name='sisters_child', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, sisters_child)
        path.add_node(parent, RAISED_BY)
        path.add_node(sister, RAISED)
        path.add_node(sisters_child, RAISED)

        result = get_name(path)

        self.assertTrue("Sister's Daughter" in result)
        self.assertTrue("Sister's Son" in result)


    def test_wifes_younger_sister(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        wife = Node(Person.objects.create(name='wife', gender='F', family_id=self.family.id, birth_year=1990))
        wifes_mother = Node(Person.objects.create(name='wifes_mother', gender='F', family_id=self.family.id))
        wifes_sister = Node(Person.objects.create(name='wifes_sister', gender='F', family_id=self.family.id, birth_year=1998))

        path = Path()
        path.set_goals(person, wifes_sister)
        path.add_node(wife, PARTNERED)
        path.add_node(wifes_mother, RAISED_BY)
        path.add_node(wifes_sister, RAISED)

        result = get_name(path)

        self.assertTrue("Wife's Younger Sister" in result)

    def test_husbands_elder_sister(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        husband = Node(Person.objects.create(name='husband', gender='M', family_id=self.family.id, birth_year=1990))
        husbands_mother = Node(Person.objects.create(name='husbands_mother', gender='F', family_id=self.family.id))
        husbands_sister = Node(Person.objects.create(name='husbands_sister', gender='F', family_id=self.family.id, birth_year=1988))

        path = Path()
        path.set_goals(person, husbands_sister)
        path.add_node(husband, PARTNERED)
        path.add_node(husbands_mother, RAISED_BY)
        path.add_node(husbands_sister, RAISED)

        result = get_name(path)

        self.assertTrue("Husband's Elder Sister" in result)


    def test_partners_brother(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        partner = Node(Person.objects.create(name='partner', gender='O', family_id=self.family.id))
        partners_mother = Node(Person.objects.create(name='partner_mother', gender='F', family_id=self.family.id))
        partners_brother = Node(Person.objects.create(name='partner_brother', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, partners_brother)
        path.add_node(partner, PARTNERED)
        path.add_node(partners_mother, RAISED_BY)
        path.add_node(partners_brother, RAISED)

        result = get_name(path)

        self.assertTrue("Wife's Elder Brother" in result)
        self.assertTrue("Wife's Younger Brother" in result)
        self.assertTrue("Husband's Elder Brother" in result)
        self.assertTrue("Husband's Younger Brother" in result)


    def test_childs_mother_in_law(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        child = Node(Person.objects.create(name='child', gender='O', family_id=self.family.id))
        childs_partner = Node(Person.objects.create(name='childs_partner', gender='O', family_id=self.family.id))
        childs_partners_mother = Node(Person.objects.create(name='childs_partners_mother', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, childs_partners_mother)
        path.add_node(child, RAISED)
        path.add_node(childs_partner, PARTNERED)
        path.add_node(childs_partners_mother, RAISED_BY)

        result = get_name(path)

        self.assertTrue("Child's Mother In Law" in result)


    def test_female_great_grandchild_male_lineage(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        child = Node(Person.objects.create(name='child', gender='M', family_id=self.family.id))
        grandchild = Node(Person.objects.create(name='grandchild', gender='M', family_id=self.family.id))
        great_grandchild = Node(Person.objects.create(name='great_grandchild', gender='F', family_id=self.family.id))

        path = Path()
        path.set_goals(person, great_grandchild)
        path.add_node(child, RAISED)
        path.add_node(grandchild, RAISED)
        path.add_node(great_grandchild, RAISED)

        result = get_name(path)

        self.assertTrue("Son's Granddaughter" in result)


    def test_male_great_grandchild_non_other_lineage(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        child = Node(Person.objects.create(name='child', gender='O', family_id=self.family.id))
        grandchild = Node(Person.objects.create(name='grandchild', gender='M', family_id=self.family.id))
        great_grandchild = Node(Person.objects.create(name='great_grandchild', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, great_grandchild)
        path.add_node(child, RAISED)
        path.add_node(grandchild, RAISED)
        path.add_node(great_grandchild, RAISED)

        result = get_name(path)

        self.assertTrue("Son's Grandson" in result)
        self.assertTrue("Daughter's Grandson" in result)


    def test_mothers_sisters_husband(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        mother = Node(Person.objects.create(name='mother', gender='F', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id))
        aunt_husband = Node(Person.objects.create(name='aunt husband', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, aunt_husband)
        path.add_node(mother, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt, RAISED)
        path.add_node(aunt_husband, PARTNERED)

        result = get_name(path)

        self.assertTrue("Mother's Sister's Husband" in result)

    def test_fathers_elder_sisters_husband(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        father = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id, birth_year=1992))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id, birth_year=1990))
        aunt_husband = Node(Person.objects.create(name='aunt husband', gender='M', family_id=self.family.id))

        path = Path()
        path.set_goals(person, aunt_husband)
        path.add_node(father, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt, RAISED)
        path.add_node(aunt_husband, PARTNERED)

        result = get_name(path)

        self.assertEqual(["Father's Elder Sister's Husband"], result)

    def test_aunt_uncle_partner(self):

        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id))
        parent = Node(Person.objects.create(name='parent', gender='O', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt_uncle = Node(Person.objects.create(name='aunt_uncle', gender='OF', family_id=self.family.id))
        aunt_uncle_partner = Node(Person.objects.create(name='aunt_uncle partner', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, aunt_uncle_partner)
        path.add_node(parent, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt_uncle, RAISED)
        path.add_node(aunt_uncle_partner, PARTNERED)

        result = get_name(path)

        self.assertTrue("Mother's Sister's Husband" in result)
        self.assertTrue("Mother's Brother's Wife" in result)
        self.assertTrue("Father's Elder Sister's Husband" in result)
        self.assertTrue("Father's Younger Brother's Wife" in result)


    def test_maternal_male_elder_cousin(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=2000))
        mother = Node(Person.objects.create(name='mother', gender='F', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id))
        aunt_son = Node(Person.objects.create(name='aunt husband', gender='M', family_id=self.family.id, birth_year=1998))

        path = Path()
        path.set_goals(person, aunt_son)
        path.add_node(mother, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt, RAISED)
        path.add_node(aunt_son, RAISED)

        result = get_name(path)

        self.assertTrue("Maternal Elder Male Cousin" in result)


    def test_paternal_cousin(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=2000))
        father = Node(Person.objects.create(name='father', gender='M', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id))
        cousin = Node(Person.objects.create(name='aunt husband', gender='O', family_id=self.family.id))

        path = Path()
        path.set_goals(person, cousin)
        path.add_node(father, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt, RAISED)
        path.add_node(cousin, RAISED)

        result = get_name(path)

        self.assertTrue("Paternal Elder Male Cousin" in result)
        self.assertTrue("Paternal Younger Male Cousin" in result)
        self.assertTrue("Paternal Elder Female Cousin" in result)
        self.assertTrue("Paternal Younger Female Cousin" in result)


    def test_maternal_younger_cousin(self):
        person = Node(Person.objects.create(name='patient zero', gender='M', family_id=self.family.id, birth_year=2000))
        mother = Node(Person.objects.create(name='mother', gender='F', family_id=self.family.id))
        grandmother = Node(Person.objects.create(name='grandmother', gender='F', family_id=self.family.id))
        aunt = Node(Person.objects.create(name='aunt', gender='F', family_id=self.family.id))
        cousin = Node(Person.objects.create(name='aunt husband', gender='O', family_id=self.family.id, birth_year=2005))

        path = Path()
        path.set_goals(person, cousin)
        path.add_node(mother, RAISED_BY)
        path.add_node(grandmother, RAISED_BY)
        path.add_node(aunt, RAISED)
        path.add_node(cousin, RAISED)

        result = get_name(path)

        self.assertTrue("Maternal Younger Male Cousin" in result)
        self.assertTrue("Maternal Younger Female Cousin" in result)


