# D17 - Loan Disbursement Trend Analysis: Insight Report

**ABES Engineering College | MCA 2nd Year | Data Analyst**  
**Learner:** Vansh Varshney | **Roll:** 2500320140161 | **Mentor:** Kalpana Dwivedi  
**Data:** Synthetic only | **Period:** 2021-01-01 to 2025-12-31 | **Seed:** 42

## Executive summary

The generated dataset has **12,000 valid synthetic transaction events** and **0 rejected rows**. It contains **4,132 successful disbursement events** totaling **INR 7,279,333,054.33**. Transaction success rate is **97.79%**; disbursement-attempt success rate is **96.41%**.

## Descriptive findings

- Highest monthly successful disbursement amount in this generated sample: **May 2025 (INR 187,898,932)**.
- Highest loan-type amount in this sample: **Home (INR 3,588,918,562)**.
- Highest branch amount in this sample: **South Branch 07 (INR 337,643,700)**.
- The chart and filters support comparison by date, loan type, branch, channel and status.

These are descriptive outputs of the specified random generator, not findings about an actual bank, customer base, or market.

## KPI definitions

- **Successful disbursed amount:** sum of `amount` where `event_type=disbursement` and `status=success`.
- **Disbursement event count:** count of those successful events; not necessarily distinct loans.
- **Average disbursement:** amount divided by successful disbursement event count.
- **Transaction success rate:** successful transactions divided by all selected transactions.
- **Disbursement-attempt success rate:** successful disbursement events divided by all disbursement attempts.
- **Failed disbursement amount:** failed disbursement attempt amount, displayed separately from funded amount.

## Data preparation and quality

Rows checked: 12,000; valid: 12,000; rejected: 0. The generator/validator checks required fields, parsing, category values, event-direction consistency, positive amounts, duplicate transaction IDs, stable entity mappings and relationship consistency. Seed/version metadata is saved in `outputs/data_quality.json`.

## Recommendations for a real analysis

1. Confirm the event-system definition of disbursement and reversal netting before interpreting any total.
2. Replace synthetic data only with an authorized, privacy-safe dataset and preserve lineage/quality checks.
3. Define delinquency with an agreed loan-level grain and days-past-due threshold before reporting risk measures.
4. Review observed failure patterns with business owners; do not infer causes from these generated records.

## Limitations

This dataset is synthetic, seeded, and intentionally illustrative. INR is an assumption. Gross disbursement totals exclude reversal netting. Sample loan flags have no arrears aging definition. No causal, predictive, approval, or creditworthiness inference is supported.
