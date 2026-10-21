# Ticket #18 — Support Ticket Assignment

**Difficulty:** Easy

## Problem

### Reported symptom

The support desk receives tickets from billing and technical queues. The on-call lead reports that urgent tickets can remain queued behind routine requests.

### Scenario

Trace ticket creation order into the queue selection, then follow workload changes through assignment and reassignment. Compare the repository’s load counters with actual assigned tickets after each transition.

## Acceptance Criteria
- Reject malformed or duplicate tickets without state changes.
- Treat priority 5 as most urgent and priority 1 as least urgent.
- Preserve FIFO among equal-priority tickets.
- Assign only open tickets to eligible category agents.
- Keep workload counters equal to assigned-ticket counts after reassignment.

## State Invariants
- Every assigned ticket has exactly one eligible assignee.
- For each agent, load equals the count of tickets assigned to that agent.
- Assignment consumes the highest-priority open ticket; ties preserve submission order.

## Investigation

Follow a submitted ticket as multiple agents claim work, including a tie in priority and an agent who is not eligible for the ticket's category. After assignment and reassignment, compare each agent's load counter with the tickets actually assigned to that agent.

## Starter Code

[View starter code](../../round-2/18-support-ticket-assignment/)

## Reference Solution

[View solution](../../solutions/round-2/18-support-ticket-assignment/)
