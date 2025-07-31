from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTest(TestCase):
    def test_notification_created_on_message_send(self):
        sender = User.objects.create_user(username='sender')
        receiver = User.objects.create_user(username='receiver')

        msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello!')
        notification = Notification.objects.get(user=receiver, message=msg)

        self.assertTrue(notification)
