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
    
    @action(detail=False, methods=['get'])
    def start(self, request):
        return Response(f'{request.user.full_name}, you have reached hit start')

    @action(detail=False, methods=['get'])
    def stop(self, request):
        return Response(f'{request.user.full_name}, you have reached stop')

    @action(detail=False, methods=['get'])
    def test(self, request):
        return Response(request.user.full_name, status=200)
