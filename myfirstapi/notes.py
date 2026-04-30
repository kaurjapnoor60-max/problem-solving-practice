from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import credentials, firestore, auth

from pydantic import BaseModel
from datetime import datetime


# =========================
# FASTAPI APP
# =========================

app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# SECURITY
# =========================

security = HTTPBearer()


# =========================
# FIREBASE INITIALIZATION
# =========================

cred = credentials.Certificate("new_firebase_key.json")

firebase_admin.initialize_app(cred)


# =========================
# FIRESTORE DATABASE
# =========================

db = firestore.client()


# =========================
# PYDANTIC MODEL
# =========================

class Note(BaseModel):

    title: str

    content: str


# =========================
# VERIFY FIREBASE TOKEN
# =========================


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    try:

        token = credentials.credentials

        decoded_token = auth.verify_id_token(token)

        return decoded_token

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )


# =========================
# CREATE NOTE
# =========================

@app.post("/notes")
def create_note(
    note: Note,
    user=Depends(verify_token)
):

    note_data = {

        "title": note.title,

        "content": note.content,

        "timestamp": datetime.utcnow(),

        "user_id": user["uid"]
    }

    doc_ref = db.collection("notes").document()

    doc_ref.set(note_data)

    return {
        "message": "Note Created Successfully",
        "note_id": doc_ref.id
    }


# =========================
# GET ALL NOTES
# =========================

@app.get("/notes")
def get_notes(
    user=Depends(verify_token)
):

    notes = []

    docs = db.collection("notes") \
        .where("user_id", "==", user["uid"]) \
        .stream()

    for doc in docs:

        note = doc.to_dict()

        note["id"] = doc.id

        notes.append(note)

    return notes


# =========================
# UPDATE NOTE
# =========================

@app.put("/notes/{note_id}")
def update_note(
    note_id: str,
    note: Note,
    user=Depends(verify_token)
):

    doc_ref = db.collection("notes").document(note_id)

    doc = doc_ref.get()

    if not doc.exists:

        raise HTTPException(
            status_code=404,
            detail="Note Not Found"
        )

    existing_note = doc.to_dict()

    if existing_note["user_id"] != user["uid"]:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    doc_ref.update({

        "title": note.title,

        "content": note.content,

        "timestamp": datetime.utcnow()
    })

    return {
        "message": "Note Updated Successfully"
    }


# =========================
# DELETE NOTE
# =========================

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: str,
    user=Depends(verify_token)
):

    doc_ref = db.collection("notes").document(note_id)

    doc = doc_ref.get()

    if not doc.exists:

        raise HTTPException(
            status_code=404,
            detail="Note Not Found"
        )

    existing_note = doc.to_dict()

    if existing_note["user_id"] != user["uid"]:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    doc_ref.delete()

    return {
        "message": "Note Deleted Successfully"
    }
