# NIGHT-01 — Duplicate Checkout

**Challenge ID:** NIGHT-01  
**Type:** Engineering ticket  
**Difficulty:** Hard  
**Target time:** 45–60 minutes

This is an original CIC practice exercise, not an official Bloomberg interview question.

## Ticket

A shopper says checkout took long enough that they submitted it again. Their order history and available stock no longer agree with the single purchase they intended to make.

An **idempotency key** identifies one logical request. A client reuses the key when retrying because it did not receive a timely response.

### Expected behavior

- Repeating a checkout request with the same shopper, key, and payload must not create another order or deduct stock again. A retry returns the original order result.
- The same key may be used independently by a different shopper.
- Reusing a key with a different payment outcome returns HTTP 409.
- Order creation, stock updates, cart changes, and the saved checkout result remain consistent if requests overlap or a response is delayed.

### Reproduction

Start with the seeded database. Add two `food-berry-bowl` items to `shopper-river`'s cart. Submit two overlapping `POST /checkout` requests with:

```http
X-User-Id: shopper-river
Idempotency-Key: concurrent-order
Content-Type: application/json
```

```json
{"payment_outcome":"success"}
```

The deterministic regression test sends this pair. It currently receives two HTTP 201 responses with different order IDs. The database contains two orders and stock falls from 12 to 8. The intended result is one order, one stock deduction (12 to 10), and a replay response for the second request.

### Acceptance criteria

- Repeated or overlapping requests for the same shopper and key produce one durable order and one stock deduction.
- A retry returns the original order ID and line snapshots.
- Key reuse across different shoppers and conflicting payload reuse retain the behaviors above.
- Declines, temporary payment errors, insufficient stock, cart clearing, and unrelated shopper or admin behavior remain correct.
- Add or improve focused regression coverage; do not weaken an assertion to make the challenge test pass.

### Constraints and non-regression

Keep the change within the existing FastAPI and SQLite request path. Do not add a payment provider, queue, external database, frontend feature, or broad checkout redesign. Preserve existing cart, order, inventory, and authorization behavior.

## Code version and setup

Starting version: [`night-01-v1`](https://github.com/ehuerta6/bloomberg-interview-practice/tree/night-01-v1), commit [`7206b378d13db763ec28a269d636c67f066d615e`](https://github.com/ehuerta6/bloomberg-interview-practice/commit/7206b378d13db763ec28a269d636c67f066d615e).

```sh
git clone https://github.com/ehuerta6/bloomberg-interview-practice.git
cd bloomberg-interview-practice
git switch --detach night-01-v1
cd marketplace
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m app.db reset
```

Run the focused reproduction with `python -m pytest tests/test_checkout_api.py::test_concurrent_checkouts_with_same_key_create_only_one_order -q`, then run the full suite with `python -m pytest -q`. The focused test is expected to fail on the starting version. See the [marketplace setup guide](../marketplace/README.md) for run and reset details.
