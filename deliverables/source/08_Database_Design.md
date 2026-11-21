# STEP 8 - DATABASE DESIGN
## D17 | Loan Disbursement Trend Analysis

**Database:** SQLite | **Version:** 1.0 | **Status:** Proposed logical/physical design

## 1. Purpose and workload

Persist the deterministic synthetic entities and transaction events so Streamlit can query filterable aggregates repeatably. Expected MVP workload is one local writer during sample initialization and read-oriented analytics over approximately 12,000 synthetic transactions. This is not a multi-tenant or high-concurrency banking store.

## 2. Grain and normalization

The central fact is one row per transaction event (`transaction_id`). Supporting entities separate customer, account, branch and loan attributes. Proposed schema is substantially normalized (3NF for descriptive attributes). Dashboard aggregations can be computed from indexed joins; a materialized aggregate table is unnecessary for MVP. Enforce referential integrity and uniqueness on stable synthetic identifiers.

## 3. Logical schema

### customer

`customer_id TEXT PRIMARY KEY`; `created_at TEXT NOT NULL`. No names, phone numbers, addresses, dates of birth, or actual PII are generated.

### account

`account_id TEXT PRIMARY KEY`; `customer_id TEXT NOT NULL REFERENCES customer`; `account_type TEXT NOT NULL CHECK IN ('Savings','Current')`; `opened_on TEXT NOT NULL`.

### branch

`branch_id TEXT PRIMARY KEY`; `branch_name TEXT NOT NULL`; `region TEXT NOT NULL CHECK IN ('North','South','East','West','Central')`.

### loan

`loan_id TEXT PRIMARY KEY`; `customer_id TEXT NOT NULL REFERENCES customer`; `account_id TEXT NOT NULL REFERENCES account`; `loan_type TEXT NOT NULL CHECK IN ('Personal','Home','Vehicle','Education','Business')`; `delinquency_flag INTEGER NOT NULL CHECK IN (0,1)`; `created_on TEXT NOT NULL`. The flag is synthetic and lacks delinquency aging semantics.

### transaction_event

`transaction_id TEXT PRIMARY KEY`; `transaction_date TEXT NOT NULL` (ISO date); `customer_id TEXT NOT NULL REFERENCES customer`; `account_id TEXT NOT NULL REFERENCES account`; `branch_id TEXT NOT NULL REFERENCES branch`; `loan_id TEXT REFERENCES loan`; `transaction_type TEXT NOT NULL CHECK IN ('credit','debit')`; `event_type TEXT NOT NULL CHECK IN ('disbursement','repayment','reversal')`; `channel TEXT NOT NULL CHECK IN ('ATM','UPI','Net Banking','Branch')`; `amount REAL NOT NULL CHECK(amount > 0)`; `status TEXT NOT NULL CHECK IN ('success','failed')`; `failure_reason TEXT NOT NULL DEFAULT ''`; `created_at TEXT NOT NULL`.

### dataset_metadata

`dataset_id TEXT PRIMARY KEY`; `schema_version TEXT NOT NULL`; `seed INTEGER NOT NULL`; `generated_at TEXT NOT NULL`; `row_count INTEGER NOT NULL CHECK(row_count >= 0)`; `source_label TEXT NOT NULL`; `quality_json TEXT NOT NULL`.

## 4. Relationships and cardinalities

- One customer to many accounts and loans; each loan belongs to one customer and one account.
- One account to many transaction events; one branch to many events.
- One loan to zero or many transaction events; non-loan account activity may carry a null loan ID.
- One dataset load metadata record per generated/imported version; a reload may replace the active sample in the MVP.

## 5. Constraints and validation

Enable `PRAGMA foreign_keys=ON` on every connection. Validate category and cross-field business rules before insert. Unique transaction ID prevents duplicate events. `event_type='disbursement'` should be credit in the synthetic generator; application metrics still require event/status rather than type alone. Failed events have failure reason or an explicit `Unspecified` value; successful events have blank failure reason. A reversal is recorded as its own event and is excluded from gross successful disbursement totals pending a netting rule.

## 6. Index strategy

- `idx_event_date` on `transaction_event(transaction_date)` for period filters.
- `idx_event_type_status_date` on `(event_type,status,transaction_date)` for disbursement calculations.
- `idx_event_loan_type` via a transaction/loan join; if category filtering performance needs it, denormalize a validated `loan_type` snapshot or rely on indexed `loan_id` FK.
- `idx_event_branch_date` on `(branch_id,transaction_date)`.
- `idx_event_channel_date` on `(channel,transaction_date)`.
- `idx_event_account_date` on `(account_id,transaction_date)`.

## 7. Transaction and lifecycle behavior

Initialize schema idempotently. Load dimensions then events in one transaction. Validate the input before delete/replace. For replacement, stage/validate first; use a transaction to delete old event/dim rows in dependency order, insert new records, write metadata, and commit. Roll back on any exception. Backups are not required for synthetic demo but document the SQLite file path and reset behavior.

## 8. Data dictionary and nullability

IDs are synthetic strings; dates are ISO-8601 date text; booleans are 0/1; amounts use decimal-like REAL for demonstration but production finance should use integer minor units or fixed decimal. Optional `loan_id` supports non-loan activity. No nullable amount/date/status fields allowed after validation. Failure reason defaults empty and is meaningful for failed transactions only.

## 9. Security and retention

Database contains synthetic identifiers only. Do not commit secrets or user uploads containing personal data. Add the runtime database file to `.gitignore` unless intentionally distributing the seeded sample database. Cloud ephemeral storage is assumed; recreate from versioned CSV/generator at startup.

## 10. Open decisions

OQ-001 governs reversals and event interpretation; OQ-004 governs currency and monetary precision; OQ-005 governs delinquency semantics; OQ-006 governs CSV import vs bundled seed behavior. These decisions must be updated in this design and RTM if resolved differently.
