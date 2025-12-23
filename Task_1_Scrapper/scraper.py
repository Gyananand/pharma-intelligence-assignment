import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re
import json
from collections import deque

# ---------------- CONFIG ---------------- #

HEADERS = {
    "User-Agent": "Mozilla/5.0 (DT-Company-Scraper/1.0)"
}

MAX_PAGES = 15
MAX_DEPTH = 2

INTENT_KEYWORDS = {
    "about": ["about", "about us", "company", "who we are", "our story"],
    "products": ["product", "products", "portfolio", "solutions", "shop"],
    "research": ["research", "science", "clinical", "studies", "innovation", "experts"],
    "careers": ["career", "careers", "jobs", "join", "work with"],
    "contact": ["contact", "get in touch", "reach us"]
}

SOCIAL_DOMAINS = {
    "linkedin": ["linkedin.com"],
    "twitter": ["twitter.com", "x.com"],
    "instagram": ["instagram.com"],
    "youtube": ["youtube.com"]
}

# -------------- HELPERS ---------------- #

def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.text, None
        return None, f"Status code {r.status_code}"
    except Exception as e:
        return None, str(e)

def normalize_url(url):
    return url.split("#")[0].lower()

def extract_emails(text):
    return list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))

def extract_phones(text):
    return list(set(re.findall(r"\+?\d[\d\s\-()]{7,}", text)))

def classify_link(text, href):
    combined = f"{text} {href}".lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in combined for k in keywords):
            return intent
    return None

def clean_company_name(raw_name):
    if not raw_name:
        return None

    separators = ["|", "–", "—", "-"]
    for sep in separators:
        if sep in raw_name:
            raw_name = raw_name.split(sep)[-1].strip()

    blacklist = ["shop", "buy", "official", "online store", "products"]
    lowered = raw_name.lower()
    if any(b in lowered for b in blacklist):
        return raw_name.strip()

    return raw_name.strip()

# -------------- MAIN SCRAPER ---------------- #

def scrape_company(base_url):
    domain = urlparse(base_url).netloc
    visited = set()
    queue = deque([(base_url, 0)])

    output = {
        "identity": {
            "company_name": None,
            "website_url": base_url,
            "tagline": None
        },
        "business_summary": {
            "what_they_do": None,
            "primary_offerings": [],
            "target_segments": []
        },
        "evidence": {
            "key_pages_found": {},
            "social_links": {}
        },
        "contact_location": {
            "emails": [],
            "phones": [],
            "address": None,
            "contact_page": None
        },
        "team_hiring": {
            "careers_page": None
        },
        "metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "pages_crawled": [],
            "errors": [],
            "notes": []
        }
    }

    while queue and len(visited) < MAX_PAGES:
        current_url, depth = queue.popleft()
        current_url = normalize_url(current_url)

        if current_url in visited or depth > MAX_DEPTH:
            continue

        html, error = fetch_page(current_url)
        if error:
            output["metadata"]["errors"].append({current_url: error})
            continue

        visited.add(current_url)
        output["metadata"]["pages_crawled"].append(current_url)

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # -------- HOMEPAGE IDENTITY -------- #
        if depth == 0:
            og_site = soup.find("meta", property="og:site_name")
            if og_site and og_site.get("content"):
                output["identity"]["company_name"] = og_site["content"].strip()
            else:
                title = soup.find("title")
                if title:
                    output["identity"]["company_name"] = clean_company_name(title.text)

            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                output["identity"]["tagline"] = meta_desc.get("content")

        # -------- CONTACT SIGNALS -------- #
        output["contact_location"]["emails"].extend(extract_emails(text))
        output["contact_location"]["phones"].extend(extract_phones(text))

        # -------- SOCIAL LINKS (STRICT DOMAIN) -------- #
        for a in soup.find_all("a", href=True):
            href = a["href"]
            for platform, domains in SOCIAL_DOMAINS.items():
                if any(d in href for d in domains):
                    output["evidence"]["social_links"][platform] = href

        # -------- LINK DISCOVERY -------- #
        for a in soup.find_all("a", href=True):
            href = urljoin(base_url, a["href"])
            parsed = urlparse(href)

            if parsed.netloc != domain:
                continue

            intent = classify_link(a.get_text(strip=True), href)
            if not intent:
                continue

            output["evidence"]["key_pages_found"].setdefault(intent, [])

            if href not in output["evidence"]["key_pages_found"][intent]:
                output["evidence"]["key_pages_found"][intent].append(href)

            if intent == "contact":
                output["contact_location"]["contact_page"] = href
            if intent == "careers":
                output["team_hiring"]["careers_page"] = href

            if normalize_url(href) not in visited:
                queue.append((href, depth + 1))

    # -------- POST PROCESSING -------- #
    output["contact_location"]["emails"] = list(set(output["contact_location"]["emails"]))
    output["contact_location"]["phones"] = list(set(output["contact_location"]["phones"]))

    if not output["business_summary"]["what_they_do"]:
        output["metadata"]["notes"].append(
            "Business summary could not be reliably extracted without heuristic inference."
        )

    return output

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    website = input("Enter company website URL: ").strip()
    result = scrape_company(website)

    OUTPUT_DIR = "outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = website.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"{filename}_output.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Scrape completed. Output saved to {filepath}")

