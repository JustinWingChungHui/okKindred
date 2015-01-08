from django.test import TestCase
from django.contrib.auth.models import User
from family_tree.models import Person, Relation
from family_tree.models.relation import PARTNERED, RAISED
from family_tree.views import get_css
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestTreeViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        user = User.objects.create_user(username='roger_taylor', password='nation of haircuts')
        user.save()

        person = Person.objects.create(name='Roger Taylor', gender='M', user_id = user.id)
        person.save()

        self.create_related_data_for_tests()

    def create_related_data_for_tests(self):
        '''
        Create a small family tree for testing
        '''
        self.person = Person.objects.create(name='patient zero', gender='M',hierarchy_score=100)
        self.person.save()

        self.wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100)
        self.wife.save()
        self.wife_to_person = Relation.objects.create(from_person=self.wife, to_person=self.person, relation_type=PARTNERED)
        self.wife_to_person.save()

        self.son = Person.objects.create(name='son', gender='M',hierarchy_score=101)
        self.son.save()
        self.person_to_son = Relation.objects.create(from_person=self.person, to_person=self.son, relation_type=RAISED)
        self.person_to_son.save()

        self.daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101)
        self.daughter.save()
        self.person_to_daughter = Relation.objects.create(from_person=self.person, to_person=self.daughter, relation_type=RAISED)
        self.person_to_daughter.save()

        self.mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99)
        self.mum.save()
        self.mum_to_person = Relation.objects.create(from_person=self.mum, to_person=self.person, relation_type=RAISED)
        self.mum_to_person.save()

        self.dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99)
        self.dad.save()
        self.dad_to_person = Relation.objects.create(from_person=self.dad, to_person=self.person, relation_type=RAISED)
        self.dad_to_person.save()

        self.grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98)
        self.grandma.save()
        self.grandma_to_mum = Relation.objects.create(from_person=self.grandma, to_person=self.mum, relation_type=RAISED)
        self.grandma_to_mum.save()

        self.grandson = Person.objects.create(name='grandson', gender='M', hierarchy_score=102)
        self.grandson.save()
        self.son_to_grandson = Relation.objects.create(from_person=self.son, to_person=self.grandson, relation_type=RAISED)
        self.son_to_grandson.save()


    def test_home_tree_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(username='roger_taylor', password='nation of haircuts')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/tree.html')

    def test_person_tree_view_loads(self):
        '''
        Tests that a tree view loads for a given person and uses correct template
        '''
        self.client.login(username='roger_taylor', password='nation of haircuts')
        response = self.client.get('/person={0}/'.format(self.person.id))
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



    def test_get_css(self):
        '''
        '''
        related_data = Person.objects.get_related_data(self.person)

        css =  get_css(self.person, related_data, 300)

        mum_css = "#person%s{left: 100px; top: 0px;}" % (self.mum.id)
        self.assertEqual(True, mum_css in css)

        dad_css = "#person%s{left: 200px; top: 0px;}" % (self.dad.id)
        self.assertEqual(True, dad_css in css)



