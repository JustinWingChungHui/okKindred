from django import forms

class BiographyForm(forms.Form):
    '''
    Form to edit someones biography
    '''
    content = forms.Charfield()