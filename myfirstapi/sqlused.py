from fastapi import FastAPI, HTTPException
import pyodbc
from pydantic import BaseModel

app = FastAPI()

# 1. MS SQL SERVER CONNECTION SETTINGS 
DB_CONNECTION_STRING = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=JAPNOOR\SQLEXPRESS;'
    r'DATABASE=notes_app_db;'
    r'Trusted_Connection=yes;'
)

def get_db_connection():
    try:
        return pyodbc.connect(DB_CONNECTION_STRING)
    except pyodbc.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {err}")

# 2. PYDANTIC MODELS 
class NoteCreate(BaseModel):
    title: str
    content: str

# 3. STARTUP SCRIPT (Creates the table if it is missing)
@app.on_event("startup")
def startup():
    conn = get_db_connection()
    cursor = conn.cursor()
    # This automatically builds the 'notes' table so you don't get the "Invalid Object" error
    create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='notes' and xtype='U')
        CREATE TABLE notes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL
        )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# 4. THE API ROUTES ---

# CREATE
@app.post("/notes/")
def create_note(note: NoteCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO notes (title, content) OUTPUT Inserted.id VALUES (?, ?)"
    cursor.execute(query, (note.title, note.content))
    new_id = cursor.fetchone()[0]
    conn.commit() 
    cursor.close()
    conn.close()
    return {"message": "Note saved!", "id": new_id, "title": note.title, "content": note.content}

# READ ALL
@app.get("/notes/")
def get_all_notes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    columns = [column[0] for column in cursor.description]
    notes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return notes

@app.get("/notes/{note_id}")
def get_single_note(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
        
    columns = [column[0] for column in cursor.description]
    note = dict(zip(columns, row))
    cursor.close()
    conn.close()
    return note

# UPDATE a note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE notes SET title = ?, content = ? WHERE id = ?"
    cursor.execute(query, (updated_note.title, updated_note.content, note_id))
    conn.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
        
    cursor.close()
    conn.close()
    return {"message": f"Note {note_id} updated successfully"}

# DELETE a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")
        
    cursor.close()
    conn.close()
    return {"message": f"Note {note_id} deleted successfully"}