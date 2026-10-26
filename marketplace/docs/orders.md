# Shopper orders

Order endpoints use the selected local shopper from the `X-User-Id` header. A missing or unknown user receives `401`; an admin receives `403`.

## Read orders

- `GET /orders` returns the selected shopper's orders, newest first. Each order includes its immutable line snapshots.
- `GET /orders/{order_id}` returns one order and its line snapshots. Orders belonging to another shopper and unknown order IDs both return `404`.

An order contains its integer `id`, `status`, `created_at`, `total_cents`, and `items`. Each item contains `product_id`, snapshot `name` and `category`, `price_cents`, `quantity`, and `line_total_cents`.

## Cancel an order

`POST /orders/{order_id}/cancel` cancels only an order whose status is `placed`. The successful response is the order snapshot with status `cancelled`; the purchased quantities are restored to product stock in the same SQLite transaction. A missing or other shopper's order returns `404`. A second cancellation, or cancellation of any order outside `placed`, returns `409` and does not change stock.

```sh
curl -H 'X-User-Id: shopper-river' http://127.0.0.1:8000/orders
curl -X POST -H 'X-User-Id: shopper-river' http://127.0.0.1:8000/orders/1/cancel
```
