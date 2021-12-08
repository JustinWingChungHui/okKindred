from django.conf import settings
from django.db import models
from django.utils import translation
from django.template.loader import get_template
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from common.utils import create_hash


class EmailConfirmationManager(models.Manager):
    '''
    Email confirmation custom manager
    '''
    def remove_expired_email_confirmations(self):
        '''
        Remove all pending email confirmations that are over 4 weeks old
        '''
        d = timezone.now() - timedelta(days=28)
        self.filter(sent__lte = d).delete()



# based on https://code.google.com/p/django-email-confirmation/source/browse/trunk/devproject/emailconfirmation/models.py
# and https://github.com/pinax/django-user-accounts/

class EmailConfirmation(models.Model):
    '''
    Represents an email confirmation sent out to confirm joining website
    '''

    email_address = models.EmailField(null=False, unique=True)
    person = models.ForeignKey('family_tree.Person', null=True, unique=True, on_delete=models.CASCADE) #Use of model string name to prevent circular import
    sent = models.DateTimeField(db_index = True)
    confirmation_key = models.CharField(max_length=64, unique=True)
    user_who_invited_person = models.ForeignKey('custom_user.User', null=False, on_delete=models.CASCADE) #Use of model string name to prevent circular import

    objects = EmailConfirmationManager()

    class Meta:
        indexes = [
            models.Index(fields=['person']),
            models.Index(fields=['confirmation_key']),
        ]

    def __str__(self):
        return self.person.name + " " + self.email_address

    def send_email(self):

        language = self.person.language
        translation.activate(language)

        subject = translation.gettext('An invitation to ok!Kindred from {0}').format(self.user_who_invited_person.name)

        content = translation.gettext( """Hi {0}
                                            You have been invited by {1} to join ok!Kindred.
                                            ok!Kindred is a collaborative family tree and private social network for you and you family.
                                            A network has already been set up by one of your family members to help you keep in touch.
                                            To join, please go to {2}/#/accounts/invite_confirmation/{3}/
                                        """.format(self.person.name, self.user_who_invited_person.name, settings.DOMAIN, self.confirmation_key))

        content_html = self._create_email_body_html()


        send_mail(subject, content, 'info@okkindred.com',[self.email_address], fail_silently=False, html_message=content_html)
        self.sent = timezone.now()


    #https://github.com/pinax/django-user-accounts/blob/dfa66fdffa4c2b81515658e65b39415b237ae29b/account/hooks.py
    def generate_confirmation_key(self):
        '''
        Creates a confirmation key to be emailed to new user
        '''
        self.confirmation_key = create_hash(self.email_address)


    def _create_email_body_html(self):
        '''
        Creates the email from a template
        '''
        language = self.person.language

        translation.activate(language)

        content_html = get_template('email_confirmation/invite.html').render(
                        {
                            'language' : language,
                            'confirmation_key': self.confirmation_key,
                            'person_name' : self.person.name,
                            'user_who_invited_person' : self.user_who_invited_person.name,
                            'domain' : settings.DOMAIN
                        })


        return content_html


    def save(self, *args, **kwargs):
        '''
        Overrides the save method
        '''

        #New object
        if not self.id:
            self.generate_confirmation_key()

        #If not sent, send it
        if not self.sent:
            self.send_email()

        super(EmailConfirmation, self).save(*args, **kwargs) # Call the "real" save() method.

