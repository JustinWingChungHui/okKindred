from django.db import models
from django.utils import translation
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from common import create_hash


class EmailConfirmationManager(models.Manager):
    '''
    Email confirmation custom manager
    '''
    def remove_expired_email_confirmations(self):
        '''
        Remove all pending email confirmations that are over a week old
        '''
        d = timezone.now() - timedelta(days=7)
        self.filter(sent__lte = d).delete()



# based on https://code.google.com/p/django-email-confirmation/source/browse/trunk/devproject/emailconfirmation/models.py
# and https://github.com/pinax/django-user-accounts/

class EmailConfirmation(models.Model):
    '''
    Represents an email confirmation sent out to confirm joining website
    '''

    email_address = models.EmailField(null=False, unique=True)
    person = models.ForeignKey('family_tree.Person', null=True, db_index = True, unique=True) #Use of model string name to prevent circular import
    sent = models.DateTimeField(db_index = True)
    confirmation_key = models.CharField(max_length=64, db_index = True, unique=True)
    user_who_invited_person = models.ForeignKey('custom_user.User', null=False) #Use of model string name to prevent circular import

    objects = EmailConfirmationManager()

    def __str__(self):
        return self.person.name + " " + self.email_address

    def send_email(self):

        language = self.person.language
        translation.activate(language)

        subject = translation.ugettext('An invitation to ok!Kindred from {0}').format(self.user_who_invited_person.name)

        content = translation.ugettext( """Hi {0}
                                            You have been invited by {1} to join ok!Kindred.
                                            ok!Kindred is a collaborative family tree and private social network for you and you family.
                                            A network has already been set up by one of your family members to help you keep in touch.
                                            To join, please go to https://www.okkindred.com/accounts/confirmation={2}/
                                        """.format(self.person.name, self.user_who_invited_person.name, self.confirmation_key))

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
                        Context({
                                    'language' : language,
                                    'confirmation_key': self.confirmation_key,
                                    'person_name' : self.person.name,
                                    'user_who_invited_person' : self.user_who_invited_person.name,
                                })
                        )


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

