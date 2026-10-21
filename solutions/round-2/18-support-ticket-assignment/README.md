# Support Ticket Assignment Reference Solution

## What was wrong

`TicketService.assign_next` selected the smallest priority number first. Since 5 is the most urgent priority, a routine priority 1 ticket could be assigned before an urgent priority 5 ticket. The rest of the routing flow already filters to open tickets and balances assignments by agent load.

## Reproduce and investigate

From the starter folder, run:

```sh
python3 test_support_tickets.py
```

Create tickets with priorities 1, 5, and 3, then assign the technical queue. The urgent ticket should be assigned first. Follow the request through `routes.py` into `TicketService.assign_next` in `service.py`; inspect how `repository.py` preserves ticket insertion order and tracks agent loads.

## Fix

Select the open ticket with the greatest priority number. Python’s stable selection preserves submission order for equal priorities. Keep load balancing separate from ticket priority, and move one unit of load from the old assignee to the new assignee during reassignment.

## Regression tests

- `test_priority_then_balanced_routing` proves priority 5 precedes 3 and 1, and the next assignment goes to the less-loaded eligible agent.
- `test_priority_ties_are_fifo` checks arrival order for equal priorities.
- `test_reassignment_moves_load_exactly_once` checks that the old agent’s load drops and the new agent’s load rises once.
- The remaining tests cover empty queues, invalid priority, missing tickets, category boundaries, and avoiding a second dispatch of an assigned ticket.

## Run the solution tests

```sh
python3 test_support_tickets.py
```
