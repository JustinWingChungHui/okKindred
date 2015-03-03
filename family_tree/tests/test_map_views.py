from django.test import TestCase
from custom_user.models import User
from family_tree.models import Person, Family
from django.test.utils import override_settings

@override_settings(SSLIFY_DISABLE=True)
class TestMapViews(TestCase):

    def setUp(self):
        '''
        Creates credientials as all views require login
        '''
        self.family = Family()
        self.family.save()


        self.user = User.objects.create_user(email='adam_lambert@queenonline.com', password='sexy boy', name='Adam Lambert', family_id=self.family.id)


        self.person1 = Person(name='Adam Lambert', gender='M', user_id = self.user.id, email='adam_lambert@queenonline.com'
                                    , family_id=self.family.id, latitude = 39.768, longitude = -86.158, address = 'Indianapolis, Indiana')
        self.person1.save()

        self.person2 = Person(name='Paul Rodgers', gender='M', family_id=self.family.id, latitude = 54.574, longitude = -1.235, address = 'Middlesborough, UK')
        self.person2.save()



    def test_map_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='adam_lambert@queenonline.com', password='sexy boy')
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/family_map.html')

        self.assertTrue(b'Paul Rodgers' in response.content)

        self.assertTrue(b'x.push(54.574)' in response.content)
        self.assertTrue(b'y.push(-1.235)' in response.content)

        self.assertTrue(b'Adam Lambert' in response.content)
        self.assertTrue(b'x.push(39.768)' in response.content)
        self.assertTrue(b'y.push(-86.158)' in response.content)

        self.assertTrue(b'center: new google.maps.LatLng(39.768,-86.158)' in response.content)




    def test_map_with_person_args_view_loads(self):
        '''
        Tests that the users home screen loads and uses the correct template
        '''
        self.client.login(email='adam_lambert@queenonline.com', password='sexy boy')
        response = self.client.get('/map={0}/'.format(self.person2.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/family_map.html')

        self.assertTrue(b'Paul Rodgers' in response.content)

        self.assertTrue(b'x.push(54.574)' in response.content)
        self.assertTrue(b'y.push(-1.235)' in response.content)

        self.assertTrue(b'Adam Lambert' in response.content)
        self.assertTrue(b'x.push(39.768)' in response.content)
        self.assertTrue(b'y.push(-86.158)' in response.content)

        self.assertTrue(b'center: new google.maps.LatLng(54.574,-1.235)' in response.content)


    def test_map_view_loads_in_polish(self):
        '''
        This is to check a bug where coordinates were formatted to have commas instead of decimal points
        when language set to Polish
        '''

        #Create a Polish user
        user = User.objects.create_user(email='szajka@nowahuta.pl', password='nowa huta', name='Szajka', family_id=self.family.id, language='pl')
        self.client.login(email='szajka@nowahuta.pl', password='nowa huta')
        Person.objects.create(name='Szajka', gender='M', user_id = user.id, email='szajka@nowahuta.pl', family_id=self.family.id, language='pl')
        from django.utils import translation
        translation.activate('pl')

        response = self.client.get('/map={0}/'.format(self.person2.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'family_tree/family_map.html')

        self.assertTrue(b'Paul Rodgers' in response.content)

        self.assertTrue(b'x.push(54.574)' in response.content)
        self.assertTrue(b'y.push(-1.235)' in response.content)

        self.assertTrue(b'Adam Lambert' in response.content)
        self.assertTrue(b'x.push(39.768)' in response.content)
        self.assertTrue(b'y.push(-86.158)' in response.content)

        self.assertTrue(b'center: new google.maps.LatLng(54.574,-1.235)' in response.content)

        #Check map is localised
        self.assertTrue(b'&language=pl' in response.content)
