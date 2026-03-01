import json
import os
from typing import Dict, Any, List, Optional

DATA_DIR = os.getenv("DATA_DIR", "data/users")

def _get_user_dir(user_id: str) -> str:
    path = os.path.join(DATA_DIR, user_id)
    os.makedirs(path, exist_ok=True)
    return path

def get_config(user_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(_get_user_dir(user_id), "config.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_config(user_id: str, config: Dict[str, Any]) -> None:
    path = os.path.join(_get_user_dir(user_id), "config.json")
    with open(path, "w") as f:
        json.dump(config, f, indent=2)

def get_history_emails(user_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    path = os.path.join(_get_user_dir(user_id), "history_email.json")
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = json.load(f)
    
    results = []
    for item in data:
        if start_date <= item["sent_at"] <= end_date:
            results.append({
                "id": item["id"],
                "sub_id": item.get("sub_id", ""),
                "subject": item["subject"],
                "sent_at": item["sent_at"]
            })
    return results

def get_history_email_by_id(user_id: str, email_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(_get_user_dir(user_id), "history_email.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
        
    for item in data:
        if item["id"] == email_id:
            return item
    return None

def append_history_email(user_id: str, email_data: Dict[str, Any]) -> None:
    path = os.path.join(_get_user_dir(user_id), "history_email.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
    else:
        data = []
        
    data.append(email_data)
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
