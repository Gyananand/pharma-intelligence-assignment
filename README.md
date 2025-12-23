# Pharma Intelligence Assignment

This repository contains my submission for the Pharma Intelligence take-home assignment.

The objective of the assignment is to:
- Build a lightweight, honest company website scraper
- Extract structured business signals from public websites
- Classify companies based on their involvement in the probiotics domain

---

## Repository Structure

### Task 1 — Company Website Scraper
**Folder:** `Task_1_Scrapper/`

- Python-based scraper to extract structured company information
- Crawls only public pages with controlled depth and page limits
- Outputs clean, structured JSON files
- Includes:
  - `scraper.py`
  - `requirements.txt`
  - `outputs/` (demo runs)
  - Detailed README with usage instructions

Start here if you want to understand the scraping logic.

---

### Task 2 — Probiotics Company Classification
**Folder:** `Task_2_Company_Profiling/`

- Framework to classify companies as:
  - Probiotics-focused
  - Probiotics-adjacent
  - Not relevant
- Uses only website evidence extracted in Task 1
- Includes:
  - `task2_classification.md` with full reasoning, framework, and scraper logic

Start here to see how scraped data is converted into decision-usable intelligence.

---

## How to Navigate
1. Read the **Task 1 README** to understand the scraper
2. Review the **JSON outputs** from demo runs
3. Read **Task 2 classification** to see how decisions are made

No external data sources or assumptions were used beyond public website content.
