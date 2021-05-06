from django.urls import path
from rest_framework import routers
from TheSphinx.views import *

router = routers.SimpleRouter()

router.register(r'auth', AuthViewSet)
router.register(r'meeting', MeetingViewSet)

urlpatterns = []

urlpatterns += router.urls
