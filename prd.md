# PRD: AI-Powered Smart Newsletter System

## 1. Product Overview
A multi-user personalized newsletter platform where users define their interests using a custom prompt (up to 100 words). The system delivers tailored news summaries via email on a daily, weekly, or monthly basis, with a specific focus on high quality and zero redundancy.

## 2. Core Features

### 2.1 Authentication
- **Google Login**: Users authenticate using their Google accounts (OAuth 2.0) for a seamless sign-up/sign-in experience.

### 2.2 Newsletter Configuration
- **Multiple Subscriptions**: Users can create multiple distinct news subscriptions (each acting as an independent news aggregator target).
- **Prompt-Based Interests**: For each subscription, users define what they want to read about using a direct text prompt (up to 100 words) (e.g., "I want updates on AI safety, recent LLM wrapper startups, and space exploration").
- **Delivery Management**: Each subscription can have its own frequency (e.g., Daily, Weekly), delivery window, or be paused via a simple web dashboard.
- **Email History**: Users can browse a list of past emails they received within specific time windows, and read the full content of any past email directly in the web app.

### 2.3 Newsletter Delivery
- **Three Modes**:
    - **Daily**: 300-500 words summary of today's top stories.
    - **Weekly**: Synthesis of the week's most impactful events.
    - **Monthly**: High-level trend analysis and deep dives.
- **Format**: Email with clear summaries and "Read More" redirect links.
- **Tone**: Professional, concise, and informative.

### 2.3 Intelligent Deduplication
- **Constraint**: Solve the "Repeat News" problem common in generic LLM outputs.
- **Mechanism**: The system must track what has *already* been sent to the user and ensure no overlap in content across any timeframe.

## 3. User Experience (UX)
- **Minimalist Design**: A premium, clean, simple configuration dashboard.
- **Proactive Notifications**: Brief confirmation when changes to the prompt are saved.
- **One-Click Redirection**: Links in emails lead back to source articles.

## 4. Success Metrics
- **Retention Rate**: Users remaining subscribed over 3 months.
- **Redundancy Rate**: Percentage of news items flagged as "seen before" (Target: < 1%).
