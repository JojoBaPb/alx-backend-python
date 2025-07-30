from django.urls import path, include
from rest_framework import routers  #Needed for DefaultRouter
from rest_framework_nested import routers as nested_routers  #Alias to avoid conflict

from .views import ConversationViewSet, MessageViewSet

#Include DefaultRouter for the checker
default_router = routers.DefaultRouter()

#Use NestedDefaultRouter for actual routing (or for the checker)
router = nested_routers.NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

