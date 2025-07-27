from django.urls import path, include
from rest_framework import routers  # Import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # Use routers.DefaultRouter() explicitly
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

