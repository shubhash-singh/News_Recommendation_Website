import firebase_admin
from firebase_admin import credentials, firestore



# Path to your Firebase key file
FIREBASE_CREDENTIALS = "News_Recommendation_System/firebase_service_key.json"

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()


def signup_user(email: str, password: str, name: str):
    try:
        doc_ref = db.collection('user').document()  # Create a new document
        doc_ref.set({
            'name': name,
            'email': email,
            'password': password,
            'topics': []
        })
        
        return {"success": True, "message": "User signed up successfully"}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

    


def login_user(email: str, password: str) -> dict:
    try:
        # Get the collection 'user'
        users_ref = db.collection("user")
        
        # Query the database to find the user by email
        query = users_ref.where("email", "==", email).stream()

        user_data = None
        for doc in query:
            user_data = doc.to_dict()  # Convert Firestore document to dictionary
            break  # We only need the first match
        
        # If no user is found
        if not user_data:
            return {"success": False, "message": "User not found"}
        
        # Check if the provided password matches the stored one
        if user_data.get("password") == password:
            return {"success": True, "message": "Login successful", "user": user_data}
        else:
            return {"success": False, "message": "Incorrect password"}

    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def get_user_topics(email:str):
    try:
        users_ref = db.collection("user")
        
        query = users_ref.where("email", "==", email).stream()
        
        user_data = None
        for doc in query:
            user_data = doc.to_dict()  # Convert Firestore document to dictionary
            break  # We only need the first match
        
        # If no user is found
        if not user_data:
            return {"success": False, "message": "User not found"}
        else:
            user_topic = user_data.get('topics')
        return {"topic" : user_topic}
            
    except Exception as e:
        return {"succss":False, "message":f"Error: {str(e)}"}