from rest_framework.serializers import ModelSerializer

from TheSphinx.models import Recording
from TheSphinx.serializers import UserGetSerializer, MeetingGetSerializer


class RecordingGetSerializer(ModelSerializer):
    """
    Verbose serializer for Recording model to be used in GET METHOD
    """ 
    user = UserGetSerializer()
    meeting = MeetingGetSerializer()

    class Meta:
        model = Recording
        depth = 1
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
            'meeting',
            'start_time',
            'end_time',
        ]

class RecordingPostSerializer(ModelSerializer):
    """
    Serializer for Recording model to be used in POST METHOD
    """
    class Meta:
        model = Recording
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
