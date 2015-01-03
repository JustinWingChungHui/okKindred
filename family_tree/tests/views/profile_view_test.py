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

        self.person = Person.objects.create(name='John Deacon', gender='M', user_id = self.user.id)
        self.person.save()


    def test_home_profile_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(username='john_deacon', password='invisible man')
        response = self.client.get('/profile={0}/'.format(self.person.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/profile.html')