from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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


class CreateStaffForm(forms.Form):
    email = forms.EmailField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(
        max_length=200, widget=forms.PasswordInput)

    def save(self):
        try:
            instance = Staff.objects.create_user(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                is_active=True,
                is_staff=True)
            instance.save()
        except Exception:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args,  **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit',  'Save Staff'))


class CreateCustomerForm(forms.Form):
    email = forms.EmailField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(
        max_length=200, widget=forms.PasswordInput)

    def save(self):
        try:
            instance = Customer.objects.create_user(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                is_active=True)
            instance.save()
        except Exception:
            pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args,  **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit',  'Save Customer'))


class StaffForm(forms.Form):
    class Meta:
        model = Staff
        fields = ['username', 'email', ]


class CustomerForm(forms.Form):
    class Meta:
        model = Customer
        fields = ['username', 'email', ]
