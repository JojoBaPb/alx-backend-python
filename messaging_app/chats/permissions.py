from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj can be a Message or Conversation depending on the view
        try:
            conversation = obj.conversation if hasattr(obj, 'conversation') else obj
            return request.user in conversation.participants.all()
        except AttributeError:
            return False

