# STEP 10 - SYNTHETIC DATASET GENERATION
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Dataset label:** DEMO-SYNTHETIC | **Status:** MVP generation specification

## 1. Purpose and ethical boundary

Generate a deterministic, self-contained transaction dataset to support analysis and testing without using real customer data. Records are fictional and are not statistically calibrated to any actual bank, borrower population, branch network, or lending performance. Every export and application view must retain a synthetic-data label.

## 2. Grain and schema

One row represents one synthetic transaction event. Required fields: `transaction_id`, `transaction_date`, `customer_id`, `account_id`, `account_type`, `branch_id`, `transaction_type`, `event_type`, `channel`, `amount`, `status`, `failure_reason`, `loan_id`, `loan_type`, `delinquency_flag`. Optional helper fields: `region`, `seed_version`. Enum sets are documented in README and code constants.

## 3. Default generation profile

| Attribute | Default | Rationale / caution |
|---|---|---|
| Row count | 12,000 transaction events | Small enough for laptop/Cloud demo |
| Date range | 2021-01-01 through 2025-12-31 | Supports multi-year monthly trends; not a real history |
| Seed | 42 | Repeatable baseline |
| Branches | 30 across 5 synthetic regions | Enables branch filter; labels are fictitious |
| Channels | ATM, UPI, Net Banking, Branch | Assignment suggested values |
| Account types | Savings, Current | Synthetic category values |
| Loan types | Personal, Home, Vehicle, Education, Business | Synthetic taxonomy |
| Event types | Disbursement, Repayment, Reversal | Explicit event semantics |
| Outcomes | Success, Failed | Failure reason present only where relevant |
| Currency | INR | Initial assumption A-006; replace if OQ-004 resolves otherwise |

## 4. Generation logic and consistency

1. Generate customer, account, branch and loan entities first with stable deterministic IDs.
2. Assign each loan one consistent customer, servicing account, loan type and sample delinquency flag.
3. Generate event dates using a deterministic distribution across the specified period; include seasonality/trend only as a synthetic illustration and document it.
4. Assign event type and direction consistently: disbursement credit, repayment debit, reversal as an explicitly modeled compensating event. Do not use credit/debit alone to infer event.
5. Generate positive amounts by event/loan type within documented illustrative ranges; failed attempts are not funded. Reversal is a separate event and the MVP gross disbursement KPI excludes it.
6. Generate transaction outcomes with configurable probabilities for demonstration, not a performance claim. Provide failure reasons from a small synthetic enumeration for failures.
7. Verify unique transaction IDs, foreign-key consistency, enum membership, date bounds, positive amount, and deterministic reproducibility.

## 5. Output artifacts and lineage

- `data/loan_transactions_sample.csv`: flat, analysis-friendly synthetic sample with dimension attributes joined for convenience.
- `data/loan_transactions_clean.csv`: validated sample snapshot, if a distinct clean artifact is maintained.
- SQLite tables: normalized customers/accounts/branches/loans/transaction_event plus dataset_metadata.
- Metadata: generator version, seed, row count, generation time, schema version, and quality summary.
- Runtime-generated local database is ignored by Git unless intentionally included as a seeded demo artifact.

## 6. Data quality and privacy checks

Check required fields, duplicate transaction ID, valid date range, amount > 0, allowed categories, event-direction consistency, successful/failed status, failure reason rules, and all foreign keys. Reject or quarantine malformed rows with explicit reason counts. Do not generate names or direct identifiers. Keep IDs synthetic and avoid demographics that are unnecessary for the business questions.

## 7. Limitations and assumptions

OQ-001 is resolved for the synthetic model using explicit event_type; confirm real system mapping separately. OQ-002 uses the stated default period and volume. OQ-003 category sets follow the assignment. A-006 uses INR pending confirmation. Delinquency flag has no aging basis and must not be interpreted as actual arrears. Generated patterns support software demonstration only.

## 8. Reproduction

Run the repository's dataset generation command with seed 42 for the baseline. The implementation records seed and version and includes tests that compare repeated outputs. Change seed/row count only through explicit arguments; the committed baseline CSV should be reproducible from documented defaults.
