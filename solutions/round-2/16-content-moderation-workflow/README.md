# Content Moderation Workflow Reference Solution

## What Was Broken

The starter accepted a review from the post’s author. The author could approve or reject their own pending post, and the service would change the post state and append that decision to the audit log.

## Reproduce and Investigate

From this folder, run `python3 test_moderation_workflow.py`. The self-review case submits a post as `author-1`, then attempts to approve it as the same user. Check both the returned status and the post and audit records afterward. Also trace the repeated-decision test to see how a pending post becomes terminal.

## The Fix

Before changing state, `review` rejects an author reviewing their own post with `forbidden`. A valid reviewer can decide only a pending post, and only `approve` or `reject` are accepted. Successful decisions update the post and append an audit event containing the post, reviewer, decision, and note. Invalid, forbidden, or conflicting requests leave state and audit history untouched.

## Regression Tests

The suite covers an approved post and its audit actor, forbidden self-review, a second decision against a terminal post, and an unsupported decision that must not mutate state.

## Run

```sh
python3 test_moderation_workflow.py
```
