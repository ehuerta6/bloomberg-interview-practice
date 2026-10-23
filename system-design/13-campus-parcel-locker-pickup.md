# Problem 13 — Campus Parcel Locker Pickup

**Difficulty:** Easy

## Scenario

The campus mailroom receives student parcels throughout the day. Staff currently call students to collect them, which interrupts class and creates a queue. The school wants staff to place a package in a locker and send the intended student a one-time pickup code.

Design an application for one campus mailroom and one locker bank. Treat a locker as occupied until the parcel is collected through a valid pickup flow or staff removes it; an expired code by itself does not make a physically occupied locker available.

## Functional Requirements

- Staff can record a package with a tracking reference and intended student, then assign it to a free locker.
- A package has a lifecycle such as `received`, `stored`, `collected`, and `returned_to_mailroom`. Invalid state transitions must be rejected.
- When a package is stored, the student receives a pickup notification containing a one-time code. Store only a verifier/hash of the code, not the code itself.
- The student can submit the code at a locker kiosk. A valid, unexpired code for a stored package opens that package's locker and marks the package collected.
- A code can be used only once. A wrong, expired, revoked, or already-used code does not open a locker and should not reveal whether another student's package exists.
- Staff can cancel a code and issue a replacement while the parcel remains stored. Staff can return an uncollected package to the mailroom and free the locker after confirming removal.
- The system records who performed staff actions and when. If notification delivery fails, staff can see that a notification is pending or failed and can retry it without creating a second package.

## Constraints & Assumptions

- Staff and students are authenticated; a kiosk is a trusted client that communicates with the application. The locker controller accepts only a one-locker open command from the backend.
- Assume a small set of lockers and a relational database. No integration with carrier tracking is required.
- Code expiration is configurable. Expiring or cancelling a code does not change package or locker occupancy.
- Clarify how code guessing is limited and what operational fallback exists if the kiosk or locker controller is offline.

## Your Task

Design the staff intake and student pickup flows, including data entities and state transitions. Show how a locker is assigned without being assigned to two packages, how a code is validated and consumed once, and how the application coordinates the database with the physical locker controller. Include an operational approach for a failed notification or unlock command.

## Example to Work Through

A package remains inside a locker after its pickup code expires. The student submits the old code, then staff issue a replacement code. Describe the package and locker state after each action and what the kiosk should report.

## Interviewer Follow-Ups

- Two staff members store parcels at the same time and only one locker is free. How is double assignment prevented?
- The controller opens the locker, but the application times out before recording pickup. How would you reconcile physical and recorded state?
- The mailroom adds a second building with lockers. What should change in identifiers and staff workflow?

## Reference Solution

[View the reference solution](../solutions/system-design/13-campus-parcel-locker-pickup.md)
