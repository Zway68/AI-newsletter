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
    "interests": ["AI Safety", "Space Exploration"],
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
    "interests": ["AI Safety"],
    "frequency": "WEEKLY"
  }
  ```
- **Response**: `200 OK` - Returns the updated configuration.

---

## 3. Conversational Interface (Command Center)
*The core interface for managing settings via natural language.*

### `POST /api/v1/chat`
- **Description**: Processes a user's natural language command, uses the LLM to parse the intent, and applies changes to the `config.json` if necessary.
- **Headers**: `Authorization: Bearer <Token>`
- **Payload**:
  ```json
  {
    "message": "Stop sending me space news and change my frequency to monthly."
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "reply": "I've removed space news from your interests and set your delivery to monthly.",
    "action_taken": "CONFIG_UPDATED",
    "current_config": {
      "interests": ["AI Safety"],
      "frequency": "MONTHLY"
    }
  }
  ```

### `POST /api/v1/chat/undo`
- **Description**: Reverts the last configuration change made via the chat interface by pulling from the `version_history` in `config.json`.
- **Headers**: `Authorization: Bearer <Token>`
- **Response**: `200 OK`
  ```json
  {
    "reply": "Your previous settings have been restored.",
    "restored_config": { ... }
  }
  ```

---

## 4. History and Lessons

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

### `POST /api/v1/lessons`
- **Description**: Allows a user to report a redundancy or error, writing a correction to the global `lesson_library.json`.
- **Headers**: `Authorization: Bearer <Token>`
- **Payload**:
  ```json
  {
    "error_type": "REDUNDANCY",
    "description": "You sent me this exact article yesterday."
  }
  ```
- **Response**: `201 Created`
