# Ticket #18 — Support Ticket Assignment

**Difficulty:** Easy

## Context

You maintain dispatch for a support desk with billing and technical teams.
Tickets have integer priorities from 1 (least urgent) to 5 (most urgent).
**FIFO** means submission order is preserved among equally urgent tickets.
Agent load is the count of tickets currently assigned to that agent.

## Practice report

Create technical tickets `low` at priority 1, `urgent` at 5, and `mid` at 3 in
that order. With all agent loads initially zero, call `assign_next("technical")`.

| Observation | Current starter | Expected |
| --- | --- | --- |
| Ticket selected | `low` | `urgent` |
| Assigned agent | `Cal` | `Cal` |

The next selection should be `mid`, assigned to the less-loaded eligible agent.

## Acceptance Criteria

- Reject malformed/duplicate ticket submissions without changing saved tickets
  or loads. Priority is an integer from 1 through 5; booleans are invalid.
- Select the highest-priority open ticket in the requested category. Equal
  priorities preserve submission order, and an assigned ticket is not dispatched again.
- Assign to an eligible agent with the lowest current load. Keep the supplied
  agent-list order for equal loads. An empty category queue returns no ticket.
- Each assigned ticket has exactly one eligible assignee. After assignment or
  reassignment, every agent's load equals their assigned-ticket count.
- Reassignment moves one unit of load from the old assignee to the new one.
  Unknown/unassigned tickets and agents outside that ticket's category are rejected
  without state changes.

## Out of Scope

Keep the configured teams and route response shapes. Agent availability,
automatic escalation, ticket resolution, and changing the tie-breaking policy
are outside this ticket.

## Investigation

Trace selection and assignment for the report, then test equal priorities,
independent categories, and reassignment. Compare actual assigned tickets with
load counters after each transition, including a rejected reassignment.

## Starter Code

[View starter code](../../round-2/18-support-ticket-assignment/)

## Reference Solution

[View solution](../../solutions/round-2/18-support-ticket-assignment/)
