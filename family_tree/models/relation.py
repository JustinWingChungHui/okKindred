from django.db import models
from family_tree.models.person import Person

#Relation types.  Note that 'raised by' will resolve to 'raised' but inverse
PARTNERED = 1
RAISED = 2
RAISED_BY = 3

RELATION_TYPES = (
    (PARTNERED, 'Partnered'),
    (RAISED, 'Raised'),
    (RAISED_BY, 'Raised By'),
)


class Relation(models.Model):
    '''
    Represent a relation between two people
    '''

    class Meta:
        #Allows models.py to be spp[lit up across multiple files
        app_label = 'family_tree'

        #Allows one relation betwen two people
        unique_together = (('from_person', 'to_person'),)

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
        super(Relation, self).save(*args, **kwargs) # Call the "real" save() method.
