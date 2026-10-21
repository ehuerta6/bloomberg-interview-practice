# Problem 09 — Notification Delivery System

**Difficulty:** Medium

## Scenario

Several application features need to notify users about events such as a password reset, a booking change, or a new message. Users can choose whether to receive optional updates by email and in-app notification. Security-critical messages, such as password resets, must still be sent by email. Delivery providers can fail temporarily, and an event may be submitted more than once.

## Functional Requirements

- An internal application component can submit a notification event with a stable event identifier, recipient, type, and the data needed to render a message.
- The system creates an in-app notification for eligible event types and sends email through an external provider when policy and preferences allow.
- User preferences can disable optional email and in-app categories. Required security notifications cannot be disabled.
- A user can list and mark their in-app notifications read.
- Each channel tracks delivery state and attempt count. Temporary provider failures can be retried; permanent failures stop retrying and remain observable.
- Repeated submission of the same event does not create duplicate in-app notifications or duplicate logical email deliveries.

## Constraints & Assumptions

- Begin with a single application, relational database, and email provider. A database-backed pending-work table is sufficient; a broker is not assumed.
- Clarify retry policy; use a bounded schedule such as three attempts with increasing delay for transient failures.
- “Sent” means the provider accepted the email, not that a human read it. Email delivery can be delayed or bounced after acceptance.
- Push/SMS delivery, template authoring, localization, and bulk campaigns are out of scope.

## Your Task

Design event intake, preference evaluation, in-app persistence, channel-specific delivery tracking, and retry handling. Show how event idempotency works across retries and explain what state is written before and after calling the provider. Walk through a transient email failure followed by a retry.

## Interviewer Follow-Ups

- The provider accepts an email but the application times out before recording success. What happens on retry?
- A user disables a category while a notification is waiting to send. Which preference value should the worker apply?
- An event contains sensitive data. How do you avoid exposing it through logs or notification history?

## Reference Solution

[View the reference solution](../solutions/system-design/09-notification-delivery-system.md)
