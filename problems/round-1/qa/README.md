# Round 1 rendering audit

Issue [#12](https://github.com/ehuerta6/bloomberg-interview-practice/issues/12).
Audit performed on 2026-10-22 (America/Denver), against the renderer and generated
pages at commit `cdfa3a9` (merged #10).

All 25 Round 1 pages passed. No assignment or rendering defect was found, so no
contract change was needed. This issue adds the audit evidence and its focused
checker. The 25 assignment files, generated pages, starter source, and reference
solutions retain their baseline bytes.

## What was checked

- Read all 25 Markdown contracts and compared their complete visible article text
  with the corresponding generated page, normalizing whitespace only. This covers
  every requirement, summary, review task, and input/output description.
- Compared inline code strings in order, preserving operators, signatures,
  timestamps, interval boundaries, and literal values. These assignments contain
  inline code; they have no fenced code blocks.
- Verified the page identity, Round 1 / Code Review category, and difficulty label
  against the manifest. The source difficulty remains visible inside the article.
- Verified one starter link and one explicit reference solution link per article,
  pointing to the corresponding repository directories. The manifest validates
  that those directories exist. No solution content is embedded or automatically
  fetched; ordinary pages contain no scripts.
- Loaded all 25 pages in Chromium at 1440×900 and 390×844 through a local HTTP
  server. Each returned HTTP 200, loaded the shared stylesheet and CIC logo,
  displayed inline code in a monospace font, and stayed within the viewport
  (`document.documentElement.scrollWidth <= innerWidth`). The shipping calculator
  page's long signatures and names were also inspected visually at 390 pixels.

The table records list-item counts (including the ACL shape list for #22) and
inline-code counts. PASS means the full set of checks above passed for that page.

| Problem | Difficulty | List items | Code spans | Result |
| --- | --- | ---: | ---: | --- |
| [01 — Code Validator](../01-code-validator.md) | Easy | 4 | 3 | PASS |
| [02 — Event Scheduler](../02-event-scheduler.md) | Medium | 5 | 4 | PASS |
| [03 — Cappy's Snack Inventory](../03-snack-inventory.md) | Easy | 5 | 0 | PASS |
| [04 — Coupon Eligibility](../04-coupon-eligibility.md) | Medium | 5 | 3 | PASS |
| [05 — Session Token Expiration](../05-session-token-expiration.md) | Medium | 4 | 3 | PASS |
| [06 — API Pagination](../06-api-pagination.md) | Hard | 5 | 7 | PASS |
| [07 — Notification Deduplication](../07-notification-deduplication.md) | Medium | 5 | 2 | PASS |
| [08 — File Upload Validation](../08-file-upload-validation.md) | Easy | 5 | 4 | PASS |
| [09 — Gradebook Aggregation](../09-gradebook-aggregation.md) | Medium | 7 | 12 | PASS |
| [10 — CSV Import Parser](../10-csv-import-parser.md) | Medium | 5 | 6 | PASS |
| [11 — URL Query Parameter Parser](../11-url-query-parameter-parser.md) | Easy | 5 | 2 | PASS |
| [12 — Seat Allocation](../12-seat-allocation.md) | Hard | 6 | 2 | PASS |
| [13 — LRU Cache](../13-lru-cache.md) | Medium | 6 | 3 | PASS |
| [14 — Request Rate Limiter](../14-request-rate-limiter.md) | Hard | 5 | 6 | PASS |
| [15 — Balance Transfer](../15-balance-transfer.md) | Medium | 5 | 5 | PASS |
| [16 — Log Filtering](../16-log-filtering.md) | Easy | 5 | 4 | PASS |
| [17 — Search Ranking](../17-search-ranking.md) | Medium | 6 | 8 | PASS |
| [18 — Dependency Resolution](../18-dependency-resolution.md) | Hard | 6 | 3 | PASS |
| [19 — Feature Flag Evaluation](../19-feature-flag-evaluation.md) | Medium | 4 | 7 | PASS |
| [20 — Shipping Fee Calculator](../20-shipping-fee-calculator.md) | Medium | 6 | 18 | PASS |
| [21 — Retry Backoff Planner](../21-retry-backoff-planner.md) | Medium | 4 | 7 | PASS |
| [22 — Access Permission Checker](../22-access-permission-checker.md) | Hard | 7 | 10 | PASS |
| [23 — Reservation Expiration](../23-reservation-expiration.md) | Medium | 4 | 13 | PASS |
| [24 — Data Merge Reconciliation](../24-data-merge-reconciliation.md) | Medium | 4 | 5 | PASS |
| [25 — Rolling Analytics Window](../25-rolling-analytics-window.md) | Medium | 4 | 7 | PASS |

## Replay

Install the pinned dependencies as described in
[the build guide](../../../scripts/build-site.md), then run from the repository root:

```sh
/tmp/bloomberg-site-venv/bin/python problems/round-1/qa/audit.py
/tmp/bloomberg-site-venv/bin/python scripts/build-site.py --check
/tmp/bloomberg-site-venv/bin/python -m unittest discover -s scripts -p 'test_build_site.py' -q
python3 scripts/generate_manifest.py --check
git diff cdfa3a9 -- problems/round-1/*.md round-1 solutions/round-1 docs/problems
```

Observed results: 25/25 article audits passed, 18 renderer/build tests passed,
65 generated pages current, manifest current at 25/25/15, and an empty protected
path diff. The audit checker reads neither starter implementations nor reference
solutions. Its assertions fail if visible source text, inline code, labels, or
explicit link destinations drift in a Round 1 generated page.

For browser replay, serve the existing output:

```sh
python3 -m http.server 8122 --bind 127.0.0.1 --directory docs
```

Open `/problems/round-1-01-code-validator.html` through
`/problems/round-1-25-rolling-analytics-window.html`, using the exact slugs in
[`scripts/problem-manifest.json`](../../../scripts/problem-manifest.json), and
repeat at the two viewport sizes above. Check the displayed category/difficulty,
all text/code, and explicit starter/reference links. This review did not navigate
into reference solutions or depend on their contents.

## Integration boundary

The catalog destination `../index.html` is supplied by issue #11. Its availability
was outside this category audit at the tested revision. No hosted CI workflow was
present at this revision; the checks above ran locally. The initial browser
request for `/favicon.ico` returned 404; all tested page, CSS, and logo requests
succeeded. This report does not claim a deployment, cross-browser coverage, or
validation of the exercise implementations.
