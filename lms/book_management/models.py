import datetime as dt

from django.contrib.auth.models import User as Customer
from django.contrib.auth.models import User as Staff
from django.db import models


class Book(models.Model):
    """
    Book Model
    """
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    genre = models.CharField(max_length=200)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name.title()

    class Meta:
        ordering = ('id', )


class Issue(models.Model):
    """
    Issue Model
    table holding the book's issue
    """

    staff = models.ForeignKey(
        to=Staff,
        related_name='leases',
        on_delete=models.CASCADE)

    customer = models.ForeignKey(
        to=Customer,
        related_name='issues',
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        to=Book,
        related_name='issues',
        on_delete=models.CASCADE)

    issue_date = models.DateField()
    expected_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    fine = models.FloatField(default=0.00)

    def close_issue(self, returned_date):
        """ an issue is closed by returning a book. """

        days_spent = 0
        if returned_date > self.expected_date:
            days_spent = (returned_date - self.expected_date).days

        self.fine = self.price * 0.1
        self.fine = self.fine * days_spent
        self.return_date = returned_date

    @property
    def current_fine(self):
        return_date = self.return_date
        fine = 0
        price = 0

        if return_date is None:
            return_date = dt.date.today()

        days_spent = 0
        if return_date > self.expected_date:
            days_spent = (return_date - self.expected_date).days

        try:
            price = self.book.price
        except Exception:
            pass

        fine = price * 0.1
        return fine * days_spent

    def __repr__(self):
        pass

    class Meta:
        ordering = ('id', )
