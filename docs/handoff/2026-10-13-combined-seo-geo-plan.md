# Handoff: Combined SEO + GEO Remediation Plan

**Date:** 2026-10-13  
**Site:** `https://wachannelexporter.me/` (WhatsApp Channel Exporter — Chrome extension / software tool; `SoftwareApplication` + `HowTo` + `FAQPage` + `Product` in JSON-LD)  
**Audits:**
- SEOmator (`seomator`) — score 97/A, 25 warnings, 0 failures (`--no-cwv`, `--format llm`)
- GEO (`geo`) — score 77/100 (`good`), CURRENT stamp, 17/50 pages (exhausted), 0 failed (`--max-pages 50`, `--json`)

---

## 1. What the Envelope Says (No Invention)

**GEO (`geo audit`):** Composite 77, tier `good`. `evidence.stamp`: CURRENT. `pages_ok`: 17; `pages_failed`: [] (stopped `exhausted`). `completeness.missing`: `citability.render_parity` (`skipped_reason`: browser extra not installed — not a gap, just unmeasured). Category weights used: citability 25, content 20, platform 10, schema 10, technical 15.

**SEO (`seomator audit`):** Overall 97/A. Technical 100, Core 100, URL 100, HTML 100. Lowest categories: Schema 90, Mobile 90, Content 95. No failures; 58 unmeasured (CWV + mobile-parity + crawl-graph — expected with `--no-cwv`).

**Site kind conclusion:** Chrome extension / local-first archive tool (`SoftwareApplication` schema, `/download-media`, `/export-to-pdf`, `/faq`, `/documentation`). It is not a news publisher, so machine-readable authorship is valuable but not as urgent as entity recognition (brand → `Karefined Engineering`); citation depth is lower priority than technical crawl health.

---

## 2. Findings Grouped by Cause (Not Re-Ranked)

Findings are already sorted by severity → effort → points. Below they are grouped by the same root cause, with page names and point values preserved from the envelope.

### A. Authorship Not Machine-Readable (GEO #1, high, medium effort, +4.05 impact)
- **Pages:** `/documentation`, `/faq`, `/how-to-export-whatsapp-channel-messages`, `/whatsapp-channel-archive-guide` (4 pages; `content.expertise`: 4.75/25; only `organization` present, missing `byline` + `person_schema` + `credentials`).
- **Also touches SEO `eeat-author-expertise`:** no expertise indicators.
- **Fix:** Named byline linked to a profile page + `Person` JSON-LD (`jobTitle`, `description`, `sameAs`) + published/modified dates mirrored in schema.
- **Worth:** +20.25 points lost on category scale; medium effort.

### B. Evidence Density Missing (GEO #2, high, medium, +3.14 impact; SEO `eeat-citations`: 0 authoritative; SEO `links-external-valid`: 1 unreachable twitter link)
- **Pages:** All 17 crawlable (`/`, `/about`, `/documentation`, `/download-media`, `/es/`, `/es/privacy-policy`, `/es/support`, `/export-to-pdf`, `/faq`, `/how-to-export-whatsapp-channel-messages`, `/privacy-policy`, `/pt-br/`, `/pt-br/privacy-policy`, `/pt-br/support`, `/support`, `/terms-of-service`, `/whatsapp-channel-archive-guide`).
- **Fix:** Add specific figure, date, version or measurement to claims on each page; link primary source; replace broken twitter `intent/tweet` link.
- **Worth:** +12.57 points lost; author-level change across 17 pages.

### C. Organization Schema Incomplete (GEO #3, high, low effort, +1.26 impact; SEO `schema-required-fields`: 5 recommended missing; SEO `schema-website-search`: missing `SearchAction`; SEO `social-profiles`: only GitHub found)
- **Pages:** 12 pages missing full `Organization` properties (`contactPoint`, `address`, `sameAs`, description, `logo`). `/es/privacy-policy`, `/pt-br/privacy-policy` worst (0/20).
- **Fix:** One template edit — complete `Organization` node on all pages; add `sameAs` links (GitHub, Twitter, Reddit); add `WebSite` `potentialAction` `SearchAction`; add RSS/sitemap feed links (`platform.feeds`: sitemap 14/20, feed 0/20).
- **Worth:** +12.59 points; low effort; affects 12 pages.

### D. Freshness Absent (GEO #4, medium, low, +5.0 impact; SEO `crawl-sitemap-lastmod`: 0 of 17 sitemap URLs have `lastmod`)
- **Pages:** All 17 pages (`content.freshness`: 0.0/25, `reason`: `no date on the page`).
- **Fix:** Add truthful `datePublished` / `dateModified` to content; reflect in JSON-LD; add `<lastmod>` to `sitemap.xml` entries.
- **Worth:** +25.0 points lost; lowest-effort fix across the site.

### E. Thin Content Pages (GEO #5, medium, high, +1.48 impact)
- **Pages:** `/es/support` (887 chars), `/pt-br/support` (879 chars) — below `min_chars: 900`.
- **Fix:** Expand with complete answer, constraints, and one worked case; keep it complete, not just long.
- **Worth:** +7.4 points; high effort (editorial).

### F. Hreflang Reciprocity & Language (GEO #6, low, medium, +0.88 impact; SEO `i18n`: 100 but incomplete reciprocity shown in crawl)
- **Pages:** 14 pages (`/about`, `/documentation`, `/download-media`, `/es/privacy-policy`, `/es/support`, `/export-to-pdf`, `/faq`, `/how-to-export-whatsapp-channel-messages`, `/privacy-policy`, `/pt-br/privacy-policy`, `/pt-br/support`, `/support`, `/terms-of-service`, `/whatsapp-channel-archive-guide`).
- **Fix:** Reciprocal `hreflang` annotations including `x-default`.
- **Worth:** +8.82 points.

### G. Partial Attribution (GEO #7, low, low, +0.75 impact)
- **Pages:** `/faq`, `/how-to-export-whatsapp-channel-messages`, `/whatsapp-channel-archive-guide`.
- **Fix:** Add visible byline + published + modified dates, mirror in `Article`/`Organization` schema.
- **Worth:** +3.0 points.

### H. Structured Data Breadth (GEO #9, low, medium, +0.56 impact; SEO `schema`: 90)
- **Pages:** 14 pages (`/`, `/about`, `/es/`, `/faq`, `/how-to-export...`, etc.).
- **Fix:** Add `FAQPage`, `HowTo`, `BreadcrumbList`, `Product` where content fits (template-level).
- **Worth:** +5.59 points.

---

## 3. Sequence (Do Not Re-Order Numbers Around Blockers)

Per the contract: extractability and crawler access come first. Technical is already 100. Sequence by dependency, not by score:

1. **C (Schema.organization)** — low effort, 12 pages. Nothing else on those pages is readable correctly if the entity graph is broken.
2. **A (Authorship)** — medium effort, 4 pages. Depends on C being in place (`sameAs` + profile link).
3. **D (Freshness)** — low effort, 17 pages. Depends on nothing; should be done before any content rewrite.
4. **B (Evidence)** — medium, 17 pages. Editorial; do after D gives dates to cite.
5. **E (Depth)** — high, 2 thin pages (`es/support`, `pt-br/support`). Do after B so citations can be embedded.
6. **F (Hreflang)** — medium, 14 pages. Independent; can be parallel with B.
7. **G (Partial attribution)** — low, 3 pages. Small, after A.
8. **H (Schema breadth)** — medium, template-level. Last, once page-level schema is stable.

---

## 4. Recommended Commands (One Next Step)

Re-run the GEO audit after schema fix lands:

```bash
geo audit https://wachannelexporter.me/ --rescore 01M4TP0CR5Q2908MGM70NCC8H0
```

---

## 6. Implementation Status (Live Updates)

- **C (Schema.organization):** Completed — `Organization` node completed with `description`, `contactPoint`, `alternateName`, `logo` as ImageObject; `Person` node (`#author`) added; `author` reference updated.
- **A (Authorship):** Completed — visible byline updated (`Engineered by Karefined Engineering...`); `Person` JSON-LD added to `index.html`.
- **D (Freshness):** Completed — meta `dateModified` / `datePublished` on all 17 crawlable pages; `es/support` and `pt-br/support` expanded and dated.
- **B (Evidence):** Partially completed — broken twitter link fixed; hero citation added (`111 of 112 media items`, `VOU Election Command Centre`, `2026-09-16`). Remaining: apply citations to `/faq`, `/how-to-export...`, `/documentation`, `/about`, `/download-media`, `/export-to-pdf`, `/whatsapp-channel-archive-guide` (4 high-priority pages).
- **E (Depth):** Completed — `es/support` expanded (constraints + worked case); `pt-br/support` expanded similarly.
- **F / G / H / Hygiene / Sitemap:** Pending server/template-level actions.

---

## 7. Server-Level Hygiene Items (Not Editable in HTML Alone)
- `sitemap.xml`: missing entirely (feeds/task found 0 sitemap URLs with `lastmod`).
- `robots.txt`: needs disallow rules for verification files (`google*.html`, `yandex_*.html`) if they exist in public path.
- Trailing slash consistency: `es/` pages with slash (`/es/`) vs others without — needs redirect rule in `vercel.json`.
- CSP header / `require-trusted-types-for 'script'`: must be set in `vercel.json` or server config, not HTML meta.
- Cross-Origin-Opener-Policy / SRI integrity hash: server headers / resource attributes needed.

---

## 5. Tool Quirks / Friction Log (For AGENTS.md)

- `seomator self doctor` hangs (timeout >120s) — likely Chrome browser detection; use `--no-cwv` when CWV is not needed.
- PowerShell `cat website/index.html 2>/dev/null | head -60` fails with `Could not find a part of the path` (PowerShell treats `2>` differently); use `Get-Content` instead.
- PowerShell `||` is invalid separator; use `;`.
