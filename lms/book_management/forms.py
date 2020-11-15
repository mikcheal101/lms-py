import datetime as dt

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User as Customer
from django.contrib.auth.models import User as Staff

from book_management.models import Book, Issue


class IssueForm(forms.ModelForm):

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_staff=False))

    staff = forms.ModelChoiceField(
        queryset=Staff.objects.filter(is_staff=True))

    book = forms.ModelChoiceField(
        queryset=Book.objects.all())

    issue_date = forms.DateField(
        initial=dt.date.today(),
        widget=forms.TextInput(attrs=dict(type='date')))

    class Meta:
        model = Issue
        fields = [
            'issue_date',
            'staff',
            'customer',
            'book', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Issue Book'))


class ReturnBookForm(forms.Form):
    pass


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'price', 'genre']
