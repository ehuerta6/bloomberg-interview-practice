# Problem 03 — Student Study Room Booking

**Difficulty:** Medium

## Scenario

Students at a university need to find quiet rooms for group study. The library has rooms with different seating capacities and facilities such as whiteboards or displays. Today students check availability at the front desk and can arrive to find that another group was given the same room. The university wants a booking tool for students and library staff.

## Functional Requirements

- Students can search rooms for a requested time interval and filter by minimum capacity and required facilities.
- Students can reserve an available room, view their future reservations, and cancel a reservation they own.
- A room must never have two active reservations whose time intervals overlap.
- A reservation has a start and end time, an owner, and a state such as `CONFIRMED` or `CANCELLED`.
- Search results are advisory: the reservation operation must recheck availability before confirming.
- Staff can mark a room unavailable for a maintenance interval; such intervals must block student reservations.
- A cancelled reservation no longer blocks availability, while its history remains available for audit/support.

## Constraints & Assumptions

- Start with one campus and a relational database as the persistent store.
- Use campus-local time in the interface and store timestamps consistently; clarify daylight-saving handling.
- Reservations use explicit start and end times. A room is available only if no active reservation overlaps the requested interval; adjacent bookings where one ends exactly as another starts are allowed.
- Assume students authenticate through the university, but identity-provider implementation is out of scope.
- Specify reasonable booking limits (for example, maximum duration and how far ahead) during clarification rather than inventing them as fixed requirements.
- Room facility changes and maintenance are staff-controlled.

## Your Task

Design the search and booking flow, the data model for rooms, facilities, student reservations, and staff blocks, and a safe way to confirm a booking when two students request the same room at once. Explain why search alone cannot guarantee a successful reservation. Include ownership checks for cancellation and discuss how availability is presented if the data changes between search and confirmation.

## Example to Work Through

A student searches for a room from 2:00 to 3:00 PM, while another reservation for that room runs from 3:00 to 4:00 PM. Explain whether the intervals conflict, then describe the response if a different student confirms the 2:00 to 3:00 PM booking after the first student's search results were shown.

## Interviewer Follow-Ups

- Two requests overlap by only five minutes. How does the system determine whether they conflict?
- A staff maintenance block is entered after a student reservation already exists. What policy and workflow should apply?
- The university asks for recurring weekly reservations. What changes to validation and storage would you consider?

## Reference Solution

[View the reference solution](../solutions/system-design/03-student-study-room-booking.md)
