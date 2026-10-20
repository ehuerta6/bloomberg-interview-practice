# Ticket 18: Support Ticket Assignment (Easy)

## Ticket

Support Ticket Assignment needs reliable state transitions.

## Reported symptom

The support desk receives tickets from billing and technical queues. The on-call lead reports that urgent tickets can remain queued behind routine requests.

## Scenario

Trace ticket creation order into the queue selection, then follow workload changes through assignment and reassignment. Compare the repository’s load counters with actual assigned tickets after each transition.

## Acceptance criteria

- Reject malformed or duplicate tickets without state changes.
- Treat priority 5 as most urgent and priority 1 as least urgent.
- Preserve FIFO among equal-priority tickets.
- Assign only open tickets to eligible category agents.
- Keep workload counters equal to assigned-ticket counts after reassignment.

## State invariants

- Every assigned ticket has exactly one eligible assignee.
- For each agent, load equals the count of tickets assigned to that agent.
- Assignment consumes the highest-priority open ticket; ties preserve submission order.

## Investigation task

Trace a normal operation, a boundary or failure case, and a repeated request across the route, service, and repository. Explain which state should change, which state must remain untouched, and how your regression tests demonstrate both outcomes. Keep the implementation in memory; no external services or frameworks are required.

## Run the starter tests

```sh
python3 test_support_tickets.py
```

## Exercise folders

- [Starter exercise](../../round-2/18-support-ticket-assignment/)
- [Reference solution](../../solutions/round-2/18-support-ticket-assignment/)
