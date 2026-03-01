import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from backend.storage import get_config, save_config, get_history_emails, get_history_email_by_id

app = FastAPI(title="AI Newsletter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Auth Dependency
def get_current_user_id() -> str:
    return "mock-user-id"

class Subscription(BaseModel):
    id: str
    name: str
    prompt: str
    frequency: str

class ConfigUpdateRequest(BaseModel):
    subscriptions: List[Subscription]

@app.get("/api/v1/config")
def read_config(user_id: str = Depends(get_current_user_id)):
    config = get_config(user_id)
    if not config:
        return {"email": "unknown", "subscriptions": []}
    return config

@app.put("/api/v1/config")
def update_config(request: ConfigUpdateRequest, user_id: str = Depends(get_current_user_id)):
    config = get_config(user_id) or {"email": "unknown"}
    config["subscriptions"] = [sub.model_dump() for sub in request.subscriptions]
    save_config(user_id, config)
    return config

@app.get("/api/v1/history_email")
def list_history_email(
    user_id: str = Query(...), 
    start_date: str = Query(...), 
    end_date: str = Query(...)
):
    current_usr = get_current_user_id()
    if current_usr != "mock-user-id" and current_usr != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    emails = get_history_emails(user_id, start_date, end_date)
    return {"emails": emails}

@app.get("/api/v1/history_email/{email_id}")
def read_history_email(email_id: str, user_id: str = Query(...)):
    email = get_history_email_by_id(user_id, email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

# Mount frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

@app.get("/")
def serve_frontend_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

