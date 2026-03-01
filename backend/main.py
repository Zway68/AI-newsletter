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
def get_frontend_path():
    try:
        from python.runfiles import runfiles
        r = runfiles.Create()
        # The path in Bazel is <workspace_name>/<path_from_root>
        # Workspace name is 'ai_newsletter' from MODULE.bazel
        path = r.Rlocation("ai_newsletter/frontend")
        if path and os.path.exists(path):
            return path
    except ImportError:
        pass
    
    # Fallback to local source tree relative path
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

frontend_path = get_frontend_path()

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/index.css")
def serve_css():
    return FileResponse(os.path.join(frontend_path, "index.css"))

@app.get("/app.js")
def serve_js():
    return FileResponse(os.path.join(frontend_path, "app.js"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

