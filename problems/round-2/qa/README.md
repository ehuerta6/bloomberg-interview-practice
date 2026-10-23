# Round 2 ticket rendering audit

Issue #13 was audited on 2026-10-22 against commit
`cdfa3a9` (the Markdown renderer merged in PR #26).
All 25 ticket pages passed. No assignment, starter, reference solution, or
renderer changes were needed.

## Review scope

Every Markdown ticket was read alongside its generated page. Each contains a
reported symptom, scenario, acceptance criteria, state invariants, investigation
guidance, starter link, and separate reference solution link. The ticket text
states the required behavior and investigation direction without embedding a
finished implementation or solution explanation. Reference contents are not
loaded into the generated assignment.

The manifest resolves each starter link to the matching `round-2/<ticket>/`
directory. Every target has its Python modules, a `test_*.py` file, and local
`AGENTS.md`. Generated starter links use the canonical repository and matching
folder; reference links remain explicit choices. This audit checks paths and
presentation, not whether the intentionally defective starters pass their tests.

## Page inventory

For every row, source content, rendered sections, starter destination, formatting,
and absence of embedded solution code passed. Python file counts include tests.

| Ticket source | Acceptance criteria | Starter Python files | Result |
| --- | ---: | ---: | --- |
| [01 — Event Registration](../01-event-registration.md) | 4 | 5 | PASS |
| [02 — Order Processing](../02-order-processing.md) | 5 | 7 | PASS |
| [03 — Password Reset Flow](../03-password-reset-flow.md) | 5 | 4 | PASS |
| [04 — Library Book Checkout](../04-library-book-checkout.md) | 5 | 4 | PASS |
| [05 — Refund Processing](../05-refund-processing.md) | 5 | 4 | PASS |
| [06 — Warehouse Shipment Processing](../06-warehouse-shipment-processing.md) | 6 | 4 | PASS |
| [07 — Ticket Seat Holds](../07-ticket-seat-holds.md) | 6 | 4 | PASS |
| [08 — Course Enrollment](../08-course-enrollment.md) | 6 | 4 | PASS |
| [09 — Appointment Rescheduling](../09-appointment-rescheduling.md) | 6 | 4 | PASS |
| [10 — Notification Delivery](../10-notification-delivery.md) | 3 | 5 | PASS |
| [11 — Subscription Renewal](../11-subscription-renewal.md) | 3 | 5 | PASS |
| [12 — Digital Wallet Ledger](../12-digital-wallet-ledger.md) | 3 | 4 | PASS |
| [13 — Invoice Reconciliation](../13-invoice-reconciliation.md) | 3 | 4 | PASS |
| [14 — Checkout Promotion Engine](../14-checkout-promotion-engine.md) | 3 | 5 | PASS |
| [15 — Session Revocation](../15-session-revocation.md) | 3 | 4 | PASS |
| [16 — Content Moderation Workflow](../16-content-moderation-workflow.md) | 3 | 4 | PASS |
| [17 — Background Job Queue](../17-background-job-queue.md) | 3 | 4 | PASS |
| [18 — Support Ticket Assignment](../18-support-ticket-assignment.md) | 5 | 5 | PASS |
| [19 — Parking Permit Management](../19-parking-permit-management.md) | 5 | 5 | PASS |
| [20 — Team Invitation System](../20-team-invitation-system.md) | 5 | 5 | PASS |
| [21 — Data Import Pipeline](../21-data-import-pipeline.md) | 5 | 5 | PASS |
| [22 — Shared Document Permissions](../22-shared-document-permissions.md) | 5 | 5 | PASS |
| [23 — Product Returns & Exchanges](../23-product-returns-exchanges.md) | 5 | 5 | PASS |
| [24 — Multi-Location Inventory](../24-multi-location-inventory.md) | 5 | 5 | PASS |
| [25 — Webhook Event Processing](../25-webhook-event-processing.md) | 5 | 5 | PASS |

## Verification evidence

- `python3 scripts/generate_manifest.py --check`: current, with 25 Round 2
  entries and 65 total problems.
- `python scripts/build-site.py --check` using the pinned build dependencies:
  all 65 generated problem pages current.
- `python -m unittest discover -s scripts -p 'test_build_site.py' -v`:
  18 tests passed, including safe links, escaping, output preservation, and
  deterministic generation.
- Chromium through Playwright: all 25 Round 2 pages loaded at 1280×900 and
  390×900 (50 page/viewport checks). Each returned HTTP 200, retained the full
  source text in order after normalizing Markdown and whitespace, exposed the
  required section headings and matching starter URL, loaded CSS and logo, and
  had no horizontal document overflow. Body text was 16px. No page loaded a
  script or contained a fenced implementation. Mobile screenshot and snapshots
  were also inspected for heading wrapping and readable text flow.
- Git diff review: the audit document is the only changed file; numbered ticket
  sources, generated pages, `round-2/`, and `solutions/` remain unchanged.

To repeat the browser checks, install the pinned dependencies using
[`scripts/build-site.md`](../../../scripts/build-site.md), serve `docs/`, and
visit each `docs/problems/round-2-*.html` at the two viewport sizes above. Compare
article text with its linked Markdown source, verify the sections and starter
URL, and inspect document overflow and asset loading.

At this revision, catalog navigation targets `docs/index.html`, which is supplied
by issue #11. Catalog integration is outside this ticket-content audit. The local
server also returned a harmless missing `favicon.ico` request; the ticket,
stylesheet, and logo requests succeeded. External GitHub pages were validated by
their repository paths rather than by navigating to every hosted link.
