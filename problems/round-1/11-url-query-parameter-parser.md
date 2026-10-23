# PR #11 — URL Query Parameter Parser

**Difficulty:** Easy

**PR title:** Parse query parameters for request routing

## Summary

A request router uses query parameters to search and filter a page. A user can select several tags, leave a filter blank, or enter text containing spaces. You are reviewing `parse_query` so these requests reach the handler with the intended values rather than losing repeated selections or encoded text.

## Input and output

`parse_query(query)` accepts a query string with or without a leading question mark and returns a dictionary mapping each key to an ordered list of values.

## Expected behavior and invariants
- Decode percent-encoded text and interpret `+` as a space in keys and values.
- Preserve the order of repeated values for a key.
- Keep both bare keys and explicit empty values as empty strings.
- Split a pair at its first equals sign, so later equals signs belong to the value.
- Ignore empty segments and return an empty mapping for an empty query.

## Contract example

For `parse_query("?q=red+fox&tag=a&tag=b&flag&redirect=a=b")`, the expected return is:

```python
{
    "q": ["red fox"],
    "tag": ["a", "b"],
    "flag": [""],
    "redirect": ["a=b"],
}
```

`parse_query("%74ag=one&empty=&q=red%20fox")` returns `{"tag": ["one"], "empty": [""], "q": ["red fox"]}`. Both the key and the value may contain percent-encoded text.

## Review task

Review the helper and its assertions against the decoded mapping contract. Correct discrepancies and add focused tests for repeated selections, blank values, encoded keys and values, and a value containing an equals sign. Explain how the tests verify value order as well as content.

## Starter Code

[View starter code](../../round-1/11-url-query-parameter-parser/)

## Reference Solution

[View solution](../../solutions/round-1/11-url-query-parameter-parser/)
