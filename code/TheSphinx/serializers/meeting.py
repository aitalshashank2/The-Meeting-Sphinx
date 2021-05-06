from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from TheSphinx.models import Meeting
from TheSphinx.serializers import UserGetSerializer


class MeetingGetSerializer(ModelSerializer):
    organizers = UserGetSerializer(read_only=True, many=True)
    attendees = UserGetSerializer(read_only=True, many=True)

    class Meta:
        model = Meeting
        depth = 1
        fields = [
            'id',
            'title',
            'organizers',
            'attendees',
            'attendees_recording',
            'start_time',
            'end_time',
            'meeting_code',
            'meeting_link',
        ]
        read_only_fields = [
            'id',
            'title',
            'organizers',
            'attendees',
            'attendees_recording',
            'start_time',
            'end_time',
            'meeting_code',
            'meeting_link',
        ]

class MeetingPostSerializer(ModelSerializer):
    class Meta:
        model = Meeting
        fields = [
            'id',
            'title',
            'organizers',
            'attendees',
            'start_time',
            'meeting_code',
            'meeting_link',
        ]
        read_only_fields = [
            'id',
            'organizers',
            'start_time',
            'meeting_code',
        ]
