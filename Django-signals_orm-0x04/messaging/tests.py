from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class SignalTest(TestCase):
    def test_notification_created_on_message_send(self):
        sender = User.objects.create_user(username='sender')
        receiver = User.objects.create_user(username='receiver')

        msg = Message.objects.create(sender=sender, receiver=receiver, content='Hello!')
        notification = Notification.objects.get(user=receiver, message=msg)

        self.assertTrue(notification)

class MessageEditTest(TestCase):
    def test_message_edit_history(self):
        sender = User.objects.create_user(username='sender')
        receiver = User.objects.create_user(username='receiver')

        # Create a message
        msg = Message.objects.create(sender=sender, receiver=receiver, content='Original content')

        # Edit the message content
        msg.content = 'Updated content'
        msg.save()

        # Check if MessageHistory has logged the old content
        history = MessageHistory.objects.filter(message=msg).first()
        self.assertEqual(history.old_content, 'Original content')
        self.assertTrue(msg.edited)  # Check if 'edited' flag is True
