from django.db import models
from family_tree.models.person import Person
from django.utils.translation import ugettext_lazy as _

#Relation types.  Note that 'raised by' will resolve to 'raised' but inverse
PARTNERED = 1
RAISED = 2
RAISED_BY = 3

RELATION_TYPES = (
    (PARTNERED, _('Partnered')),
    (RAISED, _('Raised')),
    (RAISED_BY, _('Raised By')),
)


class RelationManager(models.Manager):
    '''
    Custom manager to represent relations
    '''

    def get_all_relations_for_family_id(self, family_id):
        '''
        Gets all the relations for a family
        '''
        return self.raw("""
                        SELECT r.*
                        FROM family_tree_person p
                        INNER JOIN family_tree_relation r
                        ON r.from_person_id = p.id
                        AND p.family_id={0}
                        """.format(family_id))


    def get_navigable_relations(self, family_id, relations=None):
        '''
        Gets the relations in a navigable format to determine paths
        returns a dictionary of paths by person id
        '''

        if not relations:
            relations = self.get_all_relations_for_family_id(family_id)

        paths_by_person = {}

        for relation in relations:

            #Add the from person path
            if not relation.from_person_id in paths_by_person:
                paths_by_person[relation.from_person_id] = []

            paths_by_person[relation.from_person_id].append(relation)

            #Add the to person path
            if not relation.to_person_id in paths_by_person:
                paths_by_person[relation.to_person_id] = []

            paths_by_person[relation.to_person_id].append(self._create_inverted_relation(relation))

        return paths_by_person


    def _create_inverted_relation(self, relation):
        '''
        Creates inverted relation, used to determine paths
        '''
        if relation.relation_type == PARTNERED:
            new_type = PARTNERED
        elif relation.relation_type == RAISED:
            new_type = RAISED_BY
        elif relation.relation_type == RAISED_BY:
            new_type = RAISED

        return Relation(from_person_id=relation.to_person_id
                            ,to_person_id=relation.from_person_id
                            ,relation_type=new_type)


class Relation(models.Model):
    '''
    Represent a relation between two people
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'family_tree'

        #Allows one relation betwen two people
        unique_together = (('from_person', 'to_person'),)

    #Customer Manager
    objects = RelationManager()

    #Required fields
    from_person =  models.ForeignKey(Person,db_index=True, related_name = 'from_person', null = False, blank = False)
    to_person =  models.ForeignKey(Person,db_index=True, related_name = 'to_person', null = False, blank = False)
    relation_type = models.IntegerField(choices=RELATION_TYPES, null = False, blank = False)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)



    def __str__(self): # __unicode__ on Python 2
        return self.from_person.name + '-' + self.to_person.name


    def normalise(self):
        '''
        This normalises the relations.
        'raised by' will be resolved to 'raised' but inverted relation
        'Partnered' will ordered by gender with sorted alphabetically
        '''
        #Invert Raised by relationship
        if self.relation_type == RAISED_BY:
            self._invert_relationship()
            self.relation_type = RAISED


        if self.relation_type ==PARTNERED:

            if self.from_person.gender == 'M' and self.to_person.gender == 'F':
                self._invert_relationship()

            elif self.from_person.gender == 'O' and self.to_person.gender == 'F':
                self._invert_relationship()

            elif self.from_person.gender == 'O' and self.to_person.gender == 'M':
                self._invert_relationship()



    def _invert_relationship(self):
        '''
        Swaps the from and to in the relationship
        '''
        from_id = self.from_person_id
        self.from_person_id = self.to_person_id
        self.to_person_id = from_id


    def save(self, *args, **kwargs):
        '''
        Overrides the save method to allow normalisation
        '''
        self.normalise()

        #Delete any relations already defined between both people
        Relation.objects.filter(from_person_id = self.from_person_id, to_person_id = self.to_person_id).delete()
        Relation.objects.filter(from_person_id = self.to_person_id, to_person_id = self.from_person_id).delete()

        super(Relation, self).save(*args, **kwargs) # Call the "real" save() method.
