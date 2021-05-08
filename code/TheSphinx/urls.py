from django.urls import path
from rest_framework import routers

from TheSphinx.views import *

router = routers.SimpleRouter()

router.register(r'auth', AuthViewSet)
router.register(r'meeting', MeetingViewSet, basename="meeting")
router.register(r'message', MessageViewSet, basename="message")
router.register(r'recording', RecordingViewSet)

urlpatterns = []

urlpatterns += router.urls
