# AI Newsletter API Specification

This document outlines the REST API endpoints to be exposed by the FastAPI backend server. The backend interacts directly with the local file system (`data/users/$user_id/*`) as its datastore.

## 1. Authentication
*All protected routes require a valid session/token obtained from authentication.*

### `POST /api/v1/auth/google`
- **Description**: Verifies a Google OAuth token and signs the user in.
- **Payload**:
  ```json
  {
    "credential": "<Google JWT ID token>"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "user_id": "uuid-string",
    "email": "user@example.com",
    "token": "<Session or Access Token>"
  }
  ```

---

## 2. User Configuration
*Reads and writes to `data/users/{user_id}/config.json`*

### `GET /api/v1/config`
- **Description**: Retrieves the current newsletter configuration for the authenticated user.
- **Headers**: `Authorization: Bearer <Token>`
- **Response**: `200 OK`
  ```json
  {
    "prompt": "AI Safety, recent LLM wrapper startups, space exploration",
    "frequency": "DAILY",
    "email": "user@example.com"
  }
  ```

### `PUT /api/v1/config`
- **Description**: Directly updates the user's newsletter configuration.
- **Headers**: `Authorization: Bearer <Token>`
- **Payload**:
  ```json
  {
    "prompt": "Only focus on AI Safety from now on.",
    "frequency": "WEEKLY"
  }
  ```
- **Response**: `200 OK` - Returns the updated configuration.

---

## 3. History

### `GET /api/v1/history`
- **Description**: Retrieves the list of recently sent newsletter items for the user (reads from `history.json`).
- **Headers**: `Authorization: Bearer <Token>`
- **Response**: `200 OK`
  ```json
  {
    "history": [
      {
        "content_id": "uuid",
        "sent_at": "2023-10-27T10:00:00Z",
        "topic": "AI Release"
      }
    ]
  }
  ```
