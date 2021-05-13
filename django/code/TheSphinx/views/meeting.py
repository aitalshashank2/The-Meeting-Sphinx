import random
import string

from urllib.parse import urlparse

from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Meeting, Attendee
from TheSphinx.serializers import MeetingGetSerializer, MeetingPostSerializer
from TheSphinx.permissions import HasMeetingAccess


class MeetingViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return MeetingPostSerializer
        else:
            return MeetingGetSerializer

    # queryset = Meeting.objects.all().order_by('-start_time')

    def get_queryset(self):
        return self.request.user.meetings_organizing.all() | Meeting.objects.filter(attendees__user=self.request.user)

    permission_classes = [IsAuthenticated, HasMeetingAccess, ]
    lookup_field = 'meeting_code'

    def perform_create(self, serializer):
        meeting_code = ''.join(random.choice(
            string.ascii_lowercase) for _ in range(6))

        while True:
            try:
                clone = Meeting.objects.get(meeting_code=meeting_code)
                meeting_code = ''.join(random.choice(
                    string.ascii_lowercase) for _ in range(6))
            except Meeting.DoesNotExist:
                break

        # try:
        #     result = urlparse(serializer.validated_data['meeting_link'])
        #     valid = all([result.scheme, result.netloc, result.path])
        # except:
        #     valid = False

        # if not valid:
        #     meeting_link = "pasta"

        serializer.save(
            organizers=[self.request.user.pk, ],
            meeting_code=meeting_code,
            meeting_link=serializer.validated_data['meeting_link']
        )

        # else:
        #     serializer.save(
        #         organizers=[self.request.user.pk, ],
        #         meeting_code=meeting_code
        #     )

    @action(detail=False, methods=['post'])
    def join(self, request):
        code = request.data['meeting_code']

        user = request.user

        try:
            meeting = Meeting.objects.get(meeting_code=code)

            attendee_exists = False
            try:
                attendee = Attendee.objects.get(user=self.request.user, meeting=meeting, end_time=None)
                attendee_exists = True
            except Attendee.DoesNotExist:
                attendee_exists = False

            if user in meeting.banned.all():
                return Response({
                    'Detail': 'User is banned from this meeting',
                    'error': 1
                })
            elif attendee_exists:
                return Response({
                    'Detail': 'User is already in this meeting',
                    'meeting_code': code,
                    'error': -3
                })
            elif user in meeting.organizers.all():
                return Response({
                    'Detail': 'User is already organiser of this meeting',
                    'meeting_code': code,
                    'error': -2
                })
            else:
                # Join
                attendee = Attendee(
                    user=self.request.user,
                    meeting=meeting,
                )
                attendee.save()
                return Response({
                    'Detail': 'User added to meeting attendees',
                    'meeting_code': code,
                    'error': -1
                })

        except Meeting.DoesNotExist:
            return Response({
                'Detail': 'Invalid meeting code',
                'error': 2
            })

        # POSITIVE ERROR CODES ARE ERROS, NEGATIVE ARE NOT
