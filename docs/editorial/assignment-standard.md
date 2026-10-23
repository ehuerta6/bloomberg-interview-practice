# Assignment writing standard

This guide sets a shared writing standard for the 65 CIC practice exercises.
Markdown remains the maintained source; the site generator renders it into
HTML. The two Bloomberg workshop examples below are teaching examples. They do
not establish one exact format for real Bloomberg interviews, and these CIC
exercises are not official Bloomberg questions.

## What the workshops teach

The **Potluck** product spec groups business rules around a seed pot, entry fee,
five-digit access codes (`00000`–`99999`), draw time, payout tiers for zero
through five matches, and how winners split, take priority, or roll winnings
over. Its useful writing lesson is to turn each statement into a condition a
reader can check. Boundary examples such as leading zeroes and inclusive
endpoints make those conditions concrete.

The **Blike Moomberg's Calendar** workshop pairs a candidate README with a named
engineering ticket. The ticket leads with the reported behavior, acceptance
criteria, scope, and the state or invariant that matters. For example, the
same requester and idempotency key must return the same request ID across
overlapping calls, while another requester can reuse that key. The workshop's
work sequence is **Read ticket → Trace code → Name invariant → Patch small →
Prove it**. Students work on one bounded goal and add deterministic regression
tests; the exercise is not a race to complete many tickets.

The Bloomberg presentation describes three skills for this practice: using AI
to navigate code, generate code, and debug; verifying results and exercising
technical judgment; and communicating decisions. The student owns and explains
the final code.

Noel's CIC System Design workshop uses a separate whiteboard sequence:
**Clarify → Interactions → Data → Design → Improve**. The Gym Class Sign-Up and
Campus Café cases are the two original CIC workshop cases. Their diagrams are
editable reference adaptations; preserve their attribution and do not present
them as exact reproductions.

## Shared writing rules

- Write student-facing assignments in English. Name the student's role and
  task, then give a credible scenario before technical detail.
- Define unfamiliar domain terms when they first matter. Explain terms such as
  *SKU*, *all-or-nothing*, *backorder*, and *idempotency* in the context of the
  exercise instead of assuming the reader knows them.
- Separate supplied facts, required behavior, optional assumptions, and
  follow-up questions. Do not turn an optional design choice into a hidden
  requirement.
- Use small groups of functional rules and testable acceptance criteria.
  Prefer an observable result over “handle edge cases” or “make it robust.”
- Include a representative example when the contract supports one. State the
  relevant input and initial state, then identify the expected result. For a
  reported bug, distinguish the current observed result from the expected
  contract. Do not invent production logs or imply an invented practice
  scenario came from a real incident.
- Make examples useful for testing boundaries, state changes, retries, and
  failure behavior. Check their values against the starter, its tests, and the
  reference contract before adding them.
- Give the student a focused investigation or design task. Keep the culprit
  line, root cause, fixed algorithm, and reference solution out of the
  assignment. A contract example may state what should happen; it must not tell
  the student how to implement it.
- Preserve intended difficulty, existing behavior contracts, deliberate
  starter defects, tests, and reference solutions. If those sources disagree,
  record the contradiction for review; do not silently change code or tests to
  make the prose fit.
- Keep Markdown links and their destinations unchanged unless a verified link
  defect is found. Do not copy reference material into the assignment.
- Apply the `unslop` skill from `ehuerta6/ai-setup`: remove empty technical
  language and unsupported claims, but keep useful detail. Clear writing is
  not a requirement to make every assignment shorter.

## Use the right shape for each category

### Round 1: PR Review

Write a short PR description with a product goal, the behavior contract, useful
examples, and a review task. State the valid inputs and outputs, important
boundaries, and relevant state where applicable. Ask the student to compare the
proposed code and tests with the contract, add meaningful regression coverage,
and explain the evidence. Do not turn a contract example into a disclosure of
the starter's defect.

### Round 2: Engineering Ticket

Start with business context and the student's role. Describe the reported
behavior with a reproducible input or action, the initial state, and observed
versus expected results when those are supported by the repository. State
acceptance criteria, important invariants, and what is out of scope. Define
domain terms and ask the student to trace the relevant behavior and prove the
contract with focused tests. Do not name the cause or propose the patch.

### System Design

Use a concrete scenario, the user's journey or interactions, functional
requirements, assumptions, and constraints. Ask the student to clarify
ambiguities, model the data, describe a design, and discuss how it should
change under follow-ups. Keep architecture choices open where the prompt allows
them. Do not force a PR-review or debugging-ticket structure onto a whiteboard
exercise. Keep diagrams and reference designs out of the prompt.

## Worked examples for writers

These are editorial examples grounded in the current repository. They show the
level of specificity to aim for; they are not text to copy into student
assignments without checking the complete exercise.

### Round 1 example: PR #01, Code Validator

The [assignment](../../problems/round-1/01-code-validator.md) asks for a
six-character string of ASCII digits and says leading zeroes count. The starter
and reference expose the same function,
`is_valid_access_code(code)`, and the tests cover ordinary digits, leading
zeroes, non-ASCII numerals, and invalid values.

An appropriate contract example is:

| Input | Expected contract result |
| --- | --- |
| `"001234"` | `True` (valid) |
| `"12a456"` | `False` (invalid) |

This states the required behavior without reporting what the current starter
returns or pointing to a cause. A review task can then ask the student to check
the implementation and tests against that contract.

Sources checked: [starter](../../round-1/01-code-validator/validator.py),
[reference implementation](../../solutions/round-1/01-code-validator/validator.py),
and the tests in each `validator.py` file.

### Round 2 example: Ticket #06, Warehouse Shipment Processing

The [ticket](../../problems/round-2/06-warehouse-shipment-processing.md)
defines all-or-nothing fulfillment, existing reservations, rollback after a
failed attempt, partial fulfillment, retries, and invalid quantities. The
starter, its tests, and the reference all use `fulfill(order_id, lines,
allow_partial=False)` and a repository that tracks on-hand and reserved stock.

A useful failure report is:

| Point in the report | `sku-a` | `sku-b` |
| --- | ---: | ---: |
| On hand before request | 4 | 2 |
| Reserved before request | 0 | 0 |
| Requested, all-or-nothing | 3 | 3 |
| Current starter after it reports `backordered` | 4 on hand; 3 reserved | 2 on hand; 0 reserved |
| Expected after failed attempt | 4 on hand; 0 reserved | 2 on hand; 0 reserved |

This gives the student an input, starting state, observed result, and expected
invariant without naming a source line or suggesting an implementation. The
separate partial-fulfillment criterion remains in the ticket; it should not be
confused with the all-or-nothing example.

Sources checked: [starter service](../../round-2/06-warehouse-shipment-processing/shipment_service.py),
[starter tests](../../round-2/06-warehouse-shipment-processing/test_shipments.py),
[reference service](../../solutions/round-2/06-warehouse-shipment-processing/shipment_service.py),
and [reference tests](../../solutions/round-2/06-warehouse-shipment-processing/test_shipments.py).

### System Design example: Noel's Gym Class Sign-Up

Keep this in the design-prompt shape: describe the class and enrollment
scenario, ask what must be clarified, identify member and staff interactions,
and let the student choose a data model and design. Follow-ups can ask how the
design responds to contention or notification failures. The source prompt
remains the authority for its requirements; the reference diagrams stay in the
solution. Preserve the Noel workshop attribution.

See [the prompt](../../system-design/01-gym-class-signup.md),
[its reference](../../solutions/system-design/01-gym-class-signup.md), and the
[category provenance note](../../system-design/README.md).

## Category-owner verification checklist

For each problem, record the source paths you inspected and verify:

1. The role, scenario, task, examples, and domain terms are clear to the intended
   student.
2. Every example and acceptance criterion matches the current starter API,
   tests, and reference contract. Check both sides of a boundary and the state
   before and after any stateful operation.
3. The assignment preserves its difficulty, requirements, deliberate starter
   behavior, and reference solution. It does not disclose a culprit, root cause,
   patch, algorithm, or design diagram.
4. Category format fits the exercise: PR contract for Round 1, reported ticket
   for Round 2, and the Clarify → Interactions → Data → Design → Improve path
   for System Design.
5. Starter, source, and reference links still resolve to the intended files or
   directories. No assignment link or Markdown source is replaced by generated
   HTML as the maintained source.

When the text already meets the standard, record that review instead of
rewriting it for novelty. When the source, tests, and reference do not agree,
report the exact paths and behavior to the issue owner; preserve the existing
code, test behavior, and difficulty until the contract is resolved.
