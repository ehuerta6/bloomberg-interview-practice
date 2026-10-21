# Problem 01 — Gym Class Sign-Up

**Difficulty:** Easy

## Scenario

A neighborhood gym wants members to browse its weekly group-class schedule and reserve a place. Classes such as yoga or cycling are offered as scheduled sessions with a fixed capacity. Members currently call the front desk to ask whether a class has room. The gym wants a small application that makes sign-up and cancellation predictable for members and staff.

Adapted from Noel's CIC workshop. This is an educational exercise, not an official Bloomberg interview question.

## Functional Requirements

- Members can browse the weekly schedule, including each session's class type, start time, and capacity/availability.
- A member can register for a session while it has a place.
- A session cannot have more confirmed signups than its capacity.
- Each signup has one state: `confirmed`, `waitlisted`, or `cancelled`.
- When a session is full, later registration requests join a first-come, first-served waitlist. Existing waitlisted members always have priority over new registration requests when a place opens.
- A member can cancel their registration at any time. Cancelling a confirmed signup frees a place and promotes the earliest waitlisted signup, if one exists.
- The promoted member receives a notification. The member's signup state must reflect that promotion.
- A member must not hold two active signups for the same session. Cancelled history may be retained.

## Constraints & Assumptions

- Start with one gym and a modest schedule; no scale target is supplied.
- Class types describe offerings; sessions are dated occurrences of a class type and have a capacity.
- Treat the database as the source of truth. A registration or cancellation should report a definite result.
- “First come” means the order in which accepted signup requests are committed by the system. Clarify the exact tie-breaker if two requests arrive at effectively the same time.
- Do not assume a promoted member must reconfirm; the stated requirement is to promote them and notify them.
- Clarify the schedule time zone and the ordering rule for requests accepted at effectively the same time.

## Your Task

Design the smallest correct system for the member and gym workflows. Explain the principal records and their relationships, how capacity and FIFO waitlist order are preserved when requests overlap, and how the system handles a cancellation if notification delivery fails. Walk through one registration and one cancellation from the member's action to the stored result.

## Interviewer Follow-Ups

- Two members try to claim the final place at the same moment. What makes the outcome safe?
- A cancellation succeeds but the notification provider is unavailable. What should the member and staff see, and how can delivery recover?
- The gym wants to prevent a member from joining several waitlists for the same session. Which data rule would you enforce?

## Reference Solution

[View the reference solution](../solutions/system-design/01-gym-class-signup.md)
