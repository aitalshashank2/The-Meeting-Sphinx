from django.db import models
from django.conf import settings


class Meeting(models.Model):
    """
    This model represents all the meeting instances in our project
    """

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    organizers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='meetings_organizing',
        blank=False
    )

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='meetings_attending',
        blank=True
    )

    banned = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='meetings_banned',
        blank=True
    )

    start_time = models.DateTimeField(
        auto_now_add=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    meeting_code = models.CharField(
        max_length=6,
        null=False,
        blank=False
    )

    meeting_link = models.CharField(
        max_length=1023,
        null=True,
    )


    def __str__(self):
        return f"Meeting: {self.title}"
