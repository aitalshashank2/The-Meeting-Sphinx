from django.db import models
from django.conf import settings

from TheSphinx.models import Meeting


class Attendee(models.Model):
    """
    This model represents an Attendee instance
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='attendee_roles',
    )

    meeting = models.ForeignKey(
        Meeting,
        null=False,
        on_delete=models.CASCADE,
        related_name='attendees'
    )

    start_time = models.DateTimeField(
        auto_now_add=True,
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )
