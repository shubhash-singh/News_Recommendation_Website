from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Login and Sign up imports
from .firebase_connection import signup_user
from .firebase_connection import login_user
from .firebase_connection import get_user_topics as topics
from .firebase_connection import update_topics

# News fether class
from .News_provider import Fetch_top_news as top_news
from .News_provider import Summarise_with_image as summarize
from .News_provider import Recommend_news
from .News_provider import Get_news_on as topic_based_news
from .News_provider import get_topic

@csrf_exempt
def check_login_status_view(request):
    if request.method == "GET":
        login_status = request.COOKIES.get('login_status', 'false')  # Default to 'false' if cookie is missing
        return JsonResponse({"login_status": login_status})

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
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
            response = JsonResponse({"result":result, "name": name, "email":email})
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

@csrf_exempt
def recommended_news(request):
    if request.method == "GET":
        try:
            
            user_email = "subhashsingh2059@gmail.com"
            
            if user_email == 'false':
                user_topic = {"":""}
            else:
                user_topic = topics(user_email)
            # print("EMail :" + user_email)
            # print(f"user topic : {user_topic}")
            newses = Recommend_news(user_topic)
            for news in newses:
                # summary, image = summarize(news["url"])
                # news["summary"] = summary
                # news["image_url"] = image
                print(news)
            return JsonResponse({"news": news})
        
        
        except json.JSONDecodeError as e:
            return JsonResponse({"message":str(e)}, status = 405)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

  
@csrf_exempt
def like_from_user_view(request):
    if request.method == "POST":
        try:
            user_email = "subhashsingh2059@gmail.com"
            
            data = json.loads(request.body)
            url = data.get("url")
            url_topics = get_topic(url)
            user_topics = topics(user_email)
            
            for key in url_topics:
                if key in user_topics:
                    user_topics[key] += 1  # Increment value if key exists
                else:
                    user_topics[key] = 1    # Add new key with value 1 if not present


            return JsonResponse({update_topics(user_email, user_topics)})
            
        except json.JSONDecodeError as e:
            return JsonResponse({"error":str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
@csrf_exempt
def update_category_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            topics = data.get("topics")
            
            response = update_topics(email, topics)
            if response:
                
                return JsonResponse({"success":"true"})
            return JsonResponse({"success":"false"})
        except json.JSONDecodeError as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)