import datetime as dt

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User as Customer
from django.contrib.auth.models import User as Staff

from book_management.models import Book, Issue


class IssueForm(forms.ModelForm):
    period = forms.IntegerField(initial=1, label='Duration (days)')
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_staff=False))

    staff = forms.ModelChoiceField(
        queryset=Staff.objects.filter(is_staff=True))

    book = forms.ModelChoiceField(
        queryset=Book.objects.all())

    issue_date = forms.DateField(
        initial=dt.date.today(),
        widget=forms.TextInput(attrs=dict(type='date')))

    def save(self):
        try:
            instance = Issue()
            instance.book = self.cleaned_data['book']
            instance.staff = self.cleaned_data['staff']
            instance.customer = self.cleaned_data['customer']
            instance.issue_date = self.cleaned_data['issue_date']
            instance.expected_date = self.cleaned_data['issue_date']
            instance.expected_date += dt.timedelta(
                days=self.cleaned_data['period'])
            instance.save()
            return instance
        except Exception as e:
            print(e)
            print('saving')
            return None

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


class ReturnBookForm(forms.ModelForm):

    customer = forms.ModelChoiceField(
        disabled=True,
        queryset=Customer.objects.filter(is_staff=False))

    staff = forms.ModelChoiceField(
        disabled=True,
        queryset=Staff.objects.filter(is_staff=True))

    book = forms.ModelChoiceField(
        disabled=True,
        queryset=Book.objects.all())

    issue_date = forms.DateField(
        initial=dt.date.today(), disabled=True,
        widget=forms.TextInput(attrs=dict(type='date')))
    expected_date = forms.DateField(
        initial=dt.date.today(), disabled=True,
        widget=forms.TextInput(attrs=dict(type='date')))
    return_date = forms.DateField(
        initial=dt.date.today(),
        disabled=True,
        widget=forms.TextInput(attrs=dict(type='date')))

    current_fine = forms.CharField(
        initial=0, disabled=True)

    def save(self):
        try:
            self.instance.book = self.cleaned_data['book']
            self.instance.staff = self.cleaned_data['staff']
            self.instance.customer = self.cleaned_data['customer']
            self.instance.issue_date = self.cleaned_data['issue_date']
            self.instance.fine = float(
                self.cleaned_data['current_fine'].replace(',', ''))
            self.instance.return_date = self.cleaned_data['return_date']
            self.instance.expected_date = self.cleaned_data['expected_date']

            self.instance.save()
            return self.instance
        except Exception as e:
            print(e)
            return None

    class Meta:
        model = Issue
        fields = [
            'issue_date',
            'staff',
            'expected_date',
            'customer',
            'book', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = "{:,}".format(kwargs['instance'].current_fine)
        self.fields['current_fine'].initial = initial
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Return Book'))


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'price', 'genre']
