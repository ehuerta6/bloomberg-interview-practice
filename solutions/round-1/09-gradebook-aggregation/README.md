# Gradebook Aggregation — Reference Solution

## What broke

The draft combined scores into one equally weighted average. It did not apply category weights or remove the lowest entry from each category. It also kept differently capitalized names separate and used the rounded display average for the letter grade.

## Reproduce the issue

Run `python3 gradebook.py` in the starter folder. Weighted categories, dropped entries, normalized names, and threshold rounding show incorrect summaries. The corrected implementation has its own tests and runs independently with `python3 gradebook.py` here.

## Investigation approach

First combine every row for the same trimmed, case-insensitive student. For each weighted category, convert missing entries to zero, drop the requested lowest entries, and average what remains. Then combine the category means by their percentages. Check what happens when dropping empties a category and when rounding places the display at a grade boundary.

## Correction

The solution validates category mappings, percentage weights totaling 100, score lists, finite non-boolean percentage values, and a nonnegative integer drop count. It retains the first trimmed name spelling, counts all entries including missing and dropped ones, treats missing values as zero, and gives an empty post-drop category a mean of zero. It rounds the final weighted average to two decimals and assigns the letter from the unrounded result.

## Regression tests

The suite covers weighted means, per-category dropping, missing submissions, empty categories, merged names, entry counts, rounding and letter thresholds, plus malformed rows, weights, categories, scores, and drop counts. Run it with `python3 gradebook.py`.
