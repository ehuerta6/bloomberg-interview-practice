# Ticket 23: Product Returns & Exchanges (Medium)

## Ticket

Product Returns & Exchanges needs reliable state transitions.

## Reported symptom

A store accepts customer returns for refunds or size exchanges. A failed replacement lookup left returned stock available even though no exchange was recorded, and customers could exceed the quantity purchased by splitting requests.

## Scenario

Exercise a refund and exchange from the same order line, then try exceeding the original purchased quantity. Force an exchange failure with no replacement stock and compare stock and return records before and after.

## Acceptance criteria

- Refund amount equals returned quantity times the original unit price.
- Refund and exchange return the original SKU to stock.
- Exchange consumes replacement stock only when available.
- Failed requests make no stock or ledger changes.
- Return limits account for earlier refunds and exchanges combined.

## State invariants

- A line cannot have more units returned than purchased.
- Every completed return case corresponds to exactly one stock and financial effect.
- Stock counts never become negative.
- Replaying a return ID cannot apply effects twice.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_returns.py
```

## Exercise folders

- [Starter exercise](../../round-2/23-product-returns-exchanges/)
- [Reference solution](../../solutions/round-2/23-product-returns-exchanges/)
