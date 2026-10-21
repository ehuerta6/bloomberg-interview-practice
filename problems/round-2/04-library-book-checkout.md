# Ticket #04 — Library Book Checkout

**Difficulty:** Easy

## Problem

### Reported symptom

A book stays unavailable after a reader returns it, and readers with reservations do not get a reliable turn when a copy becomes free.

### Scenario

A small branch has a limited number of copies. Readers can borrow a copy, return it, or join a reservation queue while all copies are on loan.

## Acceptance Criteria
- The number of active loans cannot exceed the number of copies.
- A successful loan records the reader and book.
- A returned loan releases exactly one copy and cannot be returned twice.
- The next reader in line has priority over a walk-in checkout.
- A repeated or unknown loan identifier cannot overwrite an existing loan.

## State Invariants
- Available copies equal total copies minus active loans.
- A return changes one active loan to returned exactly once.
- A reservation queue retains its order until a reader checks out.

## Investigation

Follow the copy count across checkout and return. Inspect how active loans and the reservation queue are represented, and reproduce the reported sequence with one copy and two waiting readers.

## Starter Code

[View starter code](../../round-2/04-library-book-checkout/)

## Reference Solution

[View solution](../../solutions/round-2/04-library-book-checkout/)
