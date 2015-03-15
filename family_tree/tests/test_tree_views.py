from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Relation, Family
from family_tree.services import tree_service
from family_tree.models.relation import PARTNERED, RAISED
from family_tree.views.tree_views import _get_css
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestTreeViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()


        user = User.objects.create_user(email='roger_taylor@queenonline.com', password='nation of haircuts', name='Roger Taylor')
        user.save()

        self.person = Person(name='Roger Taylor', gender='M', user_id = user.id, email='roger_taylor@queenonline.com', family_id=self.family.id)
        self.person.save()

        self.wife = Person.objects.create(name='wife', gender='F', hierarchy_score=100, family_id=self.family.id)
        self.wife_to_person = Relation.objects.create(from_person=self.wife, to_person=self.person, relation_type=PARTNERED)

        self.son = Person.objects.create(name='son', gender='M',hierarchy_score=101, family_id=self.family.id)
        self.person_to_son = Relation.objects.create(from_person=self.person, to_person=self.son, relation_type=RAISED)

        self.daughter = Person.objects.create(name='daughter', gender='F',hierarchy_score=101, family_id=self.family.id)
        self.person_to_daughter = Relation.objects.create(from_person=self.person, to_person=self.daughter, relation_type=RAISED)

        self.mum = Person.objects.create(name='mum', gender='F', hierarchy_score=99, family_id=self.family.id)
        self.mum_to_person = Relation.objects.create(from_person=self.mum, to_person=self.person, relation_type=RAISED)

        self.dad = Person.objects.create(name='dad', gender='M', hierarchy_score=99, family_id=self.family.id)
        self.dad_to_person = Relation.objects.create(from_person=self.dad, to_person=self.person, relation_type=RAISED)

        self.grandma = Person.objects.create(name='grandma', gender='F', hierarchy_score=98, family_id=self.family.id)
        self.grandma_to_mum = Relation.objects.create(from_person=self.grandma, to_person=self.mum, relation_type=RAISED)

        self.grandson = Person.objects.create(name='grandson', gender='M', hierarchy_score=102, family_id=self.family.id)
        self.son_to_grandson = Relation.objects.create(from_person=self.son, to_person=self.grandson, relation_type=RAISED)


    def test_home_tree_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/tree.html')

    def test_person_tree_view_loads(self):
        '''
        Tests that a tree view loads for a given person and uses correct template
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/person={0}/'.format(self.person.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/tree.html')


    def test_shows_error_screen_if_person_not_found_for_user(self):
        '''
        Tests that the error screen loads and uses the correct template
        when a person is not found
        '''
        user = User.objects.create_user(email='leroy_brown@queenonline.com', password='bring back that', family_id = self.family.id)
        user.save()


        self.client.login(email='leroy_brown@queenonline.com', password='bring back that')
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 404)



    def test_get_css(self):
        '''
        Checks that the css returned from the get_css function is correct
        '''
        related_data = tree_service.get_related_data(self.person)

        css =  _get_css(self.person, related_data, 300)

        mum_css = "#person%s{left:" % (self.mum.id)
        self.assertEqual(True, mum_css in css)

        dad_css = "#person%s{left:" % (self.dad.id)
        self.assertEqual(True, dad_css in css)


    def test_other_family_can_not_view_my_family_tree(self):
        '''
        Check people from different families cannot view each others profiles
        '''
        another_family = Family()
        another_family.save()

        user = User.objects.create_user(email='khashoggi@queenonline.com', password='party', family_id = another_family.id)
        user.save()

        self.client.login(email='khashoggi@queenonline.com', password='party')
        response = self.client.get('/person={0}/'.format(self.person.id))
        self.assertEqual(response.status_code, 404)


    def test_how_am_i_related_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/how_am_i_related={0}/'.format(self.grandma.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/how_am_i_related.html')

        self.assertEqual(True,b'grandma' in response.content)
        self.assertEqual(True,b'mum' in response.content)
        self.assertEqual(True,b'Roger Taylor' in response.content)
        self.assertEqual(True,b'Raised' in response.content)


    def test_whole_tree_view_loads(self):
        '''
        Tests that the whole tree view loads
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/whole_tree/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/whole_tree.html')


    def test_descendants_view_loads(self):
        '''
        Tests that the descendants view loads
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/descendants={0}/'.format( self.grandma.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/whole_tree.html')


    def test_ancestors_view_loads(self):
        '''
        Tests that the descendants view loads
        '''
        self.client.login(email='roger_taylor@queenonline.com', password='nation of haircuts')
        response = self.client.get('/ancestors={0}/'.format( self.grandson.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/whole_tree.html')
