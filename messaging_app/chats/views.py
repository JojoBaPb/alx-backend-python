from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import CustomPagination

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # Only show messages for conversations the user is a participant in
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if self.request.user in conversation.participants.all():
                    return Message.objects.filter(conversation=conversation)
                else:
                    return Message.objects.none()
            except Conversation.DoesNotExist:
                return Message.objects.none()
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)
