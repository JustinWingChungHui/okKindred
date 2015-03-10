from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = UserManager.normalize_email(email).lower()
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u




class User(AbstractBaseUser):
    '''
    Defines a custom user model so that the username is the email address
    https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#specifying-a-custom-user-model
    http://stackoverflow.com/questions/16638414/set-email-as-username-in-django-1-5
    '''

    email = models.EmailField(_('Email Address'), unique=True, db_index = True)
    name = models.CharField(_('Name'), max_length=255, null = False, blank = False)
    is_staff = models.BooleanField(_('Staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_superuser = models.BooleanField(_('Superuser'), default=False, help_text=_('Designates whether the user is superuser'))
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('Date Joined'),auto_now_add=True)

    family = models.ForeignKey('family_tree.Family', null=True, db_index = True) #Use of model string name to prevent circular import
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, null = False, blank = False, default='en', db_index = True)

    receive_update_emails = models.BooleanField(_('Receive Update Emails'), default=True, help_text=_('Sends out emails if family has been updated'))


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] #should not contain the USERNAME_FIELD or password as these fields will always be prompted for.

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: yes, if superuser
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: yes, if superuser
        return self.is_superuser

    def save(self, *args, **kwargs):
        '''
        Overrides the save method to determine the calculated fields
        '''
        self.is_staff = self.is_superuser

        #Update profile language
        from family_tree.models import Person

        if self.id is not None and self.id > 0:
            try:
                person = Person.objects.get(user_id=self.id)
                if person.language != self.language:
                    person.language = self.language
                    person.save_person_only()
            except:
                pass

        super(User, self).save(*args, **kwargs) # Call the "real" save() method.

    def save_user_only(self, *args, **kwargs):
        '''
        Call to just save user with no extra stuff
        '''
        super(User, self).save(*args, **kwargs) # Call the "real" save() method.
