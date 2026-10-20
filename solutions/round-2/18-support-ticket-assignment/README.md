# Support Ticket Assignment Reference Solution

## Reported behavior

The queue can select a less urgent ticket ahead of the highest-priority open ticket.

## Reproduce and investigate

From this folder, run:

```sh
python3 test_support_tickets.py
```

Start with `routes.py` to see the request boundary, then follow the call into `service.py` and the in-memory `repository.py`. Reproduce the reported scenario and inspect repository state before and after each operation. The starter tests include examples that pass and a regression showing that the queue can select a less urgent ticket ahead of an urgent one.

## Fix

Route open tickets by descending priority, preserve FIFO within a priority, balance equal loads deterministically, and update both agents’ loads exactly once when a ticket moves.

## Regression coverage

The solution tests cover valid and invalid requests, state invariants, boundary conditions, repeated operations, and failure paths. They assert the data stored in the repository as well as returned results.

## Run the solution tests

```sh
python3 test_support_tickets.py
```
