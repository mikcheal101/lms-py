from django.db import models
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

    class Meta:
        ordering = ('id', )


class Issue(models.Model):
    """
    Issue Model
    table holding the book's issue
    """

    customer = models.ForeignKey(
        to=Customer,
        related_name='issues',
        on_delete=models.CASCADE)

    book = models.ForeignKey(
        to=Book,
        related_name='issues',
        on_delete=models.CASCADE)

    issue_date = models.DateField()
    return_date = models.DateField()

    period = models.IntegerField(default=1)
    fine = models.FloatField(default=100.00)
    """ fine per day """

    def __repr__(self):
        pass

    class Meta:
        ordering = ('id', )
