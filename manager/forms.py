from django import forms
from manager.models import Account


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        widgets = {'passwd': forms.PasswordInput(),}