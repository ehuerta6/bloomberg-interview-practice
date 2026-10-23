# PR #17 — Search Ranking

**Difficulty:** Medium

**PR title:** Rank search results by normalized relevance

## Summary

A search endpoint must put documents with relevant titles ahead of weaker body-only matches while keeping equally relevant results predictable. You are reviewing the ranking PR, which returns document IDs and normalized scores so the caller can display a limited result list.

## Input and output

`rank_results(query, documents, limit=None)` accepts a query string and documents containing `id`, `title`, and `text`. It returns matching documents as `{id, score}` mappings.

## Expected behavior and invariants
- Normalize query and document text by case-folding and tokenizing contiguous letters and digits. Count each distinct query token once.
- Each query token present in a title is worth 3 points; each present in the body text is worth 1 point.
- Normalize the total by `4 × number of distinct query tokens`, producing a score from 0 through 1. Round returned scores to four decimals.
- Exclude documents with no matching query tokens. Sort by descending score and preserve input order for ties.
- `limit` is optional or a nonnegative integer; booleans are invalid. A zero limit or query with no tokens returns an empty list.
- Malformed query, document, or limit input raises `ValueError`.

## Contract example

Search for `"PYTHON!"` in these documents, in this order:

```python
[
    {"id": "body", "title": "Notes", "text": "python guides"},
    {"id": "title", "title": "Python guides", "text": "language"},
    {"id": "mixed", "title": "Python", "text": "guides"},
]
```

Expected return:

```python
[
    {"id": "title", "score": 0.75},
    {"id": "mixed", "score": 0.75},
    {"id": "body", "score": 0.25},
]
```

For this one-token query, a title match earns 3 of 4 possible points and a body-only match earns 1 of 4. `limit=1` returns only `title`. Repeating the query token as `"PYTHON! python"` does not change these scores.

## Review task

Review the ranking and tests against normalized matching, distinct query terms, and stable score ties. Correct discrepancies and add cases that check numeric scores as well as document order, including a limited result list and a query without tokens. Explain why equal-scoring documents keep their input order.

## Starter Code

[View starter code](../../round-1/17-search-ranking/)

## Reference Solution

[View solution](../../solutions/round-1/17-search-ranking/)
