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
            'topics': {}
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
        return user_topic
            
    except Exception as e:
        return {"succss":False, "message":f"Error: {str(e)}"}
    
    
def update_topics(email, topics):
    try:
        users_ref = db.collection("user")
        
        # Get user document based on email
        query = users_ref.where("email", "==", email).stream()
        user_doc = None
        for doc in query:
            user_doc = doc
            break
        
        if user_doc is None:
            print("User not found.")
            return False  # Return False if user is not found

        # Get existing topics or initialize if none
        user_topics = user_doc.to_dict().get("topics", {})

        # Update topics
        for key, value in topics.items():
            user_topics[key] = user_topics.get(key, 0) + value

        # Save updated topics back to Firestore
        users_ref.document(user_doc.id).update({"topics": user_topics})
        
        # Verify if the update was successful
        updated_doc = users_ref.document(user_doc.id).get()
        updated_topics = updated_doc.to_dict().get("topics", {})
        
        # Check if the topics were updated correctly
        if updated_topics == user_topics:
            return True  # Return True if update was successful
        else:
            return False  # Return False if update failed
            
    except Exception as e:
        print(f"Error: {e}")
        return False  # Return False if an exception occurs


        