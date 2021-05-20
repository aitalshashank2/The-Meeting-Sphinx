import json
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from TheSphinx.models import *
from TheSphinx.serializers import MeetingGetSerializer, MessageGetSerializer, UserGetSerializer, UserIDSerializer


class VideoCallConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__()

    def connect(self):
        self.meeting_code = self.scope['url_route']['kwargs']['meeting_code']
        self.user = self.scope['user']

        try:
            meeting = Meeting.objects.get(meeting_code=self.meeting_code)

            async_to_sync(self.channel_layer.group_add)(
                f'video-{self.meeting_code}',
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
            user_ids = []
            for o in meeting.organizers.all():
                user_ids.append(o.id)
            for a in meeting.attendees.all():
                user_ids.append(a.user.id)

            message_send = {
                'data': user_ids,
                'type': "all_users",
            }
            self.send(text_data=json.dumps(message_send))

            message_send = {
                'data': user_ids,
                'type': "user_joined",
            }
            async_to_sync(self.channel_layer.group_send)(
                f'video-{self.meeting_code}',
                {
                    'type': "send_user_info",
                    'message': message_send,
                }
            )

        except Meeting.DoesNotExist:
            print("meeting not found")
            self.close()

        except Attendee.DoesNotExist:
            print("attendee not found")
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            f'video-{self.meeting_code}',
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get('type')
        data = data.get('data')

        # types = {
        #     'call_user': 'hey',
        #     'accept_call': 'call_accepted',
        #     'user_turned_off_video':'user_turned_off_video'
        # }
        message_send = {
            'data': data,
            'type': type
        }

        async_to_sync(self.channel_layer.group_send)(
            f'video-{self.meeting_code}',
            {
                'type': "send_user_info",
                'message': message_send,
            }
        )

    def send_user_info(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))


    # if type == 'call_user':
    #     message_send = {
    #         'data': data,
    #         'type': 'hey'
    #     }
    # elif type == 'accept_call':
    #     message_send = {
    #         'data': data,
    #         'type': 'call_accepted'
    #     }
    # elif type == 'user_turned_off_video':
    #     message_send = {
    #         'data': data,
    #         'type': 'user_turned_off_video'
    #     }