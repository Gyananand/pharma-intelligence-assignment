# Task 1 – Company Website Scraper

## Overview
This project implements a lightweight, honest web scraper that extracts structured company information from publicly accessible company websites.

The scraper is designed to handle real-world variability in website structure by:
- Dynamically discovering relevant pages
- Extracting only verifiable information
- Explicitly logging missing or unavailable data
- Avoiding any hallucination or assumption

Design principle:
**Explore broadly, but decide selectively.**

---

## What the Scraper Does
Given a company website URL, the scraper attempts to extract:

### A. Identity
- Company name (normalized from metadata or page title)
- Website URL
- Tagline / meta description (if available)

### B. Business Signals
- Discovery of key business pages such as:
  - About / Company
  - Products / Portfolio
  - Research / Science
  - Careers
  - Contact

### C. Evidence
- Detected business-relevant pages grouped by intent
- Social media links (LinkedIn, Twitter/X, Instagram, YouTube)

### D. Contact & Hiring Signals
- Emails (if publicly visible)
- Phone numbers (best-effort)
- Contact page URL
- Careers page URL (if present)

### E. Metadata
- Timestamp of scrape
- Pages crawled
- Errors or access issues
- Notes explaining limitations or ambiguity

---

## How It Works (High-Level)
- Starts from the homepage
- Dynamically discovers links using anchor text and URL intent
- Filters links based on business relevance
- Limits crawl depth and total pages to avoid noise
- Extracts information only when confidence is high
- Marks fields as `null` when reliable extraction is not possible

---

## Scraping Rules Followed
- Only publicly accessible pages are scraped
- No login-required or gated content
- Maximum crawl depth: 2
- Maximum pages visited: 15
- Same-domain crawling only
- No inference or guessing of missing information

---

## Demo Websites Used (Task Requirement)

The scraper was tested on the following real company websites:

1. **BioGaia**
   - URL: https://www.biogaia.com
   - Output: `outputs/biogaia_output.json`

2. **Abbott Nutrition**
   - URL: https://www.abbottnutrition.com
   - Output: `outputs/abbott_output.json`

3. **Himalaya Wellness** (additional validation)
   - URL: https://himalayawellness.in
   - Output: `outputs/himalaya_output.json`

The first two sites serve as the required demo runs.  
The third site was tested to validate robustness across different website structures.

---
## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Run the scraper

```bash
python scraper.py
```

### 3. Provide input

When prompted, enter a company website URL:

```text
Enter company website URL: https://www.example.com
```

The output will be saved automatically as a JSON file inside the `outputs/` folder.
