from django.test import TestCase
from django.contrib.auth.models import User
from family_tree.models import Person, Relation
from family_tree.models.relation import PARTNERED, RAISED
from family_tree.views import get_related_data

class TestTreeViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        user = User.objects.create_user(username='roger_taylor', password='nation of haircuts')
        user.save()

        person = Person.objects.create(name='Roger Taylor', gender='M', user_id = user.id)
        person.save()

    def test_home_tree_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(username='roger_taylor', password='nation of haircuts')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/tree.html')


    def test_shows_error_screen_if_person_not_found_for_user(self):
        '''
        Tests that the error screen loads and uses the correct template
        when a person is not found
        '''
        user = User.objects.create_user(username='brian_may', password='resurrection')
        user.save()


        self.client.login(username='brian_may', password='resurrection')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/no_match_found.html')


    def test_get_related_data(self):
        '''
        Tests the get_related function.  Set up a small family tree with parents and children
        We set hierarchry scores manually as we are not testing them
        '''
        person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100)
        person.save()

        wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100)
        wife.save()
        wife_to_person = Relation.objects.create(from_person=wife, to_person=person, relation_type=PARTNERED)
        wife_to_person.save()

        son = Person.objects.create(name='son', gender='M',hierarchy_score=101)
        son.save()
        person_to_son = Relation.objects.create(from_person=person, to_person=son, relation_type=RAISED)
        person_to_son.save()

        daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101)
        daughter.save()
        person_to_daughter = Relation.objects.create(from_person=person, to_person=daughter, relation_type=RAISED)
        person_to_daughter.save()

        mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99)
        mum.save()
        mum_to_person = Relation.objects.create(from_person=mum, to_person=person, relation_type=RAISED)
        mum_to_person.save()

        dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99)
        dad.save()
        dad_to_person = Relation.objects.create(from_person=dad, to_person=person, relation_type=RAISED)
        dad_to_person.save()

        grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98)
        grandma.save()
        grandma_to_mum = Relation.objects.create(from_person=grandma, to_person=mum, relation_type=RAISED)
        grandma_to_mum.save()

        grandson = Person.objects.create(name='grandson', gender='M', hierarchy_score=102)
        grandson.save()
        son_to_grandson = Relation.objects.create(from_person=son, to_person=grandson, relation_type=RAISED)
        son_to_grandson.save()

        related_data = get_related_data(person)

        self.assertEqual(related_data.people_upper[0].id, mum.id)
        self.assertEqual(related_data.people_upper[1].id, dad.id)
        self.assertEqual(related_data.people_upper[2].id, wife.id)
        self.assertEqual(len(list(related_data.people_upper)), 3) #raw query sets don't have a count function

        self.assertEqual(related_data.people_lower[0].id, daughter.id)
        self.assertEqual(related_data.people_lower[1].id, son.id)
        self.assertEqual(len(list(related_data.people_lower)), 2)

        self.assertEqual(len(list(related_data.relations)), 5)

