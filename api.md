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
    "email": "user@example.com",
    "subscriptions": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Daily Tech Digest",
        "prompt": "AI Safety, recent LLM wrapper startups",
        "frequency": "DAILY"
      },
      {
        "id": "987fcdeb-51a2-43d7-9012-3456789abcde",
        "name": "Space & Science Weekly",
        "prompt": "Updates on SpaceX and NASA missions",
        "frequency": "WEEKLY"
      }
    ]
  }
  ```

### `PUT /api/v1/config`
- **Description**: Updates the user's newsletter configurations (overwrites existing subscription list).
- **Headers**: `Authorization: Bearer <Token>`
- **Payload**:
  ```json
  {
    "subscriptions": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Daily Tech Digest",
        "prompt": "Only focus on AI Safety from now on.",
        "frequency": "WEEKLY"
      }
    ]
  }
  ```
- **Response**: `200 OK` - Returns the updated configuration.

---

## 3. Email History

### `GET /api/v1/history_email`
- **Description**: Retrieves a list of recently sent newsletter emails. Requires query parameters for user_id and time windows to filter the list.
- **Query Parameters**:
  - `user_id` (required): UUID of the user
  - `start_date` (required): ISO 8601 timestamp (e.g., `2023-10-01T00:00:00Z`)
  - `end_date` (required): ISO 8601 timestamp (e.g., `2023-10-31T23:59:59Z`)
- **Headers**: `Authorization: Bearer <Token>`
- **Response**: `200 OK`
  ```json
  {
    "emails": [
      {
        "id": "uuid",
        "sub_id": "123e4567-e89b-12d3-a456-426614174000",
        "subject": "Your Daily AI News",
        "sent_at": "2023-10-27T10:00:00Z"
      }
    ]
  }
  ```

### `GET /api/v1/history_email/{id}`
- **Description**: Read operation. Retrieves the full content of a specific sent email.
- **Path Parameters**:
  - `id`: The UUID of the email.
- **Query Parameters**:
  - `user_id` (required): UUID of the user
- **Headers**: `Authorization: Bearer <Token>`
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid",
    "sub_id": "123e4567-e89b-12d3-a456-426614174000",
    "subject": "Your Daily AI News",
    "sent_at": "2023-10-27T10:00:00Z",
    "html_content": "<html><body><h2>AI Safety Update</h2><p>...</p></body></html>",
    "text_content": "AI Safety Update..."
  }
  ```
