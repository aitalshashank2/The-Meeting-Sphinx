from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from TheSphinx.models import Recording, Meeting
from TheSphinx.serializers import RecordingGetSerializer, RecordingPostSerializer
from TheSphinx.permissions import IsInSafeMethods


class RecordingViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return RecordingPostSerializer
        else:
            return RecordingGetSerializer

    queryset = Recording.objects.all()
    permission_classes = [IsAuthenticated, IsInSafeMethods, ]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
