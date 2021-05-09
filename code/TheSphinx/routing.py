from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/meetings/(?P<meeting_code>\w+)/$', consumers.MeetingConsumer.as_asgi()),
    re_path(r'ws/meetings/(?P<meeting_code>\w+)/chat/$', consumers.ChatConsumer.as_asgi()),
]
