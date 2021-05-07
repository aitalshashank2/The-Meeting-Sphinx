from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Message
from TheSphinx.serializers import MessageGetSerializer, MessagePostSerializer

class MessageViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return MessagePostSerializer
        else:
            return MessageGetSerializer
    
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
        )
