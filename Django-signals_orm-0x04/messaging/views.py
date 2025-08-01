from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return JsonResponse({"message": "User deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
