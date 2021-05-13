from django.db.models import fields
from rest_framework.serializers import ModelSerializer, Serializer

from TheSphinx.models import Message
from TheSphinx.serializers import UserGetSerializer, MeetingGetSerializer

class MessageSerializer(ModelSerializer):
    
    sender = UserGetSerializer()
    
    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'content',
            'creation_time'
        ]
        read_only_fields = [
            'id',
            'sender',
            'content',
            'creation_time'
        ]

class MessageGetSerializer:
    """
    Verbose serializer for Message model to be used in GET METHOD
    """

    def __init__(self, object, many=False, context=None):
        if many:
            self.data = []
            for m in object:
                self.data.append({
                    'message': MessageSerializer(m).data,
                    'type': 'chat'
                })
        else:
            self.data = {
                'message': MessageSerializer(object).data,
                'type': 'chat'
            }
    


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
