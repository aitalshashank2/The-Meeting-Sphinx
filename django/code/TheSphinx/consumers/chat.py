from datetime import datetime
import json
from datetime import date, datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from TheSphinx.models import *
from TheSphinx.serializers import MeetingGetSerializer, MessageGetSerializer , UserGetSerializer
from TheSphinx.serializers.recording import RecordingGetSerializer

from django.db.models import Q

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def connect(self):
        self.meeting_code = self.scope['url_route']['kwargs']['meeting_code']
        self.user = self.scope['user']

        if self.meeting_code == "gg":
            try:
                self.gg = Meeting.objects.get(meeting_code="gg")
            except Meeting.DoesNotExist:
                self.gg = Meeting(
                    title="GG",
                    meeting_code="gg"
                )
                self.gg.save()
                self.gg.organizers.add(User.objects.get(is_superuser = True))
                self.gg.save()
            
            try:
                a = Attendee.objects.get(user = self.user, meeting = self.gg, end_time = None)
            except Attendee.DoesNotExist:
                a = Attendee(
                    user=self.user,
                    meeting=self.gg
                )
                a.save()

        
        try:
            meeting = Meeting.objects.get(meeting_code = self.meeting_code)

            async_to_sync(self.channel_layer.group_add)(
                f'chat-{self.meeting_code}',
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
            messages = Message.objects.filter(meeting_id=meeting.id).order_by('creation_time')
            message_send = {
                'data' : MessageGetSerializer(messages, many=True).data,
                'type' : "message_data",
            }
            self.send(text_data=json.dumps(message_send))
        
            r = Recording.objects.filter(Q(user = self.user) & Q(end_time = None) & ~Q(meeting = meeting))
            is_recording = (len(r) > 0)
            if is_recording:
                async_to_sync(self.channel_layer.group_send)(
                    f'chat-{self.meeting_code}',
                    {
                        'type': "send_message",
                        'data': {
                            'type': "user_recrd_start",
                            'data': RecordingGetSerializer(r.first()).data,
                        }
                    }
                )
                for x in r:
                    if x.meeting != meeting:
                        x.end_time = datetime.now()
                        x.save()
                try:
                    r1 = Recording.objects.get(user = self.user, meeting = meeting, end_time = None)
                except Recording.DoesNotExist:
                    r1 = Recording(
                        user = self.user,
                        meeting = meeting,
                    )
                    r1.save()
        
        except Exception as e:
            print("disconnecting from connect method")
            print(f"because, my meeting code is {self.meeting_code}", e)
            self.close()
    
    def disconnect(self, close_code):
        self.user = self.scope['user']

        async_to_sync(self.channel_layer.group_discard)(
            f'chat-{self.meeting_code}',
            self.channel_name
        )
    
    def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('content', None)
        data_type = data.get('type', None)

        if content:
            try:
                meeting = Meeting.objects.get(meeting_code=self.meeting_code)
                message = Message(
                    sender=self.user,
                    content=content,
                    meeting=meeting
                )
                message.save()

                serializer = MessageGetSerializer(message)
                
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
        elif data_type:
            print("data_type", data_type)
            try:
                meeting = Meeting.objects.get(meeting_code=self.meeting_code)

                if data['type'] == "user_recrd_start":
                    r = Recording(
                        user = self.user,
                        meeting = meeting
                    )
                    r.save()
                    async_to_sync(self.channel_layer.group_send)(
                        f'chat-{self.meeting_code}',
                        {
                            'type': "send_message",
                            'data': {
                                'type': 'user_recrd_start',
                                'data': RecordingGetSerializer(r).data
                            },
                        }
                    )

                elif data['type'] == "user_recrd_stop":
                    try:
                        r = Recording.objects.filter(user=self.user, meeting=meeting, end_time=None)
                        print(r)
                        if len(r) == 0:
                            raise

                        x = r.first()
                        x.end_time = datetime.now()
                        x.save()
                        print(RecordingGetSerializer(x).data)

                        async_to_sync(self.channel_layer.group_send)(
                            f'chat-{self.meeting_code}',
                            {
                                'type': "send_message",
                                'data': {
                                    'type': 'user_recrd_stop',
                                    'data': RecordingGetSerializer(x).data
                                },
                            }
                        )

                    except:
                        r = Recording(
                            user=self.user,
                            meeting=meeting,
                            end_time=datetime.now()
                        )
                        r.save()
                        async_to_sync(self.channel_layer.group_send)(
                            f'chat-{self.meeting_code}',
                            {
                                'type': "send_message",
                                'data': {
                                    'type': 'user_recrd_stop',
                                    'data': RecordingGetSerializer(r).data
                                },
                            }
                        )
                    
            except Exception as e:
                print("disconnecting from receive method")
                print(f"because, my meeting code is {self.meeting_code}", e)
            
                
            else:
                print(data['type'])
        else:
            pass
        
    
    def send_message(self, event):
        self.send(text_data=json.dumps(event['data']))
