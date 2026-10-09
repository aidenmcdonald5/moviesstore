from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import Profile
from .regions import REGION_CHOICES

class CustomErrorList(ErrorList):
    def __str__(self): 
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True, label='Region')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
        self.fields['region'].widget.attrs.update({'class': 'form-select'})
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=commit)
        if commit:
            Profile.objects.create(user=user, region=self.cleaned_data['region'])
        return user