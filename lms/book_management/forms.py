from django import forms
from book_management.models import Book, Issue
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer


class IssueForm(forms.ModelForm):

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_staff=False))

    staff = forms.ModelChoiceField(
        queryset=Staff.objects.filter(is_staff=True))

    book = forms.ModelChoiceField(
        queryset=Book.objects.all())

    class Meta:
        model = Issue
        fields = [
            'issue_date',
            'expected_date',
            'return_date',
            'fine',
            'customer',
            'book', ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'price', 'genre']
