from django.test import TestCase
from django.contrib.auth.models import User
from family_tree.models import Person

class TestProfileViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.user = User.objects.create_user(username='john_deacon', password='invisible man')
        self.user.save()

        self.person = Person.objects.create(name='John Deacon', gender='M', user_id=self.user.id)
        self.person.save()

        self.user2 = User.objects.create_user(username='brian_may', password='last horizon')
        self.user2.save()

        self.person2 = Person.objects.create(name='Brian May', gender='M', user_id=self.user2.id, locked=True)
        self.person2.save()


    def test_home_profile_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.get('/profile={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/profile.html')



    def test_update_person_denies_get_requests(self):
        '''
        Tests that get requests are not allowed
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.get('/update_person/')
        self.assertEqual(405, response.status_code)
        self.assertEqual("Only POST requests allowed", response.content)


    def test_update_person_denied_with_invalid_person_id(self):
        '''
        Tests that an invalid response is sent when trying to change a person that does not exist
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.post('/update_person/', {'pk': 204, 'name': 'name', 'value': 'new name'})
        self.assertEqual(405, response.status_code)
        self.assertEqual("Person ID is invalid", response.content)


    def test_update_person_denied_with_locked_profile(self):
        '''
        Tests that an invalid response is sent when trying to change a persons profile that is locked
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.post('/update_person/', {'pk': self.person2.id, 'name': 'name', 'value': 'new name'})
        self.assertEqual(405, response.status_code)
        self.assertEqual("Access denied to locked profile", response.content)


    def test_update_person_can_update_name(self):
        '''
        Tests that a field can be updated through api
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.post('/update_person/', {'pk': self.person.id, 'name': 'name', 'value': 'new name'})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual("new name", self.person.name)




