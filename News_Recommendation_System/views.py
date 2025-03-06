from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .login_signup import signup_user
from .login_signup import login_user


@csrf_exempt  # Disable CSRF protection for testing (remove in production)
def signup_view(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            # Check if required fields are provided
            if not name or not email or not password:
                return JsonResponse({"message": "Missing required fields"}, status=400)

            # Call the signup function
            result = signup_user(email, password, name)
            return JsonResponse(result)  # Return the signup function response

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)

    return JsonResponse({"message": "Not a POST request"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Check if required fields are provided
            if not email or not password:
                return JsonResponse({"message": "Missing required fields"}, status=400)

            # Call the signup function
            result = login_user(email, password)
            return JsonResponse(result)  # Return the signup function response

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)

    return JsonResponse({"message": "Not a POST request"}, status=405)