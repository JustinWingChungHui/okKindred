from family_tree.models import Family, Person
from family_tree.services import map_service
from django.test import TestCase


class MapServiceTestCase(TestCase):

    '''
    This defines all the tests for the map service
    '''
    def setUp(self):

        self.family = Family()
        self.family.save()


    def test_get_snapped_location_for_a_person(self):
        '''
        Tests that the service snaps the location of a person to a grid
        '''

        person1 = Person(family_id = self.family.id,
                                        name = "person1",
                                        latitude = 1.2,
                                        longitude = 4.3,
                                        )

        division_size = 1.0

        result = map_service._get_snapped_location(person1, division_size)

        self.assertEqual(1.5, result[0])
        self.assertEqual(4.5, result[1])


    def test_combines_multiple_people_near_to_each_other(self):
        '''
        Tests that the service combines two people that are close together
        '''
        person1 = Person(family_id = self.family.id,
                                name = "person1",
                                latitude = 7.2,
                                longitude = 12.3,
                                )
        super(Person, person1).save() # original save so does not overwrite the location

        person1 = Person(family_id = self.family.id,
                                name = "person1",
                                latitude = 7.3,
                                longitude = 12.5,
                                )
        super(Person, person1).save() # original save so does not overwrite the the location

        division_size = 5

        result = map_service.get_person_location_points(self.family.id, division_size)

        self.assertEqual(True, '(7.5, 12.5)' in result)
        self.assertEqual(2, len(result['(7.5, 12.5)']))
