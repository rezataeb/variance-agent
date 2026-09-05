# Northwind Analytics — Finance Demo Data

This is a **synthetic, operationally realistic** dataset for a B2B SaaS data platform. It is designed for a Money Operations variance-analysis agent and does not represent a real company or real customers. Email addresses use the reserved `.example` domain.

## Files

- `monthly_summary_2026-07.csv` — July management summary
- `monthly_summary_2026-08.csv` — August management summary
- `transactions_2026-07.csv` — 180 transaction rows
- `transactions_2026-08.csv` — 210 transaction rows
- `Northwind Analytics Finance Demo Data.xlsx` — the same four datasets in one formatted workbook

## Management story

Northwind Analytics accelerated in August after several enterprise wins, while entry-level customer health weakened.

| Metric | July 2026 | August 2026 | Change |
|---|---:|---:|---:|
| Total revenue | $342,500 | $404,850 | +$62,350 / +18.2% |
| Enterprise revenue | $185,000 | $244,000 | +$59,000 / +31.9% |
| SMB revenue | $118,000 | $124,510 | +$6,510 / +5.5% |
| Starter revenue | $39,500 | $36,340 | -$3,160 / -8.0% |
| COGS | $79,140 | $84,670 | +7.0% |
| OPEX | $186,000 | $208,320 | +12.0% |
| Sales OPEX | $74,000 | $91,460 | +23.6% |
| Lost MRR | $1,240 | $2,574 | +107.6% |

Enterprise is the clear growth driver. Acme Corp, Globex, and Initech contribute **$37,760, or 64.0%, of the $59,000 enterprise increase** when their complete monthly billings are compared across periods.

The August data includes the visible deal events:

- Acme Corp: $18,500 expansion on August 12
- Globex: $14,200 expansion on August 18
- Initech: $12,800 new enterprise contract on August 5

Six Starter cancellations create $2,574 of lost MRR. Revenue still grew strongly, but the pattern suggests dependence on a small number of enterprise deals and emerging weakness at the low end.

## Definitions

- **Revenue rows are net billings by tier.** Sum only rows where `category = Revenue` for total revenue.
- **Churn is a memo metric.** Do not add the summary `Churn` row to revenue again. Negative transaction rows are already reflected in Starter revenue.
- **Account count** is the active billed-account count at month-end for Revenue rows; on the Churn row it is the number of cancellations.
- **MRR** is the recurring revenue represented by that summary line.
- **Transaction type** is one of `new`, `expansion`, `renewal`, or `churn`. Churn amounts are negative.
- **Contact email** is synthetic and safe for demos; every address ends in `.example`.

## Reconciliation checks

For each month, group transactions by `tier` and sum `amount`. The results exactly match the three Revenue rows in the corresponding monthly summary. Total transaction amounts also reconcile exactly to total revenue:

```text
July:   $185,000 + $118,000 + $39,500 = $342,500
August: $244,000 + $124,510 + $36,340 = $404,850
```

The three named enterprise customers reconcile to the 64% claim using full customer-period totals, not just the individual expansion event rows:

```text
Enterprise increase: $244,000 - $185,000 = $59,000
Named-account contribution: $37,760
$37,760 / $59,000 = 64.0%
```

## Suggested agent workflow

1. Load both summary files and identify the largest absolute and percentage variances.
2. Rank the Revenue, COGS, and OPEX changes separately.
3. For material Revenue variances, group transaction data by tier, customer, and type.
4. Compare each customer's complete July and August totals; surface the top contributors.
5. Check concentration, churn count, lost MRR, and whether expense growth supports or threatens the revenue gain.
6. Produce a concise answer with exact dollar amounts, percentages, named drivers, and reconciliation evidence.

## Expected evidence-backed explanation

> August revenue increased $62,350, or 18.2%, to $404,850. Enterprise contributed $59,000 of growth and rose 31.9%. Acme, Globex, and Initech produced $37,760 of the enterprise increase, equal to 64.0%. Starter revenue fell 8.0% as six cancellations generated $2,574 of lost MRR. OPEX rose 12.0%, led by a 23.6% increase in Sales expense, consistent with the enterprise push.

## Modeling note

The requested headline totals, exact enterprise amount, and an 8% Starter decline mathematically require SMB to increase by $6,510 rather than remain perfectly flat. The dataset treats +5.5% SMB growth as comparatively stable next to the 31.9% enterprise increase so that all headline totals reconcile exactly.
