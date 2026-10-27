# Ticket #18 — Support Ticket Assignment

**Difficulty:** Easy

## Practice Metadata

- **Interview format:** Engineering ticket / existing-code debugging.
- **Primary skills:** priority ordering, FIFO behavior, load-aware dispatch.
- **Expected duration:** 50–60 minutes.
- **AI assistance:** Allowed in guided practice mode for explanations, hypotheses, test ideas, and focused hints; the candidate owns and explains every change.
- **Candidate objective:** Trace why an older lower-priority ticket is selected and correct the dispatch order while preserving the assignment-load invariant.
- **Interviewer evaluation:** Problem decomposition, code navigation, root-cause explanation, incremental implementation, and test evidence. See the [shared interviewer rubric](../../docs/editorial/interviewer-rubric.md).

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

## Core acceptance criteria

- Select the highest-priority open ticket in the requested category. Equal
  priorities preserve submission order, and an assigned ticket is not dispatched
  again.
- Assign the selected ticket to an eligible agent with the lowest current load.
  An empty category queue returns no ticket.
- After assignment, the selected ticket has one assignee and that agent's load
  increases by one.

## Optional follow-ups

If time remains, inspect malformed submissions, reassignment, and tie behavior
for equally loaded agents. Agree on any unspecified tie policy with the
interviewer before implementing it.

## Out of Scope

Keep the configured teams and route response shapes. Agent availability,
automatic escalation, ticket resolution, and changing the tie-breaking policy
are outside this ticket.

## Investigation

Reproduce the priority report and verify the selected ticket and agent load. Add a focused test for equal-priority FIFO ordering. Discuss how you would clarify an equal-load tie before choosing a policy.

## Starter Code

[View starter code](../../round-2/18-support-ticket-assignment/)

## Reference Solution

[View solution](../../solutions/round-2/18-support-ticket-assignment/)
