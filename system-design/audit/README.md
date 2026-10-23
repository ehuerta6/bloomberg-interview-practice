# System Design diagram audit — issue #14

Audited on 2026-10-22 against base `a82c4fd` plus the four corrections below.
The source snapshot is recorded in [sources.sha256](sources.sha256). Markdown
remains authoritative; this directory contains audit evidence and a disposable
preview generator, not a second set of maintained assignments.

## Results

Read all 15 prompts and 15 reference solutions. Every prompt retains its
scenario, requirements, constraints, task, follow-ups, and explicit reference
link. No reference architecture or ERD is embedded in a prompt. Concrete
requirements such as a relational store or private object storage remain part
of the supplied problem scope, rather than being removed as spoilers. Noel's
workshop attribution in prompts/references 01–02 and the category README is
unchanged.

Both diagrams in each reference successfully parsed and rendered with the
site's actual pinned **Mermaid 12.2.0** module in **Chromium 155.0.8059.85** on
macOS. Each successful SVG retained a separate readable source disclosure.
The table records individual diagram results: “SVG” means syntax accepted and
nonempty SVG rendered; “reviewed” means the captured SVG was visually inspected.
It does not mean every visual issue is resolved.

| Reference | Architecture syntax/render | Architecture visual | ERD syntax/render | ERD visual |
|---|---|---|---|---|
| [01 Gym](../../solutions/system-design/01-gym-class-signup.md) | SVG | reviewed; wide/label overlap | SVG | reviewed |
| [02 Café](../../solutions/system-design/02-campus-cafe-ordering.md) | SVG | reviewed; label overlap | SVG | reviewed |
| [03 Study rooms](../../solutions/system-design/03-student-study-room-booking.md) | SVG | reviewed | SVG | reviewed |
| [04 Shuttle](../../solutions/system-design/04-campus-shuttle-live-tracking.md) | SVG | reviewed | SVG | reviewed |
| [05 Library](../../solutions/system-design/05-library-book-loans-holds.md) | SVG | reviewed; wide/label overlap | SVG | reviewed |
| [06 Marketplace](../../solutions/system-design/06-student-marketplace.md) | SVG | reviewed | SVG | reviewed |
| [07 Enrollment](../../solutions/system-design/07-course-enrollment-waitlist.md) | SVG | reviewed | SVG | reviewed |
| [08 Theater](../../solutions/system-design/08-movie-theater-seat-booking.md) | SVG | reviewed; label overlap | SVG | reviewed; dense |
| [09 Notifications](../../solutions/system-design/09-notification-delivery-system.md) | SVG | reviewed; label overlap | SVG | reviewed |
| [10 Short links](../../solutions/system-design/10-url-shortener-click-analytics.md) | SVG | reviewed | SVG | reviewed |
| [11 Task board](../../solutions/system-design/11-collaborative-task-board.md) | SVG | reviewed; wide/label overlap | SVG | reviewed; dense |
| [12 File sharing](../../solutions/system-design/12-file-sharing-permissions.md) | SVG | reviewed; wide/label overlap | SVG | reviewed |
| [13 Parcel lockers](../../solutions/system-design/13-campus-parcel-locker-pickup.md) | SVG | reviewed; label overlap | SVG | reviewed |
| [14 Expenses](../../solutions/system-design/14-shared-expense-splitter.md) | SVG | reviewed; label overlap | SVG | reviewed; dense |
| [15 Polling](../../solutions/system-design/15-live-classroom-polling.md) | SVG | reviewed; label overlap | SVG | reviewed |

At 1280×900, all 30 SVGs were captured and reviewed for entities, relationship
endpoints, direction, truncation, and rendering failures. At 390×844, all 15
reference fixture pages again produced two SVGs, zero failed-source fallbacks,
and two source disclosures each. All 15 prompt fixture pages had one title,
one reference link, no Mermaid diagrams or scripts, and no document overflow.
All 30 fixture pages stayed within the mobile viewport.

## Concrete corrections

- **01:** `SIGNUPS ||--o| NOTIFICATION_OUTBOX` now agrees with the documented
  unique `notification_outbox.signup_id`. A signup has zero or one promotion
  event, and every outbox event belongs to one signup.
- **07:** Added `SECTION ||--o{ WAITLIST_ENTRY` for the existing
  `waitlist_entry.section_id` foreign key. The optional one-to-one enrollment
  relationship still agrees with unique `enrollment_id`.
- **13:** The pickup notification now flows from the campus notification
  provider to the student, agreeing with the written notification workflow.
- **14:** Allocations now connect to `EXPENSE_SHARES`, showing the documented
  composite foreign key `(expense_id, debtor_user_id)` to
  `(expense_id, user_id)`. Each allocation settles one particular share; a
  share can receive zero or more allocations. The adjacent prose makes that
  composite relationship explicit.

Other relationship checks included nullable route assignments/current vehicle
locations (04), historical versus active copy/hold relationships (05),
showing-seat allocations and optional tickets (08), composite delivery keys
(09), optional unique creation records (10), nullable task assignees (11),
private object keys versus relational entities (12), unique nullable locker
assignment (13), and same-poll option/vote keys (15). Diagrams summarize models;
transactional invariants and composite-key details also remain in their prose.

## Visual limitations for issue #17

No diagram is unverified for syntax or Chromium SVG rendering. These shared
renderer/layout issues remain visible and require the broader review in #17:

- Several labeled flowchart edges pass through their own label text. The
  clearest example is reference 09's **“claim delivery; load preferences”** edge
  from the worker to the database. Similar overlaps appear on the gym database
  edge, café payment edge, and polling request/result edges. The site uses
  `htmlLabels: false`; this audit has not changed shared Mermaid configuration.
- Wide left-to-right architectures shrink substantially inside the prose
  column. Reference 01 is an extreme example. Dense ERDs such as 08, 11, and 14
  also require zoom or their source disclosure to inspect details comfortably,
  particularly at 390px. No document overflow does not establish label
  readability at that size.
- The audit used local fixtures and Chromium, not GitHub's Markdown renderer,
  another browser engine, a screen reader, or the deployed Pages site. Full
  site navigation and reference presentation belong to the subsequent site
  and accessibility work. The preview uses the real Markdown renderer, CSS,
  and Mermaid module but does not duplicate the complete site template.

## Reproduce

Use Python 3.10+ and the pinned dependencies documented in
[the build guide](../../scripts/build-site.md). From the repository root:

```sh
shasum -a 256 -c system-design/audit/sources.sha256
/tmp/bloomberg-site-venv/bin/python system-design/audit/render-fixtures.py \
  --output /tmp/bloomberg-system-design-audit
python3 -m http.server 8014 --directory /tmp/bloomberg-system-design-audit
```

The generator requires an external output directory and writes 15
`prompt-<source-stem>.html` and 15 `solution-<source-stem>.html` pages, plus
copies of shared assets and the pinned renderer. Open each solution fixture in
a browser with network access to jsDelivr, wait for rendering, then inspect
both SVGs and their “Diagram source” disclosures. Check the corresponding
prompt fixtures separately. To reproduce the recorded sizes, use 1280×900 and
390×844 viewports. A successful reference has two `figure svg` elements, two
`details pre.mermaid` elements, and zero `pre[data-render-status]` elements.
Captured audit screenshots are disposable local evidence and are not required
for the site build.

Local completion checks: the source hash check, manifest freshness check,
site freshness check, renderer/build unit suite, and `git diff --check` all
passed. These are local results; no hosted CI result is asserted here.
