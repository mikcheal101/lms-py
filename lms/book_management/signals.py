from django.db.models.signals import post_save
from django.dispatch import receiver

from book_management.models import Issue
import datetime as dt

@receiver(post_save, sender=Issue)
def save_issue_event(sender, instance, created, **kwargs):
    if created:
        expected_date = instance.
