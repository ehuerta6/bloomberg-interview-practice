# Cappy Marketplace
Cappy Marketplace — a realistic full-stack codebase for CIC Nightmare Mode interview practice.

Fork or clone the repository and run it locally using the instructions below. No cloud environment or container is required.

Cappy Marketplace is self-contained in this `marketplace/` directory. From the
parent repository, run `cd marketplace` before using these commands.

## Local setup

Requirements: Python 3.11 or newer.

On macOS and Linux, use the system `python3` command to create the virtual
environment. After activation, `python` refers to the environment's interpreter:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m app.db seed
uvicorn app.main:app --reload
```

The app is local-only. Open `http://127.0.0.1:8000/` for the marketplace or
`http://127.0.0.1:8000/health` to confirm the server responds. The SQLite
database is created at `data/cappy.sqlite3` by default. Set `CAPPY_DB_PATH` to
use another local database file.

Run the automated checks with:

```sh
pytest
```

The parent repository's **Marketplace tests** GitHub Actions job runs this
backend and API test suite on pull requests and pushes to `main`.

With the virtual environment active, restore the deterministic fictional users,
products, stock, and empty shopper carts with:

```sh
python -m app.db reset
```

`seed` is safe to run more than once and adds any missing starter rows. `reset`
clears local changes and restores the original fixture state. Neither command
uses a hosted service. The seeded identities are local selectors, not real
accounts or credentials.

## Product catalog API

`GET /products` lists the catalog and `GET /products/{product_id}` reads one
product. Product prices are integer cents; categories are `food`, `stones`,
`sticks`, or `toys`. An unknown product returns HTTP 404.

Create products with `POST /admin/products` and update an existing product with
`PUT /admin/products/{product_id}`. These local admin routes require
`X-User-Id: admin-stone`. The seeded shopper selector `shopper-river` receives
HTTP 403 on admin routes, and a missing or unknown selector receives HTTP 401.
This header selects a seeded local role for practice; it is not real
authentication. Names must be non-empty, IDs use lowercase letters, digits
and hyphens, and price and stock must be nonnegative integers.

## Shopper cart API

Cart routes use the selected shopper in `X-User-Id`. `GET /cart` returns that
shopper's items and current-price totals. `POST /cart/items` adds the requested
quantity to an item; `PUT /cart/items/{product_id}` sets its quantity, and
`DELETE /cart/items/{product_id}` removes it. Quantities must be positive
integers and cannot exceed current stock. Invalid quantities return HTTP 422,
unknown products return HTTP 404, and requests exceeding stock return HTTP 409.
Cart rows are stored in the configured SQLite database and survive restarting
the app with the same database path.

## Checkout API

`POST /checkout` requires `X-User-Id` and an `Idempotency-Key` header scoped to
that shopper. Its JSON `payment_outcome` is `success` (the default), `decline`,
or `temporary_error`. A successful checkout returns HTTP 201 with a persisted
order, deducts stock, and clears the cart. Decline returns HTTP 402 and a
temporary payment error returns HTTP 503; both leave the cart and stock intact.
An empty cart or insufficient stock returns HTTP 409 without creating an
order.

Reusing the same key with the same payment outcome replays the original result:
successful orders return HTTP 200 with the same order, and failed attempts
repeat their original status and detail. Reusing a key with a different
outcome returns HTTP 409. Use a new key for a new attempt after a failure.
Order lines preserve the purchased product name, category, unit price, and
quantity, even if the catalog changes later.

## Admin order and inventory API

The seeded admin can inspect all orders through `GET /admin/orders` and adjust
inventory through `POST /admin/products/{product_id}/stock-adjustments`. Order
views are read-only. See [docs/admin.md](docs/admin.md) for the stock adjustment
contract and validation responses.

## Marketplace interface

The storefront and admin room are served at `/` and use the API contracts
above. Use the identity selector to switch between the seeded shopper and
admin. Shoppers can browse, manage a persisted cart, try mock checkout outcomes,
review orders, and cancel eligible orders. Admins can create and edit products,
adjust stock, and inspect orders without order controls. The interface uses
vanilla HTML, CSS, and JavaScript; the backend remains responsible for
validation, stock, cancellation, and payment outcome rules.

## AI-assisted practice

Share the specific task and acceptance criteria before asking an AI assistant
to change code. The [AI Interview Mode policy](AGENTS.md) lets it inspect and
explain the code, run commands, write tests, and implement a well-defined
request while keeping the student in charge of scope and decisions. Students
should run relevant tests and the full suite, then explain what the results do
and do not prove. The browser-independent `tests/test_smoke.py` exercises the
shopper and admin API workflows; it does not verify browser rendering.
