from django.db import models
from django.conf import settings
from django.core.mail import send_mail


# Email Types
SELF_REGISTRATION_CONFIRMATION = 'R'
OTHER_USER_REGISTERED_YOU_CONFIRMATION = 'O'
NEW_FAMILY_MEMBER = 'N'
MEMBER_DETAILS_UPDATED = 'U'

EMAIL_TYPE_CHOICES = (
    (SELF_REGISTRATION_CONFIRMATION, 'Self registration confirmation'),
    (OTHER_USER_REGISTERED_YOU_CONFIRMATION, 'Other User registered me confirmation'),
    (NEW_FAMILY_MEMBER, 'New Family Member'),
    (MEMBER_DETAILS_UPDATED, 'Family Member Deatils Updated'),
)

class EmailTemplate(models.Model):
    '''
    Allows data defined templates for emails
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'emailer'

        #Allows one biog per person per language
        unique_together = (('email_type', 'language'),)

    email_type = models.CharField(max_length=1, choices=EMAIL_TYPE_CHOICES, null = False, blank = False, db_index = True)
    language = models.CharField(max_length=5, choices=settings.LOCALES, null = False, blank = False, db_index = True)
    subject = models.CharField(null = True, blank = True, max_length = 60)
    content = models.TextField(null = True, blank = True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)


class EmailManager(models.Manager):
    '''
    Email manager, handles processing the email queue
    '''

    def process_emails(self):
        '''
        Sends all the daily update emails
        '''

        #Clean up any that have already been sent
        self.filter(send_successful = True).delete()

        #Only attempt to send emails that have low number of fails
        for email in self.filter(send_attempts__lt = 4):
            email.send()





class Email(models.Model):
    '''
    Represents an email that needs to be sent
    '''

    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'emailer'

    #Customer Manager
    objects = EmailManager()

    email_type = models.CharField(max_length=1, choices=EMAIL_TYPE_CHOICES, null = False, blank = False, db_index = True)
    recipient = models.EmailField(null = False, blank = False, db_index = True)
    subject = models.CharField(null = False, blank = False, max_length = 78)
    content = models.TextField(null = False, blank = False)
    creation_date = models.DateTimeField(auto_now_add=True)

    send_attempts = models.IntegerField(default=0, null = False)
    send_successful = models.BooleanField(default=False, null = False)

    def send(self):

        try:
            send_mail(self.subject, self.content, 'info@okkindred.com',[self.recipient], fail_silently=False)
            self.send_successful = True
        except:
            self.send_attempts += 1

        self.save()





class FamilyNewsLetter(models.Model):
    '''
    Represents a daily newsletter to inform an entire family of updates
    '''
    class Meta:
        #Allows models.py to be split up across multiple files
        app_label = 'emailer'





