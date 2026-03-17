## [LRN-20260317-001] best_practice

**Logged**: 2026-03-17T02:04:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
General web search is unreliable for time-sensitive, localized data (like used car listings); direct fetching and parsing of source URLs is required.

### Details
When users ask for specific, time-sensitive, and highly localized data (like used car listings, real estate, or job postings), general web search (Google/Bing) often returns outdated SEO pages, aggregated lists, or hallucinated details with broken links. To ensure accuracy, it is necessary to prioritize directly fetching the source URLs (e.g., Craigslist search URLs, specific dealer inventory pages) and parsing the actual HTML/JSON content, rather than trusting the snippets provided by the search engine. Furthermore, it is critical to always verify that the links provided in the final output actually exist and point to the specific item, not just a general homepage or a 404 page.

### Suggested Action
When tasked with finding live, localized listings (cars, real estate, jobs), bypass general search engines for the final data. Instead, construct search URLs for known listing sites (like Craigslist), fetch the pages directly, parse the results, and verify all outgoing links before presenting them to the user.

### Metadata
- Source: user_feedback
- Related Files: 
- Tags: web_search, data_fetching, hallucinations, verification, scraping
- Pattern-Key: harden.data_fetching

---
