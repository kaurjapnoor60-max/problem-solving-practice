from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. SHOW THE VIP PASS TO FIREBASE ---
# Why: We are telling Python to grab the secret key file so Firebase lets us in.
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# --- 2. CONNECT TO THE DATABASE ---
# Why: This creates the secure pipe to your specific Firestore database.
db = firestore.client()

# --- 3. HIRE THE WAITER ---
# Why: This officially creates your FastAPI app.
app = FastAPI()

# --- 4. CREATE THE POST ACTION ---
# Why: We are making a rule. If someone visits "/add-user" and gives us data, we run this code.
@app.post("/add-user")
def create_user(name: str, age: int):
    
    # Pack the data into a neat little box (a dictionary) that Firebase can understand
    data_to_save = {
        "Name": name,
        "Age": age
    }
    
    # Send the box through the pipe to a collection (drawer) called "Users"
    # .add() tells Firebase to save it and automatically give it a random ID
    db.collection("Users").add(data_to_save)
    
    # Tell the customer the job is done!
    return {"message": "Success! The data went to Firebase!"}

# --- 5. CREATE THE GET ACTION (Read Data) ---
# Why: We are making a rule. If someone visits "/get-users", the waiter fetches all user folders.

@app.get("/get-users")
def read_users():
    
    # 1. Create an empty list (like an empty tray) to hold the data we find
    all_users = []
    
    # 2. Tell the waiter to go to the "Users" drawer and grab EVERY folder inside it
    # We use .stream() to tell Firebase to send us the folders one after another
    users_ref = db.collection("Users").stream()
    
    # 3. Open each folder one by one to read the data inside
    for doc in users_ref:
        # doc.to_dict() translates the Firebase data back into a normal Python dictionary
        user_data = doc.to_dict() 
        
        # Put this user's data onto our tray
        all_users.append(user_data)
        
    # 4. Hand the tray full of data back to the app/customer!
    return {"Total Users Found": len(all_users), "Data": all_users}