from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from TheSphinx.models import *
from TheSphinx.serializers import MeetingGetSerializer, MessageGetSerializer , UserGetSerializer

class MeetingConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def connect(self):
        self.meeting_code = self.scope['url_route']['kwargs']['meeting_code']
        self.user = self.scope['user']

        try:
            meeting = Meeting.objects.get(meeting_code = self.meeting_code)

            async_to_sync(self.channel_layer.group_add)(
                self.meeting_code,
                self.channel_name
            )
            
            if self.user in meeting.banned.all():
                self.close()
                return
            elif (self.user not in meeting.organizers.all()):
                attendee = Attendee.objects.get(user=self.user, meeting=meeting, end_time=None)
                if (attendee not in meeting.attendees.all()):
                    self.close()
                    return
            
            self.accept()

            # SEND MEETING INFORMATION TO JOINED USER
            message_send = {
                'data' : MeetingGetSerializer(meeting).data,
                'type' : "meeting_data",
            } 
            self.send(text_data=json.dumps(message_send))

            # SEND NEW USER INFORMATION TO EVERYONE IN THE MEETING
            message_data = {}
            message_data['user_data'] = UserGetSerializer(self.user).data
            message_data['rights'] = None
            if self.user in meeting.organizers.all():
                message_data['rights'] = 'Organiser'
            else:
                message_data['rights'] = 'Attendee'

            message_send = {
                'data' : message_data,
                'type' : "user_joined",
            } 
            async_to_sync(self.channel_layer.group_send)(
                self.meeting_code,
                {
                    'type': "send_user_info",
                    'message': message_send,
                }
            )

            try:
                r = Recording.objects.get(user = self.user, end_time=None)
                is_recording = True
            except Recording.DoesNotExist:
                is_recording = False

            if is_recording:
                async_to_sync(self.channel_layer.group_send)(
                    self.meeting_code,
                    {
                        'type': "user_recrd_start",
                    }
                )
                
            if r.meeting != meeting:
                r.end_time = datetime.now()
                r.save()

                r = Recording(
                    user = self.user,
                    meeting = meeting
                )
                r.save()
        
        except Meeting.DoesNotExist:
            print("meeting not found")
            self.close()
        
        except Attendee.DoesNotExist:
            print("attendee not found")
            self.close()
    
    def disconnect(self, close_code):
        message_send = {
            'data' : UserGetSerializer(self.user).data,
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
            meeting = Meeting.objects.get(meeting_code=self.meeting_code)
            attendee = Attendee.objects.get(user=self.user, meeting=meeting, end_time=None)
            attendees = meeting.attendees.all()

            if attendee in attendees :
                attendee.end_time = datetime.now()
                attendee.save()
            elif self.user in meeting.organizers.all():
                message_send = {
                    'data' : '',
                    'type' : "organiser_left",
                } 
                async_to_sync(self.channel_layer.group_send)(
                    self.meeting_code,
                    {
                        'type': "send_user_info",
                        'message': message_send,
                    }
                )
                meeting.meeting_code = ""
                meeting.end_time = datetime.now()
                meeting.save()
                
        except:
            self.close()
        
        async_to_sync(self.channel_layer.group_discard)(
            self.meeting_code,
            self.channel_name
        )
    
    def send_user_info(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        