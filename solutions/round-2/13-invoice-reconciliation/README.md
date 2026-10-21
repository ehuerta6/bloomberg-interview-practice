# Invoice Reconciliation Reference Solution

## What Was Broken

The starter recorded each payment but never checked whether its payment reference was already present. A duplicated bank notification could add the same installment twice, making the invoice balance incorrect or causing a false overpayment.

## Reproduce and Investigate

From this folder, run `python3 test_invoice_reconciliation.py`. The duplicate-reference case applies `pay-3` twice and compares the invoice’s paid amount and stored payment count. Follow `apply_payment` into `InvoiceStore`: payment references identify incoming remittances and must be checked before changing the invoice.

## The Fix

The service returns the current invoice state for a replay with the same reference, invoice, and amount, without changing the paid amount again. If a reference is reused with a different amount or invoice, it returns `conflict`. New positive payments are recorded only when they fit the remaining balance; exact settlement marks the invoice `paid`, smaller installments leave it `partial`, and overpayments are rejected before either record changes.

## Regression Tests

The suite covers two installments that settle an invoice exactly, duplicate references, changed amount or invoice under an existing reference, and an overpayment that leaves the paid amount unchanged.

## Run

```sh
python3 test_invoice_reconciliation.py
```
