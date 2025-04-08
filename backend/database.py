import sqlite3
from cryptography.fernet import Fernet

# Encryption key (should be securely stored in a config or environment variable)
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)

def init_db():
    """
    Initializes the SQLite database and creates the notes table with indexing.
    """
    conn = sqlite3.connect("../storage/notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            transcription BLOB NOT NULL,
            summary BLOB NOT NULL,
            quiz BLOB NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON notes (title)")
    conn.commit()
    conn.close()

def encrypt_data(data):
    """
    Encrypts the given data using Fernet encryption.

    Args:
        data (str): The data to encrypt.

    Returns:
        bytes: The encrypted data.
    """
    return cipher.encrypt(data.encode())

def decrypt_data(data):
    """
    Decrypts the given data using Fernet encryption.

    Args:
        data (bytes): The encrypted data.

    Returns:
        str: The decrypted data.
    """
    return cipher.decrypt(data).decode()

def save_note(title, transcription, summary, quiz):
    """
    Saves a new note to the database.

    Args:
        title (str): The title of the note.
        transcription (str): The transcribed text.
        summary (str): The summarized text.
        quiz (str): The quiz questions.
    """
    conn = sqlite3.connect("../storage/notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notes (title, transcription, summary, quiz)
        VALUES (?, ?, ?, ?)
    """, (title, encrypt_data(transcription), encrypt_data(summary), encrypt_data(quiz)))
    conn.commit()
    conn.close()

def get_notes():
    """
    Retrieves all notes from the database.

    Returns:
        list: A list of notes with decrypted data.
    """
    conn = sqlite3.connect("../storage/notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, transcription, summary, quiz FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return [
        {
            "id": note[0],
            "title": note[1],
            "transcription": decrypt_data(note[2]),
            "summary": decrypt_data(note[3]),
            "quiz": decrypt_data(note[4])
        }
        for note in notes
    ]

def update_note(note_id, title=None, transcription=None, summary=None, quiz=None):
    """
    Updates an existing note in the database.

    Args:
        note_id (int): The ID of the note to update.
        title (str, optional): The new title.
        transcription (str, optional): The new transcription.
        summary (str, optional): The new summary.
        quiz (str, optional): The new quiz questions.
    """
    conn = sqlite3.connect("../storage/notes.db")
    cursor = conn.cursor()
    if title:
        cursor.execute("UPDATE notes SET title = ? WHERE id = ?", (title, note_id))
    if transcription:
        cursor.execute("UPDATE notes SET transcription = ? WHERE id = ?", (encrypt_data(transcription), note_id))
    if summary:
        cursor.execute("UPDATE notes SET summary = ? WHERE id = ?", (encrypt_data(summary), note_id))
    if quiz:
        cursor.execute("UPDATE notes SET quiz = ? WHERE id = ?", (encrypt_data(quiz), note_id))
    conn.commit()
    conn.close()

def delete_note(note_id):
    """
    Deletes a note from the database.

    Args:
        note_id (int): The ID of the note to delete.
    """
    conn = sqlite3.connect("../storage/notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
