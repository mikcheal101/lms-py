from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer
from django.core.exceptions import ValidationError


class SigninForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(
        max_length=200, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(
            username=cleaned_data['username'],
            password=cleaned_data['password'])

        if user is None:
            raise ValidationError("Unrecognized user!")


class StaffForm(forms.Form):
    class Meta:
        model = Staff
        fields = ['username', 'email', ]


class CustomerForm(forms.Form):
    class Meta:
        model = Customer
        fields = ['username', 'email', ]
