from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Attendee
from TheSphinx.serializers import AttendeeGetSerializer, AttendeePostSerializer
from TheSphinx.permissions import IsInSafeMethods


class AttendeeViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return AttendeePostSerializer
        else:
            return AttendeeGetSerializer

    queryset = Attendee.objects.all()
    permission_classes = [IsAuthenticated, IsInSafeMethods, ]

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user
        )
