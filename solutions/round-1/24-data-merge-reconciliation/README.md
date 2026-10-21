# Data Merge Reconciliation — Reference Solution

## What broke

For a newer snapshot, the draft replaces the whole dictionary, so tags present only in the existing record disappear. For an unmatched existing customer, `record.copy()` is shallow, so editing the returned `tags` list also edits the caller's input.

## Reproduce the issue

From `round-1/24-data-merge-reconciliation/`, run `python3 merge_records.py`. `test_tags_are_union_of_both_sources` drops `"vip"`; `test_result_records_do_not_share_tag_lists_with_inputs` mutates the original list through the result. Run it in this solution folder to confirm both regressions pass.

## Investigation approach

Trace how `merged` is initialized and how a matching incoming record replaces `merged[customer_id]`. That replacement selects the right newer ordinary fields but discards the older tag list. Also inspect the shallow `copy()` calls for existing and new records: nested lists remain shared even when the outer dictionaries are distinct.

## Correction

The solution copies each record and its tag list. For a matching ID, it chooses ordinary fields by timestamp (incoming wins ties), then builds a stable de-duplicated union from existing tags followed by incoming tags regardless of which snapshot wins. Existing order is kept and new IDs are appended in incoming order.

## Regression tests

`test_tags_are_union_of_both_sources` and `test_result_records_do_not_share_tag_lists_with_inputs` cover tag loss and aliasing. The suite also checks newer, older, and tied timestamps; stable customer ordering; and unchanged inputs. Run it with `python3 merge_records.py`.
