# GEO Remediation Sequence — Reasoning

**Date:** 2026-10-13  
**Site kind:** Chrome extension / local-first archive tool (`SoftwareApplication` + `HowTo` + `FAQPage` + `Product` schema). Not a news publisher; citation depth is lower weight than entity recognition.

## Why This Order

1. **Schema.organization (C) first:** The GEO `evidence.stamp` is CURRENT (17 pages scored). The `content.expertise` finding (priority 1, +4.05 impact) requires a `Person` node linked to `sameAs`. Without the parent `Organization` node completed first, the `author` linkage is orphaned. The SEO `schema` category is already 90; completing the node recovers 12.59 points at the lowest editorial cost.
2. **Freshness (D) before evidence (B):** The GEO `content.freshness` score is 0/25 across all 17 pages (`reason`: `no date on the page`). The `evidence_density` recommendation requires specific dates and versions to be cited. Adding dates before the editorial citation pass avoids rewriting citations a second time.
3. **Depth (E) after evidence (B):** The two thin pages (`es/support`, `pt-br/support`) need a complete answer, constraints, and a worked case. Embedding cited evidence inside those expanded sections is more efficient than expanding blank text and then inserting citations after.
4. **Hreflang (F) parallel:** Independent of content; can run concurrently with B.
5. **Schema breadth (H) last:** Template-level; depends on page-level schema being stable so `FAQPage`/`HowTo` mappings are accurate.

## What This Site Is Not

A publication site would weight `content.expertise` and `citability.evidence_density` above `platform.hreflang` and `platform.feeds`. A syntax reference site would weight `technical` and `content.readability` above `eeat-citations`. This site (extension + archive tool) benefits most from: (1) clear entity identity (`Organization`), (2) verifiable freshness (`dateModified`), and (3) machine-readable authorship (`Person`). Those three recover 43.66 of the 77 lost points.
