const firebaseConfig = {
  apiKey: "AIzaSyB24Qo574E_Ovg5MOSb7X0Q40pDhdURPhQ",
  authDomain: "notes-app-9e795.firebaseapp.com",
  projectId: "notes-app-9e795",
  storageBucket: "notes-app-9e795.firebasestorage.app",
  messagingSenderId: "157795500469",
  appId: "1:157795500469:web:a1178277e6ac3cc0db59fc",
  measurementId: "G-G7KZ4R8MTY"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);


// Firebase Auth
const auth = firebase.auth();


// Store token globally
let token = "";


// FastAPI Backend URL
const BASE_URL = "http://127.0.0.1:8000";



// =========================
// SIGNUP
// =========================
async function signup() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        await auth.createUserWithEmailAndPassword(
            email,
            password
        );

        alert("Signup Successful");

    } catch (error) {

        alert(error.message);
    }
}



// =========================
// LOGIN
// =========================
async function login() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const userCredential =
            await auth.signInWithEmailAndPassword(
                email,
                password
            );

        // Generate Firebase Token
        token =
            await userCredential.user.getIdToken();

        document.getElementById("status").innerText =
            "Login Successful";


    } catch (error) {

        alert(error.message);
    }
}



// =========================
// LOGOUT
// =========================
async function logout() {

    await auth.signOut();

    token = "";

    document.getElementById("status").innerText =
        "Logged Out";

    document.getElementById("notes-container").innerHTML =
        "";
}



// =========================
// CREATE NOTE
// =========================
async function createNote() {

    const title =
        document.getElementById("title").value;

    const content =
        document.getElementById("content").value;

    try {

        const response =
            await fetch(`${BASE_URL}/notes`, {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify({
                    title,
                    content
                })
            });

        const data =
            await response.json();

        console.log(data);

        alert("Note Added Successfully");

        // Clear inputs
        document.getElementById("title").value = "";

        document.getElementById("content").value = "";

        // Refresh notes
        fetchNotes();

    } catch (error) {

        console.log(error);

        alert("Error creating note");
    }
}


// =========================
// FETCH NOTES (UPDATED)
// =========================
async function fetchNotes() {
    console.log("Fetching Notes...");

    try {
        const response = await fetch(`${BASE_URL}/notes`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        // 1. Check if the backend returned an error status (e.g., 401, 500)
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Backend Error:", errorData);
            alert(`Backend Error: ${errorData.detail || "Could not fetch notes"}`);
            return; // Stop execution here
        }

        // 2. If response is OK, parse the notes
        const notes = await response.json();
        console.log("Notes received:", notes);
        
        displayNotes(notes);

    } catch (error) {
        // 3. This will now catch actual network errors (like CORS or server down)
        console.error("Network or Script Error:", error);
        alert("Network error. Open the browser console (F12) for more details.");
    }
}



// =========================
// DISPLAY NOTES
// =========================
function displayNotes(notes) {

    const container =
        document.getElementById("notes-container");

    container.innerHTML = "";

    // If no notes
    if (notes.length === 0) {

        container.innerHTML =
            "<p>No Notes Found</p>";

        return;
    }

    notes.forEach(note => {

        container.innerHTML += `

            <div class="note">

                <h3>${note.title}</h3>

                <p>${note.content}</p>

                <small>
                    Note ID: ${note.id}
                </small>

            </div>
        `;
    });
}



// =========================
// UPDATE NOTE
// =========================
async function updateNote() {

    const noteId =
        document.getElementById("note-id").value;

    const title =
        document.getElementById("title").value;

    const content =
        document.getElementById("content").value;

        console.log(title);
        console.log(content);
        console.log(noteId);

    try {

        const response =
            await fetch(
                `${BASE_URL}/notes/${noteId}`,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            `Bearer ${token}`
                    },

                    body: JSON.stringify({
                        title,
                        content
                    })
                }
            );

        const data =
            await response.json();

        console.log(data);

        alert("Note Updated Successfully");

        fetchNotes();

    } catch (error) {

        console.log(error);

        alert("Error updating note");
    }
}



// =========================
// DELETE NOTE
// =========================
async function deleteNoteFromInput() {

    const noteId =
        document.getElementById("note-id").value.trim();

    try {

        const response =
            await fetch(
                `${BASE_URL}/notes/${noteId}`,
                {

                    method: "DELETE",

                    headers: {

                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );

        const data =
            await response.json();

        console.log(data);

        alert("Note Deleted Successfully");

        fetchNotes();

    } catch (error) {

        console.log(error);

        alert("Error deleting note");
    }
}

