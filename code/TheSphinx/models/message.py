from django.db import models
from django.conf import settings

from TheSphinx.models import Meeting


class Message(models.Model):
    """
    This model implements a message in live chat
    """

    meeting = models.ForeignKey(
        Meeting,
        null=False,
        on_delete=models.CASCADE,
        related_name='all_messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
    )

    content = models.CharField(
        max_length=2055,
        null=False,
        blank=False
    )

    creation_time = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Comment: By {str(self.sender)}, at time {str(self.creation_time)}"
    