import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import Request, HTTPException

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

def verify_google_token(token: str) -> dict:
    """Verify a Google ID token and return the decoded claims.
    
    Returns dict with keys: sub, email, name, picture, etc.
    Raises HTTPException if token is invalid.
    """
    try:
        claims = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
        if claims["iss"] not in ("accounts.google.com", "https://accounts.google.com"):
            raise ValueError("Invalid issuer")
        return claims
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

def get_current_user(request: Request) -> dict:
    """FastAPI dependency: extract and verify the Bearer token from Authorization header.
    
    Returns dict with user claims (sub, email, name).
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header[len("Bearer "):]
    return verify_google_token(token)
