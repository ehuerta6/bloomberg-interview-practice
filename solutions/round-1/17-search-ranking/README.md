# Search Ranking — Reference Solution

## What broke

The draft used whitespace splitting for search terms and sorted score ties using document IDs as a secondary key. That can make punctuation and repeated terms affect relevance, and can reorder equally relevant results.

## Reproduce the issue

Run `python3 search_rank.py` in the starter folder. Try punctuation, repeated terms, and equal-scoring documents in a deliberate input order. Run the corrected independent suite with `python3 search_rank.py` here.

## Investigation approach

Define one normalized token set for the query and for each title and body. For each distinct query term, award three points for a title hit and one for a body hit. Divide by four times the number of query terms so the result is between zero and one, then check sorting and truncation.

## Correction

The solution tokenizes case-folded alphanumeric text, scores each distinct query term once, normalizes scores to 0–1, excludes zero-match documents, and uses stable descending score order. A nonnegative optional limit is applied after ranking.

## Regression tests

Tests cover title/body relevance, normalization, repeated terms, stable ties, result limits, empty queries, unmatched documents, and malformed inputs. Run them with `python3 search_rank.py`.
