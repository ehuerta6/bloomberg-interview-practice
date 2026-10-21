# Problem 07 — Course Enrollment & Waitlist

**Difficulty:** Medium

## Scenario

A university department needs a service for students to find course sections and request enrollment. A section has a fixed number of seats, a meeting schedule, and a course. Some courses require prerequisite courses. When a section is full, eligible students may join its waitlist. Students can drop an enrollment, and the next eligible waitlisted student should be offered the seat.

## Functional Requirements

- Students can view course sections, meeting times, prerequisites, remaining seats, and their own enrollment state.
- A student may enroll only if they have completed all required prerequisites, have no overlapping active section, and the section has capacity.
- If a section is full, an eligible student may join its waitlist. Waitlist order is first-come, first-served.
- A student may drop an enrolled section or leave a waitlist.
- When an enrolled student drops, the earliest eligible waitlisted student is enrolled. If that student is no longer eligible (for example, they added a conflicting section), skip them and continue.
- A student cannot have two active enrollment or waitlist records for the same section.

## Constraints & Assumptions

- The first version handles one term. Student identity and authoritative completed-course history are already available.
- Enrollment changes are online and may occur concurrently near a deadline. A database is the source of truth for seats and waitlist order.
- Clarify whether a promoted student is enrolled immediately or must accept an offer. For this exercise, promotion enrolls the student immediately if still eligible.
- Course equivalencies, instructor overrides, cross-listed sections, tuition, and registration holds are out of scope unless introduced in a follow-up.

## Your Task

Design the enrollment workflow, including course/section relationships, prerequisite representation, schedule conflict checks, seat allocation, and waitlist promotion. Identify the invariant that prevents over-enrollment and explain how you preserve FIFO order while skipping ineligible waitlisted students.

## Interviewer Follow-Ups

- Two students request the final seat at the same time. How does the system decide who gets it?
- A prerequisite completion arrives late from the registrar. How can a student retry without creating duplicate enrollment?
- The department wants waitlist offers that expire after 24 hours. What state and transition changes?

## Reference Solution

[View the reference solution](../solutions/system-design/07-course-enrollment-waitlist.md)
