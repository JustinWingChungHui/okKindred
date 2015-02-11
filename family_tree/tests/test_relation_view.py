from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Relation, Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestRelationViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='prince_barin@flash.com', password='arboria', name='Prince Barin')
        self.user.save()

        self.person = Person(name='Prince Barin', gender='M', user_id = self.user.id, email='prince_barin@flash.com', family_id=self.family.id)
        self.person.save()

        #http://flashgordon.wikia.com/wiki/Prince_Barin
        self.son = Person(name='Prince Alan', gender='M', family_id=self.family.id)
        self.son.save()

    def test_add_relation_view_loads(self):
        '''
        Tests that the add_relation_view loads and uses the correct template
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.get('/en/add_relation={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/add_relation.html')


    def test_add_relation_post_rejects_invalid_relation(self):
        '''
        Tests that the add relation api rejects incorrect data
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '0', 'relation_type': '4',})
        self.assertEqual(404, response.status_code)

    def test_add_relation_post_rejects_invalid_name(self):
        '''
        Tests that the add relation api rejects incorrect data
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '0', 'relation_type': '1', 'name': ''})
        self.assertEqual(404, response.status_code)

    def test_add_relation_post_rejects_invalid_language(self):
        '''
        Tests that the add relation api rejects incorrect data
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '0', 'relation_type': '1', 'name': 'Princess Aura', 'language': 'Klingon'})
        self.assertEqual(404, response.status_code)

    def test_add_relation_post_rejects_invalid_gender(self):
        '''
        Tests that the add relation api rejects incorrect data
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '0', 'relation_type': '1', 'name': 'Princess Aura', 'language': 'en', 'gender': 'W'})
        self.assertEqual(404, response.status_code)

    def test_add_relation_creates_person_and_relation(self):
        '''
        Test that the add relation api correctly creates the right records
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '0', 'relation_type': '1', 'name': 'Princess Aura', 'language': 'en', 'gender': 'F'})
        self.assertEqual(302, response.status_code)

        aura = Person.objects.get(name = 'Princess Aura')
        self.assertEqual('en', aura.language)
        self.assertEqual('F', aura.gender)
        self.assertEqual(self.family.id, aura.family_id)

        relation =Relation.objects.get(from_person_id = aura.id, to_person_id = self.person.id)
        self.assertEqual(1, relation.relation_type)


    def test_add_relation_to_existing_people(self):
        '''
        Tests that a relation can be added between two existing people
        '''
        self.client.login(email='prince_barin@flash.com', password='arboria')
        response = self.client.post('/add_relation_post={0}/'.format(self.person.id),{'existing_person': '1', 'relation_type': '2', 'relation_id': str(self.son.id)})
        self.assertEqual(302, response.status_code)

        relation =Relation.objects.get(from_person_id = self.person.id, to_person_id = self.son.id)
        self.assertEqual(2, relation.relation_type)



