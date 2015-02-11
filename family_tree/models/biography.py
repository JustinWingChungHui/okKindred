from django.db import models
from family_tree.models.person import Person
from django.conf import settings
import bleach

class BiographyManager(models.Manager):
    '''
    Adds Methods to get default language biographies to standard model manager
    '''

    def get_or_none(self, **kwargs):
        '''
        Get that returns None if record does not exist
        '''
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def get_biography(self, person_id, requested_language = '', default_language = ''):
        '''
        Gets the biography.  If no language is specified, it defaults to the user's default language.
        If no biog is written in that language, it gets the one in english.  Failing that it gets the first available one
        '''

        biography = None

        if requested_language:
            return Biography.objects.get_or_none(person_id = person_id, language = requested_language)

        #No biography in requested language get default language
        if biography is None and requested_language != default_language:
            biography = Biography.objects.get_or_none(person_id = person_id, language = default_language)

        #No biography in default language get biography in English
        if biography is None and default_language != 'en':
            biography = Biography.objects.get_or_none(person_id = person_id, language = 'en')

        #No biography in english, get first available language
        if biography is None:
                try:
                    biography = Biography.objects.filter(person_id = person_id)[0]
                except:
                    biography = None

        return biography



class Biography(models.Model):
    '''
    Class that represents a biography.
    Allows a person to have biographies in different languages.
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'family_tree'

        #Allows one biog per person per language
        unique_together = (('person', 'language'),)

        verbose_name_plural = "Biographies"

    #Specify custom model manager
    objects = BiographyManager()

    #Fields
    person = models.ForeignKey(Person, null = False, blank = False, db_index = True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null = False, blank = False, db_index = True)
    content = models.TextField(null = True, blank = True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    allowed_print_tags = [
            # tags whitelist
            "h1", "h2", "h3", "h4", "h5", "h6",
            "b", "i", "strong", "em", "tt","u","small",
            "p", "br",
            "span", "div", "blockquote", "code", "hr",
            "ul", "ol", "li", "dd", "dt",
            "table","thead","tbody","tfoot","tr","th","td",
            ]


    def __str__(self): # __unicode__ on Python 2
        return self.person.name + ' ' + self.language



    def save(self, *args, **kwargs):
        '''
        Overrides the save method to sanitise the content field
        '''
        self.content = bleach.clean(text=self.content, tags=self.allowed_print_tags)
        super(Biography, self).save(*args, **kwargs) # Call the "real" save() method.
