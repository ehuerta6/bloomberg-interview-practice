# Ticket #04 — Library Book Checkout

**Difficulty:** Easy

## Context

You maintain checkout at a small library. A loan records one reader borrowing
one copy. An active loan has not been returned. Readers can also reserve a book;
the reservation queue gives its first reader priority over a walk-in checkout.

## Practice report

Add book `b1` with one copy. Check it out to `reader-a` as loan `l1`, then call
`return_book("l1")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Return result | `True` | `True` |
| Available copies after return | 0 | 1 |

To extend the case, queue `reader-b` and `reader-c` while the copy is borrowed.
After the return, `reader-b` should be able to check out before either a walk-in
or `reader-c`.

## Acceptance Criteria

- Available copies equal total copies minus active loans. Active loans cannot
  exceed the number of copies, and a successful checkout records book and reader.
- A successful return releases exactly one copy. Unknown and repeated returns
  fail without changing other loans or the available-copy count.
- Checkout honors reservation order and consumes the first reservation only
  when that reader checks out. A blocked checkout leaves queue order unchanged.
- Unknown books cannot be reserved or checked out. Missing reader or loan IDs
  and reused loan IDs cannot create or replace a loan.

## Out of Scope

Keep the supplied copy counts, in-memory storage, and reservation queue. Due
dates, fines, notifications, and automatic checkout on return are outside this ticket.

## Investigation

Reproduce the one-copy case and trace checkout, return, and reservation handling.
Add assertions for the loan's stored state, available copies, and the next
reader's checkout. Show that a repeated return cannot manufacture another copy.

## Starter Code

[View starter code](../../round-2/04-library-book-checkout/)

## Reference Solution

[View solution](../../solutions/round-2/04-library-book-checkout/)
