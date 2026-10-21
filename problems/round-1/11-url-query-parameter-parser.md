# PR #11 — URL Query Parameter Parser

**Difficulty:** Easy

**PR title:** Parse query parameters for request routing

## Summary

A lightweight router needs a predictable mapping from URL query parameters to values. Review the helper and its behavior for repeated, blank, and encoded parameters.

## Input and output

`parse_query(query)` accepts a query string with or without a leading question mark and returns a dictionary mapping each key to an ordered list of values.

## Expected behavior and invariants
- Decode percent-encoded text and interpret `+` as a space in keys and values.
- Preserve the order of repeated values for a key.
- Keep both bare keys and explicit empty values as empty strings.
- Split a pair at its first equals sign, so later equals signs belong to the value.
- Ignore empty segments and return an empty mapping for an empty query.

## Review task

Compare the helper with familiar browser query strings. Exercise repeated keys, blank values, spaces, percent escapes in both keys and values, and values containing equals signs. Add a small test for each distinct parsing rule.

## Starter Code

[View starter code](../../round-1/11-url-query-parameter-parser/)

## Reference Solution

[View solution](../../solutions/round-1/11-url-query-parameter-parser/)
