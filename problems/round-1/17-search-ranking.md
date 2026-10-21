# PR #17 — Search Ranking

**Difficulty:** Medium

**PR title:** Rank search results by normalized relevance

## Summary

A search endpoint ranks documents using query matches in titles and body text, then returns an optional top slice. Review normalization, relevance scoring, stable ties, and limits.

## Input and output

`rank_results(query, documents, limit=None)` accepts a query string and documents containing `id`, `title`, and `text`. It returns matching documents as `{id, score}` mappings.

## Expected behavior and invariants
- Normalize query and document text by case-folding and tokenizing contiguous letters and digits. Count each distinct query token once.
- Each query token present in a title is worth 3 points; each present in the body text is worth 1 point.
- Normalize the total by `4 × number of distinct query tokens`, producing a score from 0 through 1. Round returned scores to four decimals.
- Exclude documents with no matching query tokens. Sort by descending score and preserve input order for ties.
- `limit` is optional or a nonnegative integer; booleans are invalid. A zero limit or query with no tokens returns an empty list.
- Malformed query, document, or limit input raises `ValueError`.

## Review task

Compare title-only, body-only, and mixed matches. Try punctuation and repeated query terms, then construct equal-scoring documents in a deliberate order and verify the limited output.

## Starter Code

[View starter code](../../round-1/17-search-ranking/)

## Reference Solution

[View solution](../../solutions/round-1/17-search-ranking/)
