from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import translation, timezone
from django.template import Context
from django.template.loader import get_template

from common.utils import create_hash
from family_tree.models.person import GENDER_CHOICES
from custom_user.models import User
from family_tree.models import Family, Person

class SignUpManager(models.Manager):
    '''
    Sign Up custom manager
    '''
    def remove_expired_sign_ups(self, days=28):
        '''
        Remove all pending Sign Ups that are over 4 weeks old
        '''
        d = timezone.now() - timedelta(days)
        self.filter(creation_date__lte = d).delete()


class SignUp(models.Model):
    '''
    Represents a new sign up to the website
    '''
    name = models.CharField(max_length=255, null = False, blank = False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = False, blank = False)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null = False, blank = False, default='en')
    email_address = models.EmailField(null=False, unique=True)
    confirmation_key = models.CharField(max_length=64, db_index = True, unique=True, blank = False)
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = SignUpManager()

    def __str__(self): # __unicode__ on Python 2
        return self.email_address



    def complete_registration(self, password):
        '''
        Completes the registration of the new sign up
        '''

        # Create a new family, user and person
        family = Family.objects.create(description = self.email_address)

        user = User.objects.create_user(
                        email=self.email_address,
                        password=password,
                        name=self.name,
                        family_id=family.id,
                        language=self.language)

        Person.objects.create(
                        name = self.name,
                        gender = self.gender,
                        family = family,
                        language = self.language,
                        user = user,
                        email=self.email_address)

        # Delete sign up
        self.delete()

        return user

    def save(self, *args, **kwargs):
        '''
        Overrides the save method
        '''
        #New object
        if not self.id:

            #Check email does not already exist

            self.confirmation_key = create_hash(self.email_address)
            self.send_email()

        super(SignUp, self).save(*args, **kwargs) # Call the "real" save() method.


    def send_email(self):
        '''
        Sends registration confirmation email
        '''

        language = self.language
        translation.activate(language)

        subject = translation.ugettext('ok!Kindred sign up confirmation')

        content = translation.ugettext( """Hi {0}
                                            To confirm your sign up, please go to {1}/accounts/sign_up_confirmation={2}/
                                        """.format(self.name, settings.DOMAIN, self.confirmation_key))

        content_html = self._create_email_body_html()


        send_mail(subject, content, 'info@okkindred.com',[self.email_address], fail_silently=False, html_message=content_html)


    def _create_email_body_html(self):
        '''
        Creates the email from a template
        '''
        language = self.language
        translation.activate(language)

        content_html = get_template('sign_up/confirmation_email.html').render(
                        Context({
                                    'language' : language,
                                    'confirmation_key': self.confirmation_key,
                                    'person_name' : self.name,
                                    'domain' : settings.DOMAIN
                                })
                        )


        return content_html