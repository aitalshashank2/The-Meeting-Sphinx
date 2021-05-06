from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Recording
from TheSphinx.serializers import RecordingGetSerializer, RecordingPostSerializer


class RecordingViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return RecordingPostSerializer
        else:
            return RecordingGetSerializer

    queryset = Recording.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
