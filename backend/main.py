import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from backend.storage import get_config, save_config, get_history_emails, get_history_email_by_id
from backend.auth import verify_google_token, get_current_user, GOOGLE_CLIENT_ID

app = FastAPI(title="AI Newsletter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Subscription(BaseModel):
    id: str
    name: str
    prompt: str
    frequency: str

class ConfigUpdateRequest(BaseModel):
    subscriptions: List[Subscription]

class GoogleAuthRequest(BaseModel):
    token: str

# --- Auth endpoints ---

@app.post("/api/v1/auth/google")
def google_login(request: GoogleAuthRequest):
    """Exchange a Google ID token for user info."""
    claims = verify_google_token(request.token)
    return {
        "user_id": claims["sub"],
        "email": claims.get("email", ""),
        "name": claims.get("name", ""),
        "picture": claims.get("picture", ""),
    }

@app.get("/api/v1/auth/client-id")
def get_client_id():
    """Return the Google Client ID for the frontend to use."""
    return {"client_id": GOOGLE_CLIENT_ID}

# --- Protected API endpoints ---

@app.get("/api/v1/config")
def read_config(user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    config = get_config(user_id)
    if not config:
        return {"email": user.get("email", ""), "subscriptions": []}
    return config

@app.put("/api/v1/config")
def update_config(request: ConfigUpdateRequest, user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    config = get_config(user_id) or {"email": user.get("email", "")}
    config["subscriptions"] = [sub.model_dump() for sub in request.subscriptions]
    save_config(user_id, config)
    return config

@app.get("/api/v1/history_email")
def list_history_email(
    start_date: str = Query(...), 
    end_date: str = Query(...),
    user: dict = Depends(get_current_user),
):
    user_id = user["sub"]
    emails = get_history_emails(user_id, start_date, end_date)
    return {"emails": emails}

@app.get("/api/v1/history_email/{email_id}")
def read_history_email(email_id: str, user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    email = get_history_email_by_id(user_id, email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

# --- Frontend serving ---

def get_frontend_path():
    try:
        from python.runfiles import runfiles
        r = runfiles.Create()
        path = r.Rlocation("ai_newsletter/frontend/dist")
        if path and os.path.exists(path):
            return path
    except ImportError:
        pass
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for candidate in ["dist-test", "frontend/dist"]:
        path = os.path.join(base_dir, candidate)
        if os.path.exists(path):
            return path
    
    return os.path.join(base_dir, "frontend")

frontend_path = get_frontend_path()

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

app.mount("/", StaticFiles(directory=frontend_path), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
