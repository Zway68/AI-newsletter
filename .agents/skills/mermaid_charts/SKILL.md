---
name: Mermaid Chart Guidelines
description: Rules for generating Mermaid charts in Markdown without using () or {}
---

# Mermaid Charts Guidelines

When creating or editing Mermaid charts in Markdown (`.md`) files, you MUST adhere to the following syntax rules to prevent rendering and parsing errors:

## 1. Do Not Use Parentheses `()`
Parentheses can cause syntax issues in certain node definitions or labels. 
- **Incorrect:** `User((User))`
- **Incorrect:** `Label["Something (Additional)"]`
- **Correct:** `User["User"]` or `User["User -Additional-"]`

## 2. Do Not Use Curly Braces `{}`
Curly braces (often used for variables or JSON-like syntax) can also break parsers.
- **Incorrect:** `Prefs[("data/users/{user_id}/config.json")]`
- **Correct:** `Prefs["data/users/$user_id/config.json"]` or `Prefs["data/users/-user_id-/config.json"]`

## 3. Allowed Alternatives
Instead of parentheses or curly braces, use the following characters for variables or grouping:
- Dollar sign: `$` (e.g., `$user_id` instead of `{user_id}`)
- Hyphen/Dash: `-` (e.g., `data - details` instead of `data (details)`)

Follow these rules for all future diagrams to ensure seamless generation and display.
