# Loan Disbursement Trend Analysis — Insight Report

**Project D17 | Banking & Finance | ABES Engineering College, MCA 2nd Year**  
**Skill track:** Data Analyst  
**Analysis period:** Jan 2021–Dec 2025  
**Data:** synthetic and illustrative; not actual customer or bank records.

## Executive summary

The cleaned dataset contains **12,000 transactions** (0 rows removed during cleaning). It includes **4,491 successful credit disbursements** totaling **INR 8,289,387,587**. The transaction-level success rate is **97.8%**.

## Key findings

- Peak month by amount: **February 2025**, INR 205,004,681.
- Largest loan type by disbursed amount: **Home** (INR 4,223,767,990, 51.0% of total).
- Successful disbursement count is used as a proxy for loans disbursed because the suggested schema does not include a separate loan approval or loan booking event.
- Delinquency flag rates describe flagged transactions in this illustrative dataset. A loan-level delinquency rate should be calculated from a validated loan status and an agreed delinquency definition.

### Disbursed amount by loan type

- **Home:** INR 4,223,767,990 across 984 successful credits.
- **Business:** INR 1,956,848,837 across 638 successful credits.
- **Vehicle:** INR 1,186,365,165 across 900 successful credits.
- **Education:** INR 562,364,817 across 551 successful credits.
- **Personal:** INR 360,040,778 across 1,418 successful credits.

## KPI definitions

- **Disbursed amount:** sum of `amount` for rows where `transaction_type = credit` and `status = success`.
- **Disbursement count:** count of those successful credit rows.
- **Average disbursement:** disbursed amount divided by disbursement count.
- **Transaction success rate:** all successful transaction rows divided by all cleaned transaction rows. It is not the disbursement success rate.
- **Delinquency flag:** count/rate of rows with `delinquency_flag = true`; interpret cautiously at transaction grain.

## Data preparation

Parsed transaction dates and numeric amounts, normalized category labels, removed duplicate transaction IDs, excluded rows missing required fields or with invalid amounts/status/type, and cleared failure reasons for successful records. **12,000 input rows** became **12,000 clean rows**.

## Recommendations

1. Compare monthly disbursed amounts and counts by loan type; investigate major shifts with business context before attributing causes.
2. Review failed transaction reasons and branch/channel patterns to identify operational follow-up areas.
3. Replace sample data with approved, privacy-safe source data and validate definitions with the business owner.
4. Add a stable loan-level disbursement event and dated delinquency status to support loan-level conversion and portfolio quality measures.

## Limitations

The sample data is generated for demonstration and has no real-world evidentiary value. The schema does not define approved amounts, unique loan origination events, reversals, or a delinquency aging threshold. A credit transaction is treated as a disbursement for this project; real deployments must validate that mapping.
