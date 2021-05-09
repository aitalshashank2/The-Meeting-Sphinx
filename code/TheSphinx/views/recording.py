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
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        try:
            code = request.data['meeting_code']
        except KeyError:
            return Response("Meeting Code Not Provided!", status=400)
        try:
            m = Meeting.objects.get(meeting_code=code)
        except Meeting.DoesNotExist:
            return Response("No such meeting exists!", status=404)
            
        r = Recording(
            user=request.user,
            meeting=m,
        )
        r.save()

        return Response({
            'data': f'User {request.user.username} banned from {code}'
        }, status=202)

    @action(detail=True, methods=['get'])
    def stop(self, request, pk):
        try:
            r = Recording.objects.get(pk=pk)
        except Recording.DoesNotExist:
            return Response("No such recording instance exists!",status=404)
        
        r.end_time = datetime.now()
        r.save()
        return Response(f"Recording {r.id} stopped by user!",status=200)
