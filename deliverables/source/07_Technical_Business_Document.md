# STEP 7 - TECHNICAL / BUSINESS DESIGN (TBD)
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Status:** Proposed MVP architecture | **Author:** SH-001

## 1. Purpose and architecture principles

Translate the approved-intent requirements into a small, auditable academic solution without adding production-bank complexity. Use clear module boundaries, synthetic-only data, deterministic computation, visible KPI semantics, local persistence, and minimal external dependencies. Keep business definitions out of chart code and never silently interpret repayment or reversal records as disbursements.

## 2. Proposed logical architecture

`Synthetic CSV / seeded generator -> validation & normalization -> SQLite repository -> metric/query service -> Streamlit presentation -> Plotly charts / CSV export`

Cross-cutting concerns: structured data-quality summary, synthetic-data notice, error/empty states, pytest tests, configuration from environment variables, Git history and deployment guide. No external bank API is present.

## 3. Component responsibilities

| Component | Responsibilities | Excludes |
|---|---|---|
| Data generator | Generate deterministic synthetic customers, accounts, branches, loans and transaction events | Real customer profiles, market calibration claims |
| Validation/cleaning | Parse types, enforce required columns and enum/value ranges, detect duplicates and invalid amount/date/status/event combinations | Silently guessing business-event meaning |
| SQLite repository | Create schema, perform transactional load, provide filtered query methods and metadata | UI formatting or KPI interpretation |
| Metrics service | Apply canonical event rules, calculate safe denominators, group monthly and categorical totals | Direct database writes or user interaction |
| Streamlit app | Navigation, filters, notices, KPI cards, chart/table rendering, download | SQL assembly inside UI, unstated business decisions |
| Test suite | Validate deterministic generation, rules, metrics, filters, persistence and edge cases | Replace mentor/business approval |

## 4. Data flow and transaction boundaries

1. Create or load synthetic data with schema version and seed metadata.
2. Validate the complete frame before database replacement; collect rejected-row counts and reasons.
3. Begin SQLite transaction; upsert dimensions in dependency order; replace transaction fact rows; write load metadata; commit. On failure, rollback so prior valid sample remains intact.
4. UI gathers filter values; query/service receives typed parameters, not SQL fragments.
5. Service applies one shared event predicate and computes KPIs from the exact filtered population.
6. UI renders metrics/charts and notes sample grain/limitations; CSV download contains only synthetic filtered records.

## 5. Proposed business logic contract

- `successful_disbursement := event_type == 'disbursement' AND status == 'success'`.
- `disbursement_attempt := event_type == 'disbursement'`.
- `transaction_success_rate := count(status='success') / count(all selected transactions)`.
- `disbursement_success_rate := successful disbursement attempts / all disbursement attempts`; show N/A with zero denominator.
- `disbursed_amount := sum(amount for successful_disbursement)`; display failed attempts and reversals separately.
- `delinquency_flag` belongs to synthetic loan dimension in the designed schema; current rate is a loan-level sample flag share only if distinct loans are used. Do not infer days past due.
- Dates are stored in ISO 8601 date form; month aggregation follows the selected business calendar. Synthetic data uses local date values with no timezone conversion.

## 6. Error handling and observability

Validation errors return actionable field-level messages and a quality report. Database errors show a safe user message and log diagnostic details without secrets. Empty filters produce a no-data state. Missing database triggers initialization/seed. A failed import never leaves a partially loaded dataset. Application title/help text identifies synthetic source, seed/version, and load time.

## 7. Security and privacy

Only deterministic fictitious IDs are generated. No credentials belong in code or committed config. Any future secret is supplied through Streamlit secrets/environment variables. SQL uses bound parameters. CSV uploads, if enabled, are size-limited, schema-validated and processed in memory before transactionally replacing synthetic data; MVP may omit upload to keep synthetic-only guarantees simple. Cloud data persistence is assumed ephemeral unless the hosting platform configuration explicitly demonstrates otherwise.

## 8. Deployment topology

Local development: Python virtual environment, Streamlit server, SQLite file under a configurable data directory, bundled sample. Cloud proposal: GitHub repository connected to Streamlit Community Cloud, pinned dependencies, app entrypoint, no secrets required for synthetic sample. The SQLite file is not treated as durable cloud storage; reload sample on boot or provide an explicitly documented persistence service only if approved.

## 9. Design decisions and tradeoffs

| Decision | Choice | Reason / consequence |
|---|---|---|
| Application | Streamlit single-process MVP | Fast academic delivery; limited multi-user concurrency |
| Persistence | SQLite | Portable, zero-service local setup; hosted file durability is not guaranteed |
| Data grain | One row per transaction event | Supports event/outcome analysis; distinct loans require explicit loan identifiers |
| Event taxonomy | Disbursement / repayment / reversal | Prevents credit/debit alone from determining business meaning |
| Analytics | Descriptive only | Avoid unsupported causal/risk conclusions |
| Visuals | Plotly | Interactive time/category exploration |

## 10. Technical risks and mitigations

Timezone mismatch: synthetic date-only contract and tests. Double counting: unique transaction key plus shared event rule. SQLite lock: short transactions and read-only query patterns. Cloud reset: reload-on-start and clear persistence notice. CSS dependency: bundle a small Tailwind-compatible stylesheet or use Streamlit theme if CDN reliability is unacceptable; revisit OQ-008. Package drift: pin tested compatible versions. Test coverage target is NFR-007.

## 11. Interfaces

Internal interface contracts: `generate_dataset(seed, rows) -> DataFrame`; `validate_and_normalize(frame) -> (valid_frame, quality_report)`; `initialize_database(path)`; `replace_dataset(path, frame, metadata)`; `get_filtered_transactions(filters)`; `compute_kpis(frame)`; `aggregate_monthly(frame)`; `aggregate_dimensions(frame, dimension)`; Streamlit entrypoint `app.py`.

## 12. Decisions pending

OQ-004 currency confirmation; OQ-005 delinquency definition; OQ-008 styling implementation; OQ-009 cloud account/repository; OQ-010 ABES formats remain pending. These do not block a clearly labeled synthetic MVP but constrain production claims and publication.
