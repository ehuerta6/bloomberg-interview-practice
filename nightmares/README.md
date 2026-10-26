# Nightmare Mode

Nightmare Mode has two original, timed exercises that practice AI-assisted debugging and pull request review in the local Cappy Marketplace. They are independent CIC practice scenarios, not official Bloomberg interview questions.

1. [NIGHT-01 — Duplicate Checkout](NIGHT-01.md): investigate and fix a checkout retry reliability ticket (Hard, 45–60 minutes).
2. [NIGHT-02 — Inventory Validation Review](NIGHT-02.md): review an inventory adjustment change and its tests (Medium–Hard, 30–45 minutes).

## Start

1. Clone or fork this repository and read the selected assignment here.
2. Check out its pinned tag: `night-01-v1` or `night-02-v1`.
3. Work from `marketplace/`. Follow its [setup guide](../marketplace/README.md) to install dependencies, reset the local database, run the app, and run tests.
4. Use an AI assistant as a technical partner. Give it the relevant task and acceptance criteria, direct investigation or changes, and review the evidence it reports. The policy is in [`marketplace/AGENTS.md`](../marketplace/AGENTS.md).

For NIGHT-01, investigate the failing reproduction and make a focused fix with regression coverage. For NIGHT-02, review the linked PR diff and deliver actionable, evidence-based findings plus stronger test recommendations; a replacement implementation is not required. In either exercise, run the relevant checks and full suite, then explain the behavior, evidence, tradeoffs, and remaining uncertainty in your own words.
