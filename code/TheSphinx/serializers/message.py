from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from TheSphinx.models import Message

class MessageGetSerializer(ModelSerializer):
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
