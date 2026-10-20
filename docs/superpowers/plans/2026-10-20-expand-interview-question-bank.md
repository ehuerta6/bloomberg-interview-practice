# Expand Interview Question Bank Implementation Plan

> **For agentic workers:** Use the supplied exercise workflow and finish each five-problem batch before starting the next.

**Goal:** Expand the repository into a standard-library Python bank of 25 PR reviews and 25 engineering tickets, with starter defects, complete reference solutions, and minimal static pages.

**Architecture:** Preserve the current five starter exercises and their solutions. Add each problem in its own numbered directory under `round-1/` or `round-2/`, mirror it under `solutions/`, and publish its assignment at the existing `docs/challenges/` URL pattern. Keep homepage metadata in one static manifest and generate no runtime application or build system.

**Tech Stack:** Python standard library (`unittest`), static HTML/CSS, minimal vanilla JavaScript only if needed.

**Spec:** User request in this conversation (50-problem question bank).

## Global Constraints

- Exactly 25 problems per round; all 50 have starter code, assignment pages, and reference solutions.
- Round 1 uses one Python file with implementation and `unittest` tests plus `AGENTS.md`.
- Round 2 uses approximately 3–7 meaningful Python files including tests, in-memory state, and fake adapters.
- Starter implementations contain plausible intentional defects and tests; solutions contain corrected tests and beginner-friendly reasoning.
- Every exercise uses Python's standard library and keeps concise, consistent AI-helper instructions.
- Existing exercises 01–03 in Round 1 and 01–02 in Round 2, and their solutions, remain byte-for-byte unchanged.
- Website is static HTML/CSS, monochrome, responsive, and contains only the requested problem listings and assignment content.
- Do not merge to `main`; create the requested feature branch and open a PR only after review and verification.

## Confirmed Inventory

### Round 1 — Pull Request Reviews

01 Code Validator; 02 Event Scheduler; 03 Cappy's Snack Inventory; 04 Coupon Eligibility; 05 Session Token Expiration; 06 API Pagination; 07 Notification Deduplication; 08 File Upload Validation; 09 Gradebook Aggregation; 10 CSV Import Parser; 11 URL Query Parameter Parser; 12 Seat Allocation; 13 LRU Cache; 14 Request Rate Limiter; 15 Balance Transfer; 16 Log Filtering; 17 Search Ranking; 18 Dependency Resolution; 19 Feature Flag Evaluation; 20 Shipping Fee Calculator; 21 Retry Backoff Planner; 22 Access Permission Checker; 23 Reservation Expiration; 24 Data Merge Reconciliation; 25 Rolling Analytics Window.

### Round 2 — Engineering Tickets

01 Event Registration; 02 Order Processing; 03 Password Reset Flow; 04 Library Book Checkout; 05 Refund Processing; 06 Warehouse Shipment Processing; 07 Ticket Seat Holds; 08 Course Enrollment; 09 Appointment Rescheduling; 10 Notification Delivery; 11 Subscription Renewal; 12 Digital Wallet Ledger; 13 Invoice Reconciliation; 14 Checkout Promotion Engine; 15 Session Revocation; 16 Content Moderation Workflow; 17 Background Job Queue; 18 Support Ticket Assignment; 19 Parking Permit Management; 20 Team Invitation System; 21 Data Import Pipeline; 22 Shared Document Permissions; 23 Product Returns & Exchanges; 24 Multi-Location Inventory; 25 Webhook Event Processing.

## Work Plan

Each exercise batch closes its loop before the next begins: write the detailed PR/ticket specification; add plausible starter code and 6–10 relevant tests with a mix of useful passes, meaningful failures, and deliberate gaps; build the corrected independent solution and expanded regression tests; add the assignment page; run starter/solution checks; and review for realism and duplication.

### Task 1: Baseline and repository structure

**Files:** existing README, all original starter/solution directories, existing assignment pages, `docs/index.html`, `docs/assets/styles.css`, and repo instructions.

- [ ] Record the existing five starter and solution contents for byte-for-byte preservation.
- [ ] Confirm conventions, existing URLs, and baseline runnable commands.

### Tasks 2–6: Round 1 new exercises (five batches)

**Files:** `round-1/04-*` through `round-1/25-*`, matching `solutions/round-1/*`, and matching `docs/challenges/r1-*.html`.

- [ ] Task 2: 04–08 Coupon Eligibility, Session Token Expiration, API Pagination, Notification Deduplication, File Upload Validation.
- [ ] Task 3: 09–13 Gradebook Aggregation, CSV Import Parser, URL Query Parameter Parser, Seat Allocation, LRU Cache.
- [ ] Task 4: 14–18 Request Rate Limiter, Balance Transfer, Log Filtering, Search Ranking, Dependency Resolution.
- [ ] Task 5: 19–23 Feature Flag Evaluation, Shipping Fee Calculator, Retry Backoff Planner, Access Permission Checker, Reservation Expiration.
- [ ] Task 6: 24–25 Data Merge Reconciliation, Rolling Analytics Window.

### Tasks 7–11: Round 2 new exercises (five batches)

**Files:** `round-2/03-*` through `round-2/25-*`, matching `solutions/round-2/*`, and matching `docs/challenges/r2-*.html`.

- [ ] Task 7: 03–07 Password Reset Flow, Library Book Checkout, Refund Processing, Warehouse Shipment Processing, Ticket Seat Holds.
- [ ] Task 8: 08–12 Course Enrollment, Appointment Rescheduling, Notification Delivery, Subscription Renewal, Digital Wallet Ledger.
- [ ] Task 9: 13–17 Invoice Reconciliation, Checkout Promotion Engine, Session Revocation, Content Moderation Workflow, Background Job Queue.
- [ ] Task 10: 18–22 Support Ticket Assignment, Parking Permit Management, Team Invitation System, Data Import Pipeline, Shared Document Permissions.
- [ ] Task 11: 23–25 Product Returns & Exchanges, Multi-Location Inventory, Webhook Event Processing.

### Task 12: Question bank website and repository guide

**Files:** `docs/index.html`, `docs/assets/styles.css`, `docs/assets/app.js` if required, all 50 pages under `docs/challenges/`, and `README.md`.

- [ ] Replace decorative portal with a black-and-white two-list homepage and retain the original five assignment URLs.
- [ ] Give every problem a detailed page with its title, PR/ticket requirements, investigation/review task, starter link, and solution link.
- [ ] Update README to describe the question bank without workshop onboarding or obsolete exercise totals.

### Task 13: Full quality and consistency audit

**Files:** all starter, solution, and website artifacts.

- [ ] Run all corrected solution tests and representative starter tests; preserve and verify the original five baseline files.
- [ ] Script-check 25+25 counts, matching starter/solution/page directories, all local page and solution links, and standard-library imports.
- [ ] Review starter defects, test quality, difficulty distribution, duplicate patterns, monochrome design, and absence of onboarding/copy/timer UI.
- [ ] Commit in logical batches using conventional commit messages; push the feature branch and open an unmerged PR if remote access supports it.

Difficulty target across the bank: 10 Easy, 30 Medium, 10 Hard. Difficulty labels are exposed on the homepage; assign them from investigation and edge-case load, not file size.

## Review Focus

- Exact boundary conditions for timestamps, expirations, windows, retries, and pagination require deterministic tests with injected clocks/cursors.
- Rejections and downstream failures must leave state consistent; ticket solutions need regression tests for rollback and idempotent retries.
- Stable output requires deterministic tie-breaks, duplicate handling, and explicit conflict rules.
- Authentication/authorization exercises must distinguish identity, ownership, role, revocation, and explicit deny behavior.
- Decimal prices, rounding, missing data, and partial records need specified representations and observable expected results.
