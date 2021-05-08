from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from TheSphinx.models import Message
from TheSphinx.serializers import MessageGetSerializer, MessagePostSerializer
from TheSphinx.permissions import HasMessageAccess

class MessageViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return MessagePostSerializer
        else:
            return MessageGetSerializer
    
    def get_queryset(self):
        return self.request.user.message_set.all()

    permission_classes = [IsAuthenticated, HasMessageAccess, ]

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
        )
