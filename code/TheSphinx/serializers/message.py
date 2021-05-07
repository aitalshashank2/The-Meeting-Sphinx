from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from TheSphinx.models import Message
from TheSphinx.serializers import UserGetSerializer, MeetingGetSerializer

class MessageGetSerializer(ModelSerializer):
    """
    Verbose serializer for Message model to be used in GET METHOD
    """
    sender = UserGetSerializer()
    meeting = MeetingGetSerializer()
    class Meta:
        model = Message
        depth = 1
        fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'creation_time',
        ]
        read_only_fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'creation_time',
        ]

class MessagePostSerializer(ModelSerializer):
    """
    Serializer for Message model to be used in POST METHOD
    """
    class Meta:
        model = Message
        fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'creation_time',
        ]
        read_only_fields = [
            'id',
            'sender',
            'creation_time',
        ]
