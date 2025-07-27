from django.urls import path, include
from rest_framework_nested import routers  # ✅ change this
from .views import ConversationViewSet, MessageViewSet

router = routers.NestedDefaultRouter()  # ✅ change this
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

