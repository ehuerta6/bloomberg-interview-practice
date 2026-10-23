# Problem 10 — URL Shortener & Click Analytics

**Difficulty:** Medium

## Scenario

A campus organization wants to create compact links for event flyers and see basic usage counts. A user submits a destination URL and receives a short URL. Visitors who open the short URL should be redirected to its destination. Owners can optionally set an expiration time and view aggregate click counts by day. The service does not need advertising attribution or identity-level visitor tracking.

## Functional Requirements

- An authenticated owner can create a short link for a valid HTTP or HTTPS destination and optionally choose an unused alias.
- If the service generates the code, it must be unique. If a chosen alias is already in use, creation returns a clear conflict and does not overwrite the existing link.
- Visiting an active code redirects to its destination. Unknown, disabled, or expired codes return a not-found or unavailable response without redirecting.
- An owner can disable a link and view aggregate click counts for a date range.
- Redirects record one click event or equivalent count update with a timestamp. Analytics are grouped by day in a documented timezone (use UTC).
- Repeating a creation request with the same client idempotency key returns the original result rather than creating a second link.

## Constraints & Assumptions

- Start with a relational database and a single service. Do not assume a specific request volume or introduce a cache without a stated need.
- Generated codes use a URL-safe alphabet. Clarify code length and collision strategy; choose a sufficiently long random code and enforce uniqueness in storage, retrying on collision.
- A redirect should not wait for expensive analytics aggregation. For the initial design, a durable click row may be written during redirect; discuss batching only as a later option.
- Link previews, custom domains, malware scanning, and per-visitor analytics are out of scope.

## Your Task

Design creation, redirect, expiration, disablement, and reporting. Explain the uniqueness guarantee, how a redirect checks time-sensitive state, how click events relate to links, and how analytics remain correct across day boundaries. Walk through a visitor redirect and identify the main consistency trade-off.

## Example to Work Through

An owner requests an alias that another link already uses. Later, a visitor follows that existing link just before midnight UTC. Describe the creation response and which UTC day should include the click.

## Interviewer Follow-Ups

- The database is unavailable for analytics writes but link lookup still works. Should redirects continue, and what data might be lost?
- A link receives far more visits than the rest. Which measurement would justify introducing a cache or asynchronous aggregation?
- Owners need to change a destination but preserve the existing short code. What audit and safety rules should be added?

## Reference Solution

[View the reference solution](../solutions/system-design/10-url-shortener-click-analytics.md)
