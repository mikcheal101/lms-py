from django.db import models
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer


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
    expected_date = models.DateField(default=1)
    return_date = models.DateField(blank=True, null=True)
    fine = models.FloatField(default=0.00)

    def close_issue(self, returned_date, fine_per_day):
        """ an issue is closed by returning a book. """

        days_spent = 0
        if returned_date > self.expected_date:
            days_spent = (returned_date - self.expected_date).days

        self.fine = fine_per_day * days_spent
        self.return_date = returned_date

    def __repr__(self):
        pass

    class Meta:
        ordering = ('id', )
