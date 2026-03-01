# Client-Server Architecture & Data Flow

This document outlines the interaction between the user's browser, the central AI Newsletter API server, and the local file system storage.

## Execution Environment
- **Hosting**: A single Google Cloud Platform (GCP) Virtual Machine (e.g., e2-micro/small).
- **Web App Delivery**: The FastAPI server acts as both the static file host (serving the compiled Vue/React JS bundles and HTML) and the JSON API backend.
- **Storage**: The API Server runs on the same VM as the local file system storage (`data/` directory). No external databases are used for preferences or history.

## Sequence Diagram

Below is the execution flow demonstrating how the application loads and how read/write operations occur.

```mermaid
sequenceDiagram
    autonumber
    
    actor User as Google Chrome
    participant Server as FastAPI Server -GCP VM-
    participant FS as Local File System -GCP VM-
    
    %% 1. Initial Page Load
    Note over User, Server: 1. Application Initialization
    User->>Server: GET / [Request Web App]
    Server-->>User: Returns index.html, core.js, style.css
    
    User->>User: Parse JS & Render UI
    
    %% 2. Reading Data
    Note over User, FS: 2. Reading User Preferences & History
    User->>Server: GET /api/v1/config?user=$user_id
    Server->>FS: Read "data/users/$user_id/config.json"
    FS-->>Server: JSON Content
    Server-->>User: 200 OK [Returns Config JSON]
    
    User->>Server: GET /api/v1/history?user=$user_id
    Server->>FS: Read "data/users/$user_id/history.json"
    FS-->>Server: JSON Content
    Server-->>User: 200 OK [Returns History JSON]
    
    %% 3. Writing Data
    Note over User, FS: 3. Updating User Settings (Write)
    User->>Server: POST /api/v1/config [Payload: updated prompt/frequency]
    Server->>Server: Validate Payload schema (e.g. prompt limit)
    Server->>FS: Write "data/users/$user_id/config.json"
    FS-->>Server: Write Success
    Server-->>User: 200 OK [Settings Saved]
```
