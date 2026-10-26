# Local admin API

The seeded local selector `admin-stone` can inspect orders and adjust stock.
Send it in the `X-User-Id` header. This is a local role selector, not
authentication. Missing or unknown selectors receive HTTP 401; a shopper
selector receives HTTP 403.

## Inspect orders

`GET /admin/orders` returns every order in ascending order ID, with its current
status and immutable purchase line snapshots (product name, category, price,
quantity, and line total). The route is read only. Admins cannot change order
status, edit an order, or cancel it.

## Adjust stock

`POST /admin/products/{product_id}/stock-adjustments` accepts a JSON signed
integer delta:

```json
{"delta": 3}
```

The delta must be a nonzero integer in the SQLite stock range. A positive delta
adds stock and a negative delta removes stock. The API returns the product ID,
applied delta, and resulting stock. Invalid values, including a quantity that
would make stock negative or exceed the SQLite integer range, receive HTTP 422
for invalid input or HTTP 409 for an invalid resulting quantity. An unknown
product receives HTTP 404. Each adjustment checks and writes stock within one
SQLite immediate transaction.

Product creation and catalog details remain available through the product
catalog admin routes documented in the project README.
