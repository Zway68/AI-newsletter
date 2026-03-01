# Research: News APIs for AI Newsletter

This document outlines potential news sources and their integration requirements.

## 1. NewsAPI.org
- **Description**: Search through millions of articles from over 80,000 large and small news sources and blogs.
- **Requirements**:
    - **API Key**: Required (Header: `X-Api-Key`).
    - **Free Tier**: 100 requests per day (Developer plan).
    - **Limitations**: No commercial use on the free tier; articles older than 1 month are restricted.
- **Link**: [https://newsapi.org/](https://newsapi.org/)

## 2. GNews API
- **Description**: Simple API to get breaking news and search for articles.
- **Requirements**:
    - **API Key**: Required (Query param `token`).
    - **Free Tier**: 100 requests per day.
    - **Strength**: High quality snippets and "top headlines" feature.
- **Link**: [https://gnews.io/](https://gnews.io/)

## 3. The Guardian API
- **Description**: Access to all the content the Guardian has published since 1999.
- **Requirements**:
    - **API Key**: Required.
    - **Free Tier**: 5,000 calls per day (Developer plan).
    - **Strength**: High quality, long-form content, generous free tier for personal projects.
- **Link**: [https://open-platform.theguardian.com/](https://open-platform.theguardian.com/)

## 4. Mediastack
- **Description**: Real-time news API for worldwide news, headlines, and blog posts.
- **Requirements**:
    - **API Key**: Required.
    - **Free Tier**: 500 requests per month.
- **Link**: [https://mediastack.com/](https://mediastack.com/)

## 5. Summary of Implementation Requirements
To use any of these, we need:
1.  **API Key Management**: Store keys securely in a `.env` file (local filesystem).
2.  **Rate Limiting**: Implementation must honor the daily limits of the free tiers.
3.  **Caching**: Local news cache (filesystem) to avoid redundant API calls and stay within limits.

## Recommendation
For a starting point, **GNews API** or **NewsAPI.org** offer the most straightforward "search" functionalites for diverse interests.
