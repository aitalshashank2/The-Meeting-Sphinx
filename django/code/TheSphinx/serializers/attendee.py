from rest_framework.serializers import ModelSerializer

from TheSphinx.models import Attendee
from TheSphinx.serializers import UserGetSerializer


class AttendeeGetSerializer(ModelSerializer):
    """
    Verbose serializer for Attendee model to be used in GET method
    """
    user = UserGetSerializer()

    class Meta:
        model = Attendee
        fields = [
            'id',
            'user',
            'meeting',
            'start_time',
            'end_time'
        ]
        read_only_fields = [
            'id',
            'user',
            'meeting',
            'start_time',
            'end_time',
        ]


class AttendeePostSerializer(ModelSerializer):
    """
    Serializer for Attendee Model to be used in POST method
    """
    class Meta:
        model = Attendee
        fields = [
            'id',
            'user',
            'meeting',
            'start_time',
            'end_time',
        ]
        read_only_fields = [
            'id',
            'user',
            'start_time',
            'end_time',
        ]
