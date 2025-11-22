import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from database import create_document, get_documents, db
from schemas import Context, Note

app = FastAPI(title="Learning Notes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Learning Notes API is running"}


# Internationalization - expose supported languages
SUPPORTED_LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "de", "name": "Deutsch"},
    {"code": "es", "name": "Español"},
    {"code": "fr", "name": "Français"},
]


@app.get("/api/languages")
def get_languages():
    return {"languages": SUPPORTED_LANGUAGES}


# Context endpoints
@app.post("/api/contexts")
def create_context(context: Context):
    context_id = create_document("context", context)
    return {"id": context_id}


@app.get("/api/contexts")
def list_contexts(language: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if language:
        filt["language"] = language
    contexts = get_documents("context", filt)
    for c in contexts:
        c["_id"] = str(c["_id"])  # ensure JSON serializable
    return {"items": contexts}


# Notes endpoints
@app.post("/api/notes")
def create_note(note: Note):
    note_id = create_document("note", note)
    return {"id": note_id}


@app.get("/api/notes")
def list_notes(context_id: Optional[str] = None, language: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if context_id:
        filt["context_id"] = context_id
    if language:
        filt["language"] = language
    notes = get_documents("note", filt)
    for n in notes:
        n["_id"] = str(n["_id"])  # ensure JSON serializable
    return {"items": notes}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
