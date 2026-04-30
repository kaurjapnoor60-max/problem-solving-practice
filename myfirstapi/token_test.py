import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyB24Qo574E_Ovg5MOSb7X0Q40pDhdURPhQ",
    "authDomain": "notes-app-9e795.firebaseapp.com",
    "projectId": "notes-app-9e795",
    "storageBucket": "notes-app-9e795.firebasestorage.app",
    "messagingSenderId": "157795500469",
    "appId": "1:157795500469:web:a1178277e6ac3cc0db59fc",
    "measurementId": "G-G7KZ4R8MTY",
    "databaseURL": "https://notes-app-9e795-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

user = auth.sign_in_with_email_and_password(
    "test@gmail.com",
    "123456"
)

print(user["idToken"])