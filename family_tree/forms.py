from django import forms
from django.utils.translation import ugettext_lazy as _
from family_tree.models.person import GENDER_CHOICES

class ProfileForm(forms.Form):
    '''
    Form to edit someones profile
    '''
    name = forms.CharField(label=_('Name'), max_length=255)
    gender = forms.TypedChoiceField(choices = GENDER_CHOICES)