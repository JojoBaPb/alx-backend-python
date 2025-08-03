from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch
from .models import Message
from django.contrib.auth.decorators import login_required

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
