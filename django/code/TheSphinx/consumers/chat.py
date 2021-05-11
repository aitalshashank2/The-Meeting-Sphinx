import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from TheSphinx.models import *
from TheSphinx.serializers import MeetingGetSerializer, MessageGetSerializer , UserGetSerializer

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def connect(self):
        self.meeting_code = self.scope['url_route']['kwargs']['meeting_code']
        self.user = self.scope['user']

        try:
            meeting = Meeting.objects.get(meeting_code = self.meeting_code)

            async_to_sync(self.channel_layer.group_add)(
                f'chat-{self.meeting_code}',
                self.channel_name
            )
            
            if self.user in meeting.banned.all():
                self.close()
                return
            elif (self.user not in meeting.attendees.all()) and (self.user not in meeting.organizers.all()):
                self.close()
                return

            self.accept()

            # SEND MEETING INFORMATION TO JOINED USER
            messages = Message.objects.filter(meeting_id=meeting.id).order_by('creation_time')
            message_send = {
                'data' : MessageGetSerializer(messages, many=True).data,
                'type' : "message_data",
            }
            self.send(text_data=json.dumps(message_send))
        
        except Exception as e:
            print("disconnecting from connect method")
            print("because", e)
            self.close()
    
    def disconnect(self, close_code):
        self.user = self.scope['user']

        async_to_sync(self.channel_layer.group_discard)(
            f'chat-{self.meeting_code}',
            self.channel_name
        )
    
    def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']

        try:
            meeting = Meeting.objects.get(meeting_code=self.meeting_code)
            message = Message(
                sender=self.user,
                content=content,
                meeting=meeting
            )
            message.save()

            serializer = MessageGetSerializer(message)
            print("received_sending")
            async_to_sync(self.channel_layer.group_send)(
                f'chat-{self.meeting_code}',
                {
                    'type': "send_message",
                    'data': {
                        'type': 'send_message',
                        'data': serializer.data
                    },
                }
            )
        except:
            self.close()
    
    def send_message(self, event):
        self.send(text_data=json.dumps(event['data']))
