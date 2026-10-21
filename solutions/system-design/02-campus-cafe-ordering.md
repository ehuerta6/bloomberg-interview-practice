# Reference Solution — Campus Café Mobile Ordering

> These diagrams are reconstructed reference designs based only on the requirements supplied for this exercise; no local workshop slides or guide were available. This is one defensible design, not the only acceptable interview answer.

## 1. Clarify

Confirm whether payment is authorized before the café accepts an order, what staff statuses are visible to students, how long checkout can remain pending, and how payment is reversed when a pre-preparation cancellation is accepted. The brief specifies one café, sellable stock counts, staff status updates, forward-only order progress, and cancellation only before preparation. It does not prescribe an update mechanism, so the initial design can use polling.

Keep payment credentials with the provider. The core invariants are: an order item uses the price captured at purchase time; available stock never drops below zero; a provider retry does not create duplicate charges; and order progress cannot move backward or proceed after cancellation.

## 2. Interactions

Representative operations are `GET /menu`, `POST /orders`, `GET /orders/{id}`, and staff-only `GET /staff/orders` / `PATCH /staff/orders/{id}/status`. The order service is the shared application boundary for the student app and staff screen. The payment provider is external.

For checkout, the service validates item IDs and quantities, then transactionally creates a pending order and order-item snapshots while reserving/decrementing the requested stock. It calls the provider using the order ID as an idempotency key. On confirmed payment, it records payment success and moves the order to `PLACED`. On a definite failure, it marks payment failed and restores stock once. A timeout remains pending until a provider lookup or callback resolves it; blindly charging again is unsafe.

Staff transitions are checked by the order service against an allowed transition table. A cancellation request is accepted only while preparation has not begun; the service releases stock and requests a payment void/refund as applicable. The café must decide how to show a reversal that is still pending.

## 3. Data Model

- `students(student_id PK, name, contact)` identifies students.
- `menu_items(menu_item_id PK, name, current_price, stock_count, is_available)` stores the current café menu and sellable portion count.
- `orders(order_id PK, student_id FK, status, payment_status, total_amount, created_at, payment_reference)` stores the order workflow. Example order states are `PENDING_PAYMENT`, `PLACED`, `PREPARING`, `READY`, `COMPLETED`, and `CANCELLED`; payment state is tracked separately as pending/succeeded/failed/reversal-pending/reversed.
- `order_items(order_item_id PK, order_id FK, menu_item_id FK, quantity, item_name_snapshot, unit_price_snapshot)` records what the student ordered at the charged price.

The order item references a menu item for traceability but stores a snapshot so later menu edits do not rewrite history. Validate positive quantities and nonnegative prices. Stock decrement must be conditional/transactional and cancellation or payment failure must restore it at most once. Provider idempotency uses the stable order ID; provider reference is stored after a result is known.

## 4. Architecture Diagram

```mermaid
flowchart LR
    Student[Student] --> StudentApp[Student App]
    StudentApp -->|menu, checkout, status| OrderService[Order Service]
    Staff[Cafe Staff] --> StaffScreen[Staff Screen]
    StaffScreen -->|view and advance orders| OrderService
    OrderService -->|menu, stock, orders, order items| DB[(Relational Database)]
    OrderService -->|charge or reverse using order idempotency key| Payment[Payment Provider]
    Payment -->|result or callback| OrderService
```

One service handles both student and staff requests so both observe the same order state and transition rules. The payment provider is shown separately because it owns payment processing.

## 5. Database ERD

```mermaid
erDiagram
    STUDENTS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    MENU_ITEMS ||--o{ ORDER_ITEMS : referenced_by

    STUDENTS {
        int student_id PK
        string name
        string contact
    }
    MENU_ITEMS {
        int menu_item_id PK
        string name
        decimal current_price
        int stock_count
        boolean is_available
    }
    ORDERS {
        int order_id PK
        int student_id FK
        string status
        string payment_status
        decimal total_amount
        string payment_reference
        datetime created_at
    }
    ORDER_ITEMS {
        int order_item_id PK
        int order_id FK
        int menu_item_id FK
        int quantity
        string item_name_snapshot
        decimal unit_price_snapshot
    }
```

The one-or-more relationship from order to order item applies to a submitted order; a short-lived draft checkout may be represented before submission if the implementation needs it. The menu item reference may become nullable or point to retained catalog history if items can be deleted; deletion policy should preserve order history.

## 6. Walkthrough

A student selects two sandwiches. The order service checks that the IDs are valid, the items are sellable, and stock is sufficient. In one database transaction it locks or conditionally updates the stock rows, stores an order with `PENDING_PAYMENT`, stores item names and unit-price snapshots, calculates the total using decimal currency arithmetic, and commits the reservation. It then asks the provider to charge with `order_id` as the idempotency key.

When payment success arrives, the service records the provider reference and changes the order to `PLACED`. The staff screen reads that state. A staff update to `PREPARING` is accepted only from `PLACED`; a later `READY` update is accepted only from `PREPARING`. A student polling the status endpoint sees the committed state. If payment fails, the service records that outcome and releases the reserved stock exactly once.

## 7. Design Decisions

The four relational entities preserve the workshop's supplied data model: students, menu items, orders, and order items. Price snapshots are essential because current menu prices change. The payment provider remains an external dependency and no card number is stored. A single order service supports both the mobile and staff workflows; it can enforce authorization for staff-only operations.

Keeping order state and payment state separate avoids conflating a kitchen transition with a provider result. A staff update can be validated against a small transition table. For modest one-café use, a relational database and polling are easier to reason about than a message bus or real-time push system.

## 8. Failure Cases & Trade-offs

- **Concurrent last-item checkout:** A read-then-write stock check is racy. Use row locking or an atomic conditional decrement and abort the entire checkout if any item cannot be reserved.
- **Provider timeout:** The charge may have succeeded even if the service did not receive the response. Keep the order pending and reconcile by idempotency key/provider reference; do not issue a new charge with a new key.
- **Failure after stock reservation:** Persist enough state to release a reservation exactly once when payment definitively fails or expires. A recovery process may reconcile stuck pending orders.
- **Cancellation after payment:** The café's stated cancellation boundary is before preparation. A void/refund can fail or remain pending, so show payment reversal status separately and define the customer-support policy.
- **Invalid staff transition:** Reject it without changing order state; retain authorization checks so students cannot call staff operations.
- **Polling load:** Polling is appropriate absent a freshness target. Add push updates only if observed delay or traffic makes it necessary.

## 9. Improvements

If failures between database commit and provider call need automatic recovery, add a durable payment-request/outbox record and a worker that retries with the same provider idempotency key. Add an audit trail for staff transitions if the café needs accountability. Add a second location only when required, then scope menu and inventory by location. None of these additions is needed to make the first single-café design correct.
