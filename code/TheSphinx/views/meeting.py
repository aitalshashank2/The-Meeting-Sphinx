import random
import string

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Meeting
from TheSphinx.serializers import MeetingGetSerializer, MeetingPostSerializer

class MeetingViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return MeetingPostSerializer
        else:
            return MeetingGetSerializer

    queryset = Meeting.objects.all().order_by('-start_time')
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'meeting_code'

    def perform_create(self, serializer):
        meeting_code = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        
        while True:
            try:
                clone = Meeting.objects.get(meeting_code=meeting_code)
                meeting_code = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
            except Meeting.DoesNotExist:
                break
        
        if not serializer.validated_data["meeting_link"]:
            meeting_link = "/api/meeting/" + meeting_code

            serializer.save(
                organizers = [self.request.user.pk, ],
                meeting_code = meeting_code,
                meeting_link = meeting_link
            )
        else:
            serializer.save(
                organizers = [self.request.user.pk, ],
                meeting_code = meeting_code
            )
