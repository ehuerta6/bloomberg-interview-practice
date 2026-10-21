# Problem 04 — Campus Shuttle Live Tracking

**Difficulty:** Medium

## Scenario

Students use several campus shuttle routes and want to see where each shuttle is and approximately when it will reach a stop. Drivers already carry a campus device capable of reporting GPS coordinates. The transit office maintains routes and ordered stops. A location that has not updated recently can be misleading, especially when students are deciding whether to wait or walk.

## Functional Requirements

- Students can browse active routes, their ordered stops, and the vehicles assigned to them.
- The driver device periodically submits a vehicle identifier, latitude/longitude, and observation time.
- Students can request the latest position for a route or vehicle and see when that position was observed.
- The system shows an estimated arrival time for upcoming stops, based on the latest location and route information.
- The client must be able to distinguish a current estimate from stale or unavailable location data.
- Transit staff can update route-stop ordering and vehicle-to-route assignments.
- A late, duplicated, or out-of-order location update must not move a vehicle's displayed position backward in time.

## Constraints & Assumptions

- Start with one campus and a small fleet; no high-availability or volume targets are specified.
- Assume driver devices can send updates every 10–30 seconds when connected; this is a starting assumption to confirm.
- GPS and ETA are approximate. The interface should show observation time and avoid implying precision the system cannot provide.
- For an initial design, use route order and configured typical segment travel times to estimate arrivals. Live traffic integration is out of scope.
- Define a stale threshold with the interviewer (for example, 60 seconds) and expose stale data as stale rather than silently presenting it as live.
- Historical trip replay is not required. Clarify whether a short diagnostic history is useful before retaining every coordinate indefinitely.

## Your Task

Design the driver update and student lookup interactions. Model routes, ordered stops, vehicles, and current location data. Walk through how a new location becomes a displayed position and ETA, including what happens when a device reconnects and submits an older observation. Explain how you would keep the design simple while making freshness visible.

## Interviewer Follow-Ups

- A shuttle loses connectivity for several minutes, then uploads a backlog of GPS points. Which points should affect the current view?
- Students refresh a route page frequently during class changes. What is the simplest update strategy, and what requirement would justify changing it?
- A route changes its stop order during the day. How do you avoid calculating an ETA from mismatched route data?

## Reference Solution

[View the reference solution](../solutions/system-design/04-campus-shuttle-live-tracking.md)
