from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Biography, Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestProfileViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()

        self.user = User.objects.create_user(email='john_deacon@email.com', password='invisible man', name='John Deacon', family_id=self.family.id)
        self.user.is_confirmed = True
        self.user.save()

        self.person = Person.objects.create(name='John Deacon', gender='M', user_id=self.user.id, email='john_deacon@email.com', family_id=self.family.id)
        self.person.save()

        self.biography = Biography(person_id=self.person.id, language='en', content='')
        self.biography.save()

        self.user2 = User.objects.create_user(email='freddie_mercury@email.com', password='my love is dangerous', name='Freddie Mercury', family_id=self.family.id)
        self.user2.save()

        self.person2 = Person.objects.create(name='Freddie Mercury', gender='M', user_id=self.user2.id, locked=True, email='freddie_mercury@email.com', family_id=self.family.id)
        self.person2.save()

        self.another_family = Family()
        self.another_family.save()
        self.another_user = User.objects.create_user(email='prince_vultan@email.com', password="gordon's alive", name='Prince Vultan', family_id=self.another_family.id)
        self.another_user.save()

        self.confirmed_user = User.objects.create_user(email='general_kala@email.com', password='bring back his body', name='General Kala', family_id=self.family.id)
        self.confirmed_user.is_confirmed = True
        self.confirmed_user.save()

        self.confirmed_person = Person.objects.create(name='General Kala', gender='F', user_id=self.confirmed_user.id, locked=False, email='general_kala@email.com', family_id=self.family.id)
        self.confirmed_person.save()


    def test_home_profile_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.get('/profile={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/profile.html')


    def test_home_profile_not_visible_for_other_family(self):
        '''
        Test that people in different families cannot see profile
        '''
        self.client.login(email='prince_vultan@email.com', password="gordon's alive")
        response = self.client.get('/profile={0}/'.format(self.person.id))
        self.assertEqual(404, response.status_code)


    def test_edit_profile_loads(self):
        '''
        Tests that the edit profile view loads and uses the correct template
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.get('/edit_profile={0}/'.format(self.person.id))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'family_tree/edit_profile.html')


    def test_edit_profile_not_visible_for_other_family(self):
        '''
        Test that people in different families cannot see profile
        '''
        self.client.login(email='prince_vultan@email.com', password="gordon's alive")
        response = self.client.get('/edit_profile={0}/'.format(self.person.id))
        self.assertEqual(404, response.status_code)


    def test_update_person_denies_get_requests(self):
        '''
        Tests that get requests are not allowed
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.get('/update_person={0}/'.format(self.person2.id))
        self.assertEqual(405, response.status_code)
        self.assertEqual(b"Only POST requests allowed", response.content)


    def test_update_person_denied_with_invalid_person_id(self):
        '''
        Tests that an invalid response is sent when trying to change a person that does not exist
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person=204/', {'pk': 204, 'name': 'name', 'value': 'new name'})
        self.assertEqual(404, response.status_code)


    def test_update_person_denied_with_locked_profile(self):
        '''
        Tests that an invalid response is sent when trying to change a persons profile that is locked
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.person2.id), {'pk': self.person2.id, 'name': 'name', 'value': 'new name'})
        self.assertEqual(405, response.status_code)
        self.assertEqual(b"Access denied to locked profile", response.content)

    def test_cannot_update_family_id_through_api(self):
        '''
        Test cannot update non-whitelisted properties through api
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.person2.id), {'pk': self.person2.id, 'name': 'family_id', 'value': self.family.id})
        self.assertEqual(405, response.status_code)
        self.assertEqual(b"Access denied to locked profile", response.content)

    def test_update_person_can_update_name(self):
        '''
        Tests that a field can be updated through api
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'name', 'value': 'Brian Harold May'})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual("Brian Harold May", self.person.name)

    def test_update_email_saves_to_lowercase(self):
        '''
        Tests that email field can be updated through api and is always saved as
        lower case
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'email', 'value': 'BrianHaroldMay@QueenOnline.com'})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual("brianharoldmay@queenonline.com", self.person.email)


    def test_another_family_cannot_update_person_name(self):
        '''
        Tests that a field can be updated through api
        '''
        self.client.login(email='prince_vultan@email.com', password="gordon's alive")
        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'name', 'value': 'Brian Harold May'})
        self.assertEqual(404, response.status_code)


    def test_update_person_another_user_can_update_nonlocked_profile(self):
        '''
        Tests that a person field can be updated through api by a user who is not that person
        '''
        self.client.login(email='freddie_mercury@email.com', password='my love is dangerous')
        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'name', 'value': 'John Richard Deacon'})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual("John Richard Deacon", self.person.name)



    def test_update_person_can_update_boolean(self):
        '''
        Tests that a boolean field can be updated through api
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'locked', 'value': '1'})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual(True, self.person.locked)

        response = self.client.post('/update_person={0}/'.format(self.person.id), {'pk': self.person.id, 'name': 'locked', 'value': ''})
        self.assertEqual(200, response.status_code)
        self.person = Person.objects.get(id=self.person.id)
        self.assertEqual(False, self.person.locked)

    def test_update_person_cannot_update_email_with_confirmed_user(self):
        '''
        Tests that an invalid response is sent when trying to change a persons profile that is attached
        to a confirmed user
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_person={0}/'.format(self.confirmed_person.id), {'pk': self.confirmed_person.id, 'name': 'email', 'value': 'general_kala@evil.com'})
        self.assertEqual(405, response.status_code)
        self.assertEqual(b"Access denied to change confirmed user settings", response.content)


    def test_update_biography_denied_with_invalid_person_id(self):
        '''
        Tests that an invalid response is sent when trying to change a person that does not exist
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_biography=999/ln=en/', {'biography': 'new content'})
        self.assertEqual(404, response.status_code)

    def test_update_biography_denied_with_locked_profile(self):
        '''
        Tests that an invalid response is sent when trying to change the biography of a locked profile
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_biography={0}/ln=en/'.format(self.person2.id), {'biography': 'new content'})
        self.assertEqual(405, response.status_code)
        self.assertEqual(b"Access denied to locked profile", response.content)


    def test_update_biography_can_update_existing_biography(self):
        '''
        Tests that biography content can be updated through api when a biography already exists
        '''
        self.client.login(email='john_deacon@email.com', password='invisible man')
        response = self.client.post('/update_biography={0}/ln=en/'.format(self.person.id), {'biography': 'new content'})
        self.assertEqual(200, response.status_code)
        self.biography = Biography.objects.get(person_id=self.person.id, language='en')
        self.assertEqual('new content', self.biography.content)

    def test_another_family_cannot_update_biography(self):
        '''
        Tests that a field can be updated through api
        '''
        self.client.login(email='prince_vultan@email.com', password="gordon's alive")
        response = self.client.post('/update_biography={0}/ln=en/'.format(self.person.id), {'biography': 'new content'})
        self.assertEqual(404, response.status_code)


    def test_update_biography_can_create_new_biography(self):
        '''
        Tests that biography content can be updated through api when a biography already exists
        '''
        self.client.login(email='freddie_mercury@email.com', password='my love is dangerous')
        response = self.client.post('/update_biography={0}/ln=en/'.format(self.person2.id), {'biography': 'new content'})
        self.assertEqual(200, response.status_code)
        biography = Biography.objects.get(person_id=self.person2.id, language='en')
        self.assertEqual('new content', biography.content)

    def test_cannot_delete_profile_of_a_confirmed_user(self):
        '''
        Make sure that you cannot delete the profile of someone who is a user
        '''
        self.client.login(email='freddie_mercury@email.com', password='my love is dangerous')

        response = self.client.get('/delete={0}/'.format(self.person.id))


        self.assertEqual(405, response.status_code)

        #Check it exists
        person = Person.objects.get(id=self.person.id)
        self.assertEqual(self.person.id, person.id)


    def test_cannot_delete_profile(self):
        '''
        Make sure that you cannot delete the profile of someone who is a user
        '''
        person = Person.objects.create(name='David Tennant', gender='M', family_id=self.family.id)
        person.save()

        self.client.login(email='freddie_mercury@email.com', password='my love is dangerous')

        response = self.client.get('/delete={0}/'.format(person.id))

        self.assertEqual(302, response.status_code)

        #Check it has been deleted
        self.assertEqual(0, Person.objects.filter(id = person.id).count())
