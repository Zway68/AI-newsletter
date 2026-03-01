# Technical Design: AI-Powered Smart Newsletter System (Simplified)

## 1. System Architecture (Local-First)

The system is designed for simplicity, using local file system storage and native macOS task scheduling.

```mermaid
graph TD
    User((User)) <--> UI[Web/App Chat Interface]
    UI <--> Backend[FastAPI/Node.js Logic]
    Backend <--> Prefs[(data/users/{user_id}/config.json)]
    Backend <--> LLM[LLM Engine: GPT/Gemini]
    
    subgraph Core Engine
        Aggregator[News Aggregator/API] --> Validator[Deduplication & Validation Engine]
        Validator <--> LessonLibrary[(data/lessons/library.json)]
        Validator <--> History[(data/users/{user_id}/history.json)]
    end
    
    Backend <--> CoreEngine
    CoreEngine --> EmailService[Email Delivery: SendGrid/Postmark]
    EmailService --> User
    
    Cron[Local macOS Cron Job] --> CoreEngine
```

## 2. Component Details

### 2.1 Deduplication Engine (The "Memory" Layer)
To solve the repetition problem, we implement a multi-stage filter:
1.  **Vector Store Semantic Search**: Every potential news snippet is converted into a vector embedding. Before including it in a newsletter, we perform a similarity search against the `sent_history.json`. If the cosine similarity exceeds a threshold (e.g., 0.85), it's rejected.
2.  **Canonical URL Tracking**: Store unique identifiers (URLs/IDs) of all summarized articles in `sent_history.json`.
3.  **LLM Cross-Check**: The LLM is provided with a list of "Topics covered in the last [X] days" in its context window to ensure thematic variety.

### 2.2 Lesson Library & Self-Correction
- **Schema**: `{ error_id, timestamp, error_type, original_prompt, output, correction, preventive_rule }`.
- **Workflow**:
    1.  **Detection**: Triggered by user feedback or automated validation failures.
    2.  **Inclusion**: Every new generation prompt includes a "Relevant Lessons" section, populated by finding similar past errors in `lesson_library.json`.

### 2.3 Conversational Interface
- **State Management**: Uses a state machine to handle "Draft" vs "Active" configurations.
- **Rollback Mechanism**: Implements an "Event Sourcing" pattern for user settings. Each change is a discrete event. "Undo" simply means reverting to the previous state index in the `version_history`.

### 2.4 Delivery Pipeline (Simplified)
- **Scheduling**: Uses local `crontab` on macOS.
    - **Global Dispatcher**: A recurring task that iterates through all `data/users/` directories and triggers generation based on individual `config.json` frequency settings.
- **Synthesizer**:
    - **Daily**: Summarizes raw news.
    - **Weekly/Monthly**: Uses "Recursive Summarization" (summarizing the daily summaries) to maintain context without exceeding token limits.

## 3. Data Model (Local Filesystem Structure)

```text
data/
├── users/
│   ├── {user_id_A}/
│   │   ├── config.json       (Interests, Frequency, Version History)
│   │   └── history.json      (Sent Content History, Embeddings)
│   └── {user_id_B}/
│       ├── config.json
│       └── history.json
└── lessons/
    └── library.json          (Global Shared Lessons)
```

### config.json
- `user_id`: UUID
- `email`: String
- `interests`: List[String]
- `frequency`: Enum (DAILY, WEEKLY, MONTHLY)
- `version_history`: List[SettingsState] (for rollback support)

### history.json
- `content_id`: UUID
- `payload_hash`: String (for fast exact match)
- `embedding`: Vector
- `sent_at`: Timestamp

## 4. Error Handling & Rollback
- **Transaction Logs**: Every newsletter sent is logged locally. If a "Daily" fails, the system logs the error to `errors.log`.
- **Version Control for Prompts**: System prompts are versioned so that a "rollback" can also affect the AI's behavior if a new prompt version causes regressions.
