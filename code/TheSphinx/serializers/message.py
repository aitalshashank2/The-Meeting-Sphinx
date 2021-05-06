from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from TheSphinx.models import Message

class MessageGetSerializer(ModelSerializer):
    """
    Verbose serializer for Message model to be used in GET METHOD
    """
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

class MessagePostSerialzier(ModelSerializer):
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
