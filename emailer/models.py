from django.db import models
from django.core.mail import send_mail
from django.db.models import Max
from django.db import connection
from common import query_to_dicts
from django.template.loader import get_template
from django.template import Context
from django.utils import translation
from datetime import timedelta
from django.utils import timezone
import math




class EmailManager(models.Manager):
    '''
    Email manager, handles processing the email queue
    '''

    def create_and_send_emails(self):
        '''
        Creates all the emails that need to be sent
        And sends them all
        '''

        #Create a list of events since last mailout
        if FamilyNewsLetterEvents.objects.create_news_letter_events():

            #Create the emails from the events
            self._create_emails()

            #Send the emails
            self._process_emails()

    def create_daily_emails(self):
        '''
        Creates the daily emails to be sent
        '''

        #Create a list of events since last mailout
        if FamilyNewsLetterEvents.objects.create_news_letter_events():

            #Create the emails from the events
            self._create_emails()


    def _process_emails(self):
        '''
        Sends all the daily update emails
        '''

        #Clean up any that have already been sent
        self.filter(send_successful = True).delete()

        #Only attempt to send emails that have low number of fails
        for email in self.filter(send_attempts__lt = 4).order_by('id'):
            email.send()

    def process_hourly_emails(self):
        '''
        Sends a proportion of the days emails
        '''
        #Clean up any that have already been sent
        self.filter(send_successful = True).delete()

        num_to_send = self._get_number_of_emails_to_send(timezone.now().hour)

        if num_to_send == 0:
            return

        #Only attempt to send emails that have low number of fails
        for email in self.filter(send_successful=False, send_attempts__lt = 4).order_by('id')[:num_to_send]:
            email.send()



    def _get_number_of_emails_to_send(self, hour):
        '''
        Gets the proportion of emails to send.
        Assume we send out a twelfth every hour for 12 hours
        '''

        #Can define a profile here to reduce network load
        proportion_to_send =  {
                        1: 0.084,
                        2: 0.091,
                        3: 0.1,
                        4: 0.111,
                        5: 0.125,
                        6: 0.143,
                        7: 0.167,
                        8: 0.2,
                        9: 0.25,
                        10: 0.333,
                        11: 0.5,
                        12: 1,
                    }.get(hour, 0)

        if proportion_to_send == 0:
            return 0

        return math.ceil(self.filter(send_successful=False, send_attempts__lt = 4).count() * proportion_to_send)


    def _create_emails(self):
        '''
        Creates all the emails ready to be sent
        '''

        family_id = 0

        for row in self._get_distinct_families_and_languages():
            language = row['language']

            translation.activate(language)
            if family_id != row['family_id']:
                family_id = row['family_id']
                new_people, updated_people = self._get_new_and_updated_people(family_id)

            subject = translation.ugettext('ok!Kindred family update')

            content = translation.ugettext('One or more of your family has had details in ok!Kindred updated.')

            content_html = get_template('emailer/people_updates.html').render(
                        Context({
                                    'language' : language,
                                    'new_people' : new_people,
                                    'updated_people' : updated_people
                                })
                        )

            #Using str(content_html) as content_html is of type django.utils.safestring.SafeText which stuffs up the mysql connector
            self._create_single_language_emails(language, family_id,subject, content, str(content_html))



    def _create_single_language_emails(self, language, family_id, subject, content, content_html):
        '''
        Creates the emails in batches for sections of families in their who share
        a first language
        '''
        cursor = connection.cursor()
        query = (   "INSERT INTO emailer_email "
                    "(recipient, subject, content, content_html, send_attempts, send_successful) "
                    "SELECT email, %s, %s, %s, 0 , 0 "
                    "FROM custom_user_user "
                    "WHERE language = %s AND family_id = %s "
                    "AND is_active = 1 AND receive_update_emails = 1;")



        cursor.execute(query, [subject, content, content_html, language, family_id])


    def _get_distinct_families_and_languages(self):
        '''
        Gets all the languages currently used by the families who are
        receiving the news emails
        '''
        #http://maxivak.com/executing-raw-sql-in-django/
        query = (   "SELECT DISTINCT custom_user_user.family_id, custom_user_user.language "
                    "FROM emailer_familynewsletterevents "
                    "INNER JOIN custom_user_user ON emailer_familynewsletterevents.family_id = custom_user_user.family_id "
                    "ORDER BY custom_user_user.family_id;")

        return list(query_to_dicts(query))


    def _get_new_and_updated_people(self, family_id):
        '''
        Gets a list of dicts of person_id and person_name of updated people and
         list of dicts of person_id and person_name of new people
        '''

        new_query = (  "SELECT person_id, person_name "
                        "FROM emailer_familynewsletterevents "
                        "WHERE family_id = {0} AND new_member = 1;").format(family_id)

        new_people = list(query_to_dicts(new_query))

        updated_query = (  "SELECT person_id, person_name "
                            "FROM emailer_familynewsletterevents "
                            "WHERE family_id = {0} AND new_member = 0;").format(family_id)

        updated_people = list(query_to_dicts(updated_query))

        return new_people, updated_people


class Email(models.Model):
    '''
    Represents an email that needs to be sent
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'emailer'

    #Customer Manager
    objects = EmailManager()

    recipient = models.EmailField(null = False, blank = False, db_index = True)
    subject = models.CharField(null = False, blank = False, max_length = 78)
    content = models.TextField(null = False, blank = False)
    content_html =models.TextField(null = False, blank = False)
    send_attempts = models.IntegerField(default=0, null = False)
    send_successful = models.BooleanField(default=False, null = False)

    def __str__(self): # __unicode__ on Python 2
        return self.recipient


    def send(self):

        try:
            send_mail(self.subject, self.content, 'info@okkindred.com',[self.recipient], fail_silently=False, html_message=self.content_html)
            self.send_successful = True
        except:
            self.send_attempts += 1

        self.save()



class FamilyNewsLetterEventsManager(models.Manager):
    '''
    Custom Manager for Family newsletter events
    '''


    def create_news_letter_events(self):
        '''
        Creates a news letter events for each family
        '''
        last_event_date = FamilyNewsLetterEvents.objects.aggregate(Max('creation_date'))['creation_date__max']

        if last_event_date is None: #Get a week ago
            last_event_date = timezone.now() - timedelta(7)


        #Check how many there were before adding in new ones
        old_count = FamilyNewsLetterEvents.objects.count()


        #Fastest to do one query
        cursor = connection.cursor()

        #Note a bug in SQLite prevents this from working properly
        created_query = ("INSERT INTO emailer_familynewsletterevents "
                       "(family_id,person_id,person_name,new_member,creation_date ) "
                       "SELECT family_id,id,name,1, last_updated_date "
                       "FROM family_tree_person "
                       "WHERE creation_date > %s;")

        update_query = ("INSERT INTO emailer_familynewsletterevents "
                       "(family_id, person_id,person_name,new_member, creation_date ) "
                       "SELECT family_id,id,name,0, last_updated_date "
                       "FROM family_tree_person "
                       "WHERE creation_date <= %s "
                       "AND last_updated_date > %s;")


        cursor.execute(created_query, [last_event_date])
        cursor.execute(update_query, [last_event_date, last_event_date])


        if FamilyNewsLetterEvents.objects.count() > old_count:
            #New news
            FamilyNewsLetterEvents.objects.filter(creation_date__lte=last_event_date).delete()


            return True
        else:
            return False



class FamilyNewsLetterEvents(models.Model):
    '''
    Represents a daily newsletter entry to inform an entire family of updates
    This object gets processed and queued into emails
    '''
    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'emailer'
        verbose_name_plural = "FamilyNewsLetterEvents"

    #Customer Manager
    objects = FamilyNewsLetterEventsManager()

    family_id = models.IntegerField(db_index = True, null=True) #Keep denormalised to be faster
    person_id = models.IntegerField(db_index = True, null=True) #Keep denormalised to be faster
    person_name = models.CharField(max_length=255, null=True) #Keep denormalised to be faster
    new_member = models.BooleanField(default=False, null=False, db_index=True)
    creation_date = models.DateTimeField(auto_now_add=True)


    def __str__(self): # __unicode__ on Python 2
        return self.person_name