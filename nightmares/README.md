# Nightmare Mode

Nightmare Mode is exactly ten original CIC exercises grounded in the local Cappy Marketplace: five Engineering Tickets and five PR Reviews. They are independent practice scenarios, not official Bloomberg interview questions.

| # | Challenge | Type |
|---:|---|---|
| 01 | [Duplicate Checkout](01.md) | Engineering Ticket |
| 02 | [Inventory Validation](02.md) | PR Review |
| 03 | [Double Cancellation](03.md) | Engineering Ticket |
| 04 | [Cart Ownership Leak](04.md) | PR Review |
| 05 | [Checkout Price Mismatch](05.md) | Engineering Ticket |
| 06 | [Payment Error Handling](06.md) | PR Review |
| 07 | [Partial Checkout Failure](07.md) | Engineering Ticket |
| 08 | [Admin Authorization Regression](08.md) | PR Review |
| 09 | [Cart Update Race](09.md) | Engineering Ticket |
| 10 | [Misleading Regression Tests](10.md) | PR Review |

## Start

1. Clone or fork this repository and read the selected numbered assignment here.
2. Check out its pinned `night-NN-v1` tag or matching `challenge/NN` branch.
3. Work from `marketplace/`. Follow its [setup guide](../marketplace/README.md) to install dependencies, reset the local database, run the app, and run tests.
4. Use an AI assistant as a technical partner. You direct investigation and code changes; the policy is in [`marketplace/AGENTS.md`](../marketplace/AGENTS.md).

Engineering Tickets ask you to investigate the reproduction, implement a focused correction, and verify it. PR Reviews ask you to inspect the linked diff and deliver actionable findings and test recommendations; a replacement implementation is optional. Run relevant checks and the full suite, then explain the behavior, evidence, tradeoffs, and remaining uncertainty in your own words.

The old [`NIGHT-01.md`](NIGHT-01.md) and [`NIGHT-02.md`](NIGHT-02.md) paths remain as compatibility links to numbered assignments. The `night-01-v1`, `night-02-v1`, `challenge/night-01`, and `challenge/night-02` refs and open PR #48 are preserved.
