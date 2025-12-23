# Task 2 – Probiotics Company Classification

## Objective
The objective of Task 2 is to determine whether a company is meaningfully involved in the probiotics space using **only publicly available website evidence** extracted during Task 1.  
No external research, Google searches, or assumptions are used.

The goal is to convert scraped website data into **clear, decision-usable classification logic**.

---

## PART 1 — Framework (what we look for and why)

1. **Product Presence**
   - What to look for: dedicated probiotic product pages, product collections, SKU pages with probiotic product names.
   - Why it matters: Direct commercial evidence that the company sells probiotic products.

2. **Technical / Strain Detail**
   - What to look for: mentions of strain names (e.g., Lactobacillus reuteri), CFU counts, strain IDs.
   - Why it matters: Strain-level detail signals scientific maturity and product specificity.

3. **Research / Clinical Evidence**
   - What to look for: dedicated R&D pages, clinical studies, publications, whitepapers.
   - Why it matters: Clinical evidence suggests R&D investment and seriousness.

4. **Regulatory & Quality**
   - What to look for: GMP, ISO, FSSAI, pharma-grade claims, certificate pages.
   - Why it matters: Regulatory signals indicate manufacturing or B2B ingredient intent.

5. **Commercial Intent**
   - What to look for: homepage positioning, marketing that positions probiotics as core product.
   - Why it matters: A product can exist but still be low commercial priority.

---

## PART 2 — Company Profiles

---

### Company 1: BioGaia

**Website:** https://www.biogaia.com  

#### What fits
- Large number of probiotic product pages and collections.
- Probiotics clearly positioned as the primary product offering.
- Dedicated science and research pages focused on probiotics.
- Explicit references to probiotic strains.

#### What does not fit
- No explicit regulatory or certification pages were clearly visible on the public website sections reviewed.
- Some deeper scientific content may exist in PDFs that were not parsed.

#### Website evidence
- Product collections and multiple probiotic SKUs under `/collections/all` and `/products/*`.
- Research and science pages such as:
  - `/pages/science-and-research`
  - `/pages/probiotic-innovation`
- Brand messaging explicitly focused on probiotics and probiotic strains.

#### Final classification
**Probiotics-focused**

**Reasoning:**  
BioGaia’s website shows probiotics as the core business across products, research, and brand positioning. Evidence is strong and consistent.

---

### Company 2: Abbott Nutrition

**Website:** https://www.abbottnutrition.com  

#### What fits
- Structured nutrition product portfolio.
- Dedicated clinical and medical nutrition resources.
- Formal product documentation and clinical guides.

#### What does not fit
- No strain-level probiotic details found.
- Probiotics are not highlighted as a primary product category.
- Core brand focus is broad clinical and medical nutrition, not probiotics specifically.

#### Website evidence
- Product and documentation pages such as:
  - `/our-products`
  - `/product-guides`
- Clinical resources under:
  - `/clinical-resources`
- Multiple PDF references indicating structured nutrition documentation.

#### Final classification
**Probiotics-adjacent**

**Reasoning:**  
Abbott Nutrition operates mainly as a medical and clinical nutrition company. Probiotics may exist within the portfolio but are not the core focus.

---

### Company 3: Himalaya Wellness (Additional validation)

**Website:** https://himalayawellness.in  

#### What fits
- Very large wellness and healthcare product catalog.
- Research pages related to Ayurveda and holistic health.
- Strong consumer wellness positioning.

#### What does not fit
- No probiotic-focused product line detected.
- No strain-level or microbiome-specific information found.
- Probiotics are not positioned as a central theme.

#### Website evidence
- Extensive product listings under `/collections/all`.
- Research and science pages such as:
  - `/pages/our-science`
  - `/pages/research-at-the-heart`
- Brand language focused on herbal and wellness products.

#### Final classification
**Probiotics-adjacent**

**Reasoning:**  
Himalaya Wellness is primarily a herbal and wellness brand. Probiotics, if present, are not a core business area.

---

## PART 3 — Scraper Logic (High-Level)

### Pages to scrape
- Homepage
- About / Company
- Products / Collections
- Research / Science
- Clinical resources
- Certifications / Quality
- Contact / Careers

### Signals to extract
- Probiotic-related keywords (probiotic, strain, CFU, Lactobacillus, Bifidobacterium).
- Number and depth of probiotic product pages.
- Presence of research or clinical sections.
- Structured documentation such as PDFs or clinical guides.
- Homepage and brand positioning language.

### How classification would work
After extracting signals from the targeted pages, the scraper aggregates evidence using a simple scoring model.

**Positive signals**
- Probiotics as a core product category: +5
- Strain-level or CFU-level mentions: +3
- Research, clinical studies, or R&D pages related to probiotics: +2
- Regulatory or quality certifications (GMP, ISO, FSSAI, pharma-grade): +1
- General marketing-level mention of probiotics: +1

**Negative or weak signals**
- One-off or vague mention with no supporting detail: −1
- No probiotic-related products, research, or technical evidence found: −3

**Final classification rules**
- **Probiotics-focused**  
  Score ≥ 6 and probiotics appear as a core product or research area.
- **Probiotics-adjacent**  
  Score between 2 and 5, with indirect or secondary probiotic relevance.
- **Not relevant**  
  Score ≤ 1, with no meaningful probiotic-related evidence on the website.

If required signals are missing or the website is silent, the scraper does not infer intent and applies conservative scoring.

## Final Note
This classification was created strictly using website data scraped in Task 1.  
No external research or assumptions were used.  
When information was ambiguous or unavailable, conservative judgment was applied.

The focus is on **clarity, honesty, and decision usability**, not perfection.
