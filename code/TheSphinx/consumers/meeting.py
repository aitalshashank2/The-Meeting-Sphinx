import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from TheSphinx.models import *
from TheSphinx.serializers import MeetingGetSerializer, MessageGetSerializer , UserGetSerializer

class MeetingConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meeting_code = self.scope['url_route']['kwargs']['meeting_code']
    
    def connect(self):
        self.user = self.scope['user']
        print("connecting to the meeting")

        try:
            meeting = Meeting.objects.get(meeting_code = self.meeting_code)
            print("no issues")

            async_to_sync(self.channel_layer.group_add){
                self.meeting_code,
                self.channel_name
            }

            
            if self.user in user.banned.all() :
                self.close()
                return
            elif self.user not in user.attendees.all() and self.user not in user.organizers.all() :
                self.close()
                return

            print(self.meeting_code)
            print("connected to the meeting")

            self.accept()
            message_send = {
                'user' : MeetingGetSerializer(meeting).data,
                'type' : "meeting_data,
            } 
            self.send(text_data=json.dumps(message_send))

            serializer = UserGetSerializer(self.user)
            message_send = {
                'user' : serializer.data,
                'type' : "user_joined",
            } 
            async_to_sync(self.channel_layer.group_send)(
                self.meeting_code,
                {
                    'type': "send_user_info",
                    'message': message_send,
                }
            )
        
        except Meeting.DoesNotExist:
            self.close()
    
    def disconnect(self, close_code):
        self.user = self.scope['user']

        serializer = UserGetSerializer(self.user)
        message_send = {
            'user' : serializer.data,
            'type' : "user_left",
        } 
        async_to_sync(self.channel_layer.group_send)(
            self.meeting_code,
            {
                'type': "send_user_info",
                'message': message_send,
            }
        )

        try:
            meeting = Meeting.objects.get(meeting_code = self.meeting_code)
            attendees = meeting.attendees.all()

            if self.user in attendees :
                meeting.attendees.remove(self.user)

        except:
            self.close()
        
        async_to_sync(self.channel_layer.group_discard)(
            self.meeting_code,
            self.channel_name
        )
    
    def send_user_info(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        

    # def receive(self, text_data):
    #     print("received")
    #     message_data_json = json.loads(text_data)
    #     message_id = message_data_json['message_id']

    #     try:
    #         message = Message.objects.get(pk=message_id)
    #         meeting = message.meeting
            
    #         if(meeting.meeting_code == int(self.meeting_code)):
    #             print("meeting.meeting_code")
    #             print(meeting.meeting_code)

    #             serializer = MessageGetSerializer(message)
    #             async_to_sync(self.channel_layer.group_send)(
    #                 self.meeting_code,
    #                 {
    #                     'type': "send_message",
    #                     'message': serializer.data,
    #                 }
    #             )
    #     except Message.DoesNotExist:
    #         pass
    
    # def send_message(self, event):
    #     message = event['message']

    #     self.send(text_data=json.dumps(message))
