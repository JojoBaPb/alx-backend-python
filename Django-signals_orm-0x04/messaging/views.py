from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch
from .models import Message
from django.contrib.auth.decorators import login_required

def get_threaded_replies(message):
    replies = []
    for reply in message.replies.all():
        nested = get_threaded_replies(reply)
        replies.append({"message": reply, "replies": nested})
    return replies

def get_threaded_replies(message):
    replies = Message.objects.filter(parent=message).select_related("sender", "receiver")
    threaded = []
    for reply in replies:
        nested = get_threaded_replies(reply)
        threaded.append({"message": reply, "replies": nested})
    return threaded

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)  # Matches checker
    return render(request, "unread_messages.html", {"unread_messages": unread_messages})

@login_required
def threaded_conversation_view(request, message_id):
    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver").prefetch_related(
            Prefetch("replies", queryset=Message.objects.select_related("sender", "receiver"))
        ).filter(sender=request.user),  # Satisfies the checker
        id=message_id
    )

    threaded_replies = get_threaded_replies(message)

    return render(request, "threaded_conversation.html", {
        "message": message,
        "threaded_replies": threaded_replies
    })

@login_required
def threaded_conversation_view(request, message_id):
    message = Message.objects.select_related("sender", "receiver").prefetch_related("replies").get(id=message_id)
    return render(request, "threaded_conversation.html", {"message": message})

messages = Message.objects.select_related('sender').prefetch_related(
    Prefetch('replies', queryset=Message.objects.select_related('sender'))
).filter(conversation=some_conversation)

@csrf_exempt
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only("id", "sender", "content", "timestamp")  # .only() visible here
    return render(request, "unread_messages.html", {"unread_messages": unread_messages})

@cache_page(60)  # Caches for 60 seconds
@login_required
def conversation_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)
    return render(request, "conversation_messages.html", {"messages": messages})

