# External Dependencies & API Requirements

To deploy and run the AI-Newsletter system on the GCP VM, you will need to provision several external services and obtain their respective API keys/credentials.

## 1. Authentication (Google Login)
- **Service**: Google Cloud Console (APIs & Services)
- **Requirement**: OAuth 2.0 Client IDs.
- **Setup**:
    - Configure OAuth consent screen.
    - Create Credentials -> OAuth client ID (Web application).
    - Add authorized JavaScript origins and redirect URIs (for your GCP VM's IP or domain).
- **Required Keys**: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`.

## 2. LLM Engine (Summarization & Validation)
- **Service**: OpenAI (GPT-4o/mini) OR Google AI Studio (Gemini 1.5 Pro/Flash).
- **Requirement**: Developer API Key.
    - Needs access to standard chat completion endpoints.
    - Needs embedding models (e.g., `text-embedding-3-small` or equivalent) for the deduplication engine.
- **Required Keys**: `OPENAI_API_KEY` or `GEMINI_API_KEY`.

## 3. News Aggregation API
- **Service**: GNews API or NewsAPI.org (refer to `research.md`).
- **Requirement**: Developer API Key for searching current events and top headlines.
- **Required Keys**: `NEWS_API_KEY`.

## 4. Email Delivery Service
- **Service**: SendGrid, Postmark, Mailgun, or Resend.
- **Requirement**: Transactional Email API Key.
    - Requires domain authentication (DNS records) to ensure emails do not go to spam.
- **Required Keys**: `EMAIL_API_KEY`, `SENDER_EMAIL_ADDRESS`.

## 5. Hosting / Compute
- **Service**: Google Cloud Platform (Compute Engine).
- **Requirement**: A standard Linux VM (e.g., e2-micro or e2-small running Ubuntu/Debian).
- **Setup**:
    - Needs a static external IP address.
    - Firewall rules allowing HTTP/HTTPS traffic (ports 80/443).
    - SSH key configured for deployment.

## Summary `.env` Template
```env
# Authentication
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# AI Models
LLM_API_KEY=your_openai_or_gemini_key

# News
NEWS_API_KEY=your_news_api_key

# Delivery
EMAIL_API_KEY=your_email_service_key
SENDER_EMAIL_ADDRESS=noreply@yourdomain.com
```
