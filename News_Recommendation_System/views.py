from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Login and Sign up imports
from .firebase_connection import signup_user
from .firebase_connection import login_user
from .firebase_connection import get_user_topics as topics

# News fether class
from .News_provider import Fetch_top_news as top_news
from .News_provider import Summarise_with_image as summarize
from .News_provider import Recommend_news
from .News_provider import Get_news_on as topic_based_news


@csrf_exempt
def check_login_status_view(request):
    if request.method == "GET":
        login_status = request.COOKIES.get('login_status', 'false')  # Default to 'false' if cookie is missing
        return JsonResponse({"login_status": login_status})

    return JsonResponse({"error": "Invalid request method"}, status=405)

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
            response = JsonResponse(result)
            response.set_cookie('email', email, max_age=2592000, httponly=True, secure=True)
            response.set_cookie('login_status', 'true', max_age=2592000, httponly=True, secure=True)

            return response  

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
            response = JsonResponse(result)
            response.set_cookie('email', email, max_age=2592000, httponly=True, secure=True)
            response.set_cookie('login_status', 'true', max_age=2592000, httponly=True, secure=True)

            return response  

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)

    return JsonResponse({"message": "Not a POST request"}, status=405)

@csrf_exempt
def top_news_view(request):
    if request.method == "GET":
        try:
            news = top_news()  # Fetch top news (returns a list of dicts)
            return JsonResponse({"news": news}, safe=False)  # Ensure JSON serialization
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # Handle exceptions

    return JsonResponse({"error": "Invalid request method"}, status=405)
            
        #     if (len(news) >= 0):
        #         return JsonResponse({"news":news})
            
        #     else:
        #         return JsonResponse({"message":"Unable to fetch news"}, status = 400)
            
        # except json.JSONDecodeError:
        #     return JsonResponse({"message":"Not a GET request"}, status = 405)

@csrf_exempt
def recommended_news(request):
    if request.method == "GET":
        try:
            
            user_email = request.COOKIES.get('email',"false")  # Default to 'false' if cookie is missing
            
            if user_email == 'false':
                user_topic = []
            else:
                user_topic = topics(user_email)
            news = Recommend_news(user_topic)
            
            if (len(news) > 0):
                return JsonResponse({"news":news})
            
            else:
                return JsonResponse({"message":"Unable to fetch news"}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"message":"Not a GET request"}, status = 405)