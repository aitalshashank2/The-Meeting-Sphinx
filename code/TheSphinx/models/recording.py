from django.db import models
from django.conf import settings

from TheSphinx.models import Meeting


class Recording(models.Model):
    """
    This model represents a recording instance
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name='recordings',
    )

    meeting = models.ForeignKey(
        Meeting,
        null=False,
        on_delete=models.CASCADE,
        related_name='recordings',
    )

    start_time = models.DateTimeField(
        auto_now_add=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )
