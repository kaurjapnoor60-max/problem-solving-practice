from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any

# --- 1. SECURITY CONFIGURATION ---
# This opens your VIP Pass and starts the Google connection
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# --- 2. DATABASE CONNECTION ---
# This creates the active 'pipe' to your Firestore database
db = firestore.client()

# --- 3. API INITIALIZATION ---
# This starts your FastAPI server
app = FastAPI()

# --- 4. FLEXIBLE POST ACTION (Writing Data) ---
# This window accepts ANY JSON data and pushes it to Firebase
@app.post("/add-data")
def add_flexible_data(data: Dict[str, Any]):
    """
    Accepts any key-value pairs (e.g., {"name": "A"} or {"name": "A", "roll": 1})
    and saves them into the 'Users' collection.
    """
    # This takes the whole 'data' container and adds it to the collection
    db.collection("Users").add(data)
    
    return {
        "status": "Success", 
        "message": "Data saved to Firebase",
        "saved_fields": list(data.keys())
    }

# --- 5. GET ACTION (Reading Data) ---
# This retrieves all the flexible data you have saved
@app.get("/get-data")
def read_all_data():
    all_records = []
    
    # We grab every document in the 'Users' collection
    docs = db.collection("Users").stream()
    
    for doc in docs:
        # We translate each document back into a Python dictionary
        record = doc.to_dict()
        # We add the unique ID from Firebase so we know which record is which
        record["id"] = doc.id
        all_records.append(record)
        
    return {"count": len(all_records), "results": all_records}