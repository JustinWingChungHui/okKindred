from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings
from django.core import serializers

@override_settings(SSLIFY_DISABLE=True)
class TestSearchViews(TestCase):

    def setUp(self):
        '''
        Set up a family, user and profile to test with
        '''

        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='killer_queen@email.com', password='gunpowder')
        self.user.save()

        self.person = Person.objects.create(name='Killer Queen', gender='F', user_id=self.user.id, email='killer_queen@email.com', family_id=self.family.id)
        self.person.save()

        self.person2 = Person.objects.create(name='Black Queen', gender='F', user_id=self.user.id, family_id=self.family.id)
        self.person2.save()

        self.another_family = Family()
        self.another_family.save()

        self.person3 = Person.objects.create(name='White Queen', gender='F', user_id=self.user.id, family_id=self.another_family.id)
        self.person3.save()


    def test_search_page_loads(self):
        '''
        Tests the search page loads correctly
        '''
        self.client.login(email='killer_queen@email.com', password='gunpowder')
        response = self.client.get('/search/')

        self.assertEqual(200, response.status_code)
        self.assertTrue(b'Search' in response.content)



    def test_do_search_returns_valid_json_search_result(self):
        '''
        Tests the do search view return a search result
        '''

        self.client.login(email='killer_queen@email.com', password='gunpowder')
        response = self.client.post('/get_search_results_json/'.format(self.person.id),{'search_text': 'queen',})

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)

        self.assertEqual(200, response.status_code)

        self.assertTrue(b'Killer Queen' in response.content)
        self.assertTrue(b'Black Queen' in response.content)
        self.assertFalse(b'White Queen' in response.content)

    def test_do_search_terms_are_order_independent(self):
        '''
        Tests the do search view return a search result
        '''

        self.client.login(email='killer_queen@email.com', password='gunpowder')
        response = self.client.post('/get_search_results_json/'.format(self.person.id),{'search_text': 'queen black',})

        #Check that the response is valid json
        serializers.json.Deserializer(response.content)

        self.assertEqual(200, response.status_code)
        self.assertTrue(b'Black Queen' in response.content)

