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

    class Meta:
        ordering = ('id', )
