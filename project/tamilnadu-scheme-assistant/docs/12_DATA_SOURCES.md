# 12 Data Sources

## Overview
Documentation of verified government data sources used to populate the scheme knowledge base.

## Core Decisions
- **URL Allowlist**: Only `.gov.in`, `.tn.gov.in`, and specific state body domains are considered high-reliability.
- **Costs**: ₹0 (all data sources are public and open).

## Verified Government Portals

| Source Name | URL | Content Type | Language | Reliability | Scraping Feasibility | Update Frequency |
|-------------|-----|--------------|----------|-------------|----------------------|------------------|
| TN Gov Portal | tn.gov.in | HTML, PDF | EN, TA | High (Official) | Medium | Monthly |
| e-Sevai | tnesevai.tn.gov.in | HTML | EN, TA | High | Hard (Dynamic) | Rare |
| MyScheme | myscheme.gov.in | API, HTML | EN, TA | High | Easy (API available) | Frequent |
| CMCHIS | cmchistn.com | HTML, PDF | EN, TA | High | Medium | Medium |
| KMUT | kmut.tn.gov.in | HTML, PDF | TA, EN | High | Medium | Rare |
| Open Data TN | data.tn.gov.in | CSV, JSON | EN | High | Easy | Varies |
| TAHDCO | tahdco.com | HTML | EN, TA | Medium-High | Medium | Rare |

## Reliability Scoring System

Sources are scored 1-10 to determine conflict resolution during ingestion:
1. **Central/State API (MyScheme)**: Score 10 (Gold standard).
2. **State Official Portal (tn.gov.in)**: Score 9.
3. **Department Portals (tahdco.com)**: Score 8.
4. **Verified News/Announcements**: Score 5 (requires manual verification).

## URL Allowlist
Any URL referenced as an `official_url` MUST match this regex or be manually approved:
`^https?:\/\/[a-zA-Z0-9.-]+\.(gov\.in|tn\.gov\.in|tahdco\.com|cmchistn\.com).*$`

## Source Verification Process
1. **Discover**: Identify scheme via news or gov portal.
2. **Cross-Check**: Find the official G.O. (Government Order) or department page.
3. **Draft**: Manually input or auto-scrape into draft status.
4. **Human Review**: Verify eligibility numbers, especially amounts and limits.
5. **Approve**: Move status to `Active`.
