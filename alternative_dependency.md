# Alternative Dependencies & Tradeoff Analysis

When building the AI Newsletter on a local-first/budget-friendly stack, choosing the right external APIs is critical to avoid unexpected costs or service interruptions. This document outlines the tradeoffs for each major component.

## 1. News Aggregation APIs

The core constraint for news APIs is the combination of **Requests per day** and **Articles per request**.

### Option A: GNews API (Recommended)
*   **Free Tier Limit**: 100 requests / day.
*   **Articles per Request**: Up to 10.
*   **What this translates to**: You can fetch up to **1,000 top headlines/articles per day**.
*   **Tradeoffs**:
    *   *Pros*: High-quality snippets are usually sufficient for LLM summarization without needing to scrape the full article body. Returns "top headlines" natively.
    *   *Cons*: Free tier has a 12-hour delay on news and limits history to 30 days. No full article content.
*   **Verdict**: Best for a daily/weekly newsletter where a 12-hour delay is acceptable and full article scraping isn't strictly required.

### Option B: NewsAPI.org
*   **Free Tier Limit**: 100 requests / day.
*   **Articles per Request**: Up to 100.
*   **What this translates to**: You can fetch up to **10,000 articles per day**.
*   **Tradeoffs**:
    *   *Pros*: Massive volume per request. Very mature ecosystem.
    *   *Cons*: Free tier has a **24-hour delay**. Strictly forbidden for commercial use or production environments (development/testing only).
*   **Verdict**: Good for initial prototyping and testing the deduplication engine with large volumes of data, but not suitable for a "live" personal or commercial newsletter due to the 24-hour delay and licensing restrictions.

### Option C: The Guardian API
*   **Free Tier Limit**: 5,000 requests / day.
*   **Tradeoffs**:
    *   *Pros*: Huge generous free tier. Access to high-quality, long-form journalism.
    *   *Cons*: Limited exclusively to The Guardian's content. Will not provide a diverse overview of global news from multiple sources.

## 2. Email Delivery Services

### Option A: SendGrid
*   **Free Tier Limit**: 100 emails / day (Forever free API plan).
    *   *(Note: There is a 30-day trial of 40k emails, but it reverts to 100/day).*
*   **What this translates to**: You can support a maximum of **100 individual subscribers** receiving a daily newsletter, or accommodate combinations (e.g., 20 users getting 5 different topic newsletters daily).
*   **Tradeoffs**: Industry standard, excellent deliverability, but a hard cap at 100/day forces a paid tier early if the user base grows.

### Option B: Resend
*   **Free Tier Limit**: 100 emails / day (3,000 per month).
*   **Tradeoffs**: Modern API, great developer experience, specifically built for modern stacks. Same volume limitation as SendGrid.

### Option C: SMTP Relay (e.g., Gmail/Google Workspace)
*   **Limit**: Varies (Standard Gmail is ~500/day, Workspace is higher).
*   **Tradeoffs**:
    *   *Pros*: Higher daily limits for free.
    *   *Cons*: High risk of being flagged as spam if sending bulk newsletters. Difficult to handle bounces/unsubscribes programmatically. Not recommended for a scalable application.

## 3. LLM Engines

### Option A: OpenAI (GPT-4o / GPT-4o-mini)
*   **Cost Structure**: Pay-as-you-go based on tokens.
*   **Tradeoffs**: `gpt-4o-mini` is extremely cheap and fast, perfect for high-volume summarization. Embeddings (`text-embedding-3-small`) are also highly cost-effective for the deduplication engine.

### Option B: Google Gemini (Gemini 1.5 Flash)
*   **Cost Structure**: Generous free tier (up to 15 requests per minute, 1M tokens per minute).
*   **Tradeoffs**:
    *   *Pros*: You can run the summarization engine essentially for free for a small-to-medium user base. Includes massive context windows (good for summarizing a whole month's worth of data).
    *   *Cons*: Rate limits on the free tier might cause bottlenecks during the cron job execution if many users are processed concurrently.

## Conclusion & Recommended Budget Stack
For a cost-effective, multi-user deployment on GCP:
1.  **News**: **GNews API** (100 req/day is plenty if queries are batched per topic rather than per user).
2.  **Delivery**: **SendGrid or Resend** (Limits the platform to <100 daily deliveries for free, scaling requires payment).
3.  **LLM**: **Gemini 1.5 Flash** (Utilize the free API limits to keep processing costs at zero).
