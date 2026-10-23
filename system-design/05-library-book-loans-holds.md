# Problem 05 — Library Book Loans & Holds

**Difficulty:** Medium

## Scenario

A campus library wants students to search its catalog, borrow available books, return loans, and request a title when every copy is checked out. The catalog includes titles with multiple physical copies. Staff need to record checkouts and returns accurately, while students need a clear view of whether a title is available or whether they are waiting for it.

## Functional Requirements

- Students can search titles and see the number of available copies.
- Staff can check out an available physical copy to a student and record a due date.
- A physical copy cannot be loaned to two students at once; returning it closes its active loan.
- If all copies of a title are on loan or reserved for another student, a student may join a FIFO hold queue for that title.
- On return, if a hold is waiting, the next eligible student is assigned the returned copy and notified that it is ready for pickup.
- A ready hold expires after a stated pickup period; when it expires, the copy moves to the next waiting hold or becomes available.
- Students can view and cancel their own waiting or ready holds. Staff can correct a checkout/return with an auditable action.

## Constraints & Assumptions

- Start with one library branch. Inter-branch transfers and fines are out of scope.
- A catalog title (author/ISBN/edition metadata) is distinct from each individually tracked physical copy.
- Assume one active loan per physical copy and one active hold per student per title.
- Clarify loan duration, renewals, and whether a student with an overdue loan can borrow another item; these policies are not supplied.
- “FIFO” is based on the committed time a hold is placed, with a stable tie-breaker for simultaneous requests.
- Notification delivery may be delayed; stored hold/copy state remains authoritative.

## Your Task

Design the catalog, copy, loan, and hold records and the checkout/return interactions. Trace a return when multiple students are waiting, including the pickup deadline and what happens if the first hold expires. Explain how concurrent checkout requests and duplicate return actions preserve copy and loan consistency.

## Example to Work Through

A title has two copies, both on loan, and two students are waiting for it. One copy is returned and assigned for pickup, but the first student's pickup period expires. Describe the state of that copy and the two holds at each step, including what the next student can see.

## Interviewer Follow-Ups

- Two staff members attempt to check out the same final available copy at once. How do you prevent a double loan?
- A student cancels after their hold has been assigned a copy but before pickup. What state transition should occur?
- The library adds a second branch. Which availability and hold assumptions change first?

## Reference Solution

[View the reference solution](../solutions/system-design/05-library-book-loans-holds.md)
