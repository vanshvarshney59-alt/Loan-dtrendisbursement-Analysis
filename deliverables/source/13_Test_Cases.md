# STEP 13 - TEST CASES
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Test basis:** BRD, PRD, database design, stories and UI spec | **Execution:** Step 15

## Test strategy

Test unit-level generator, validation and KPI rules; integration-level SQLite persistence and filtered queries; and application acceptance behavior. Use synthetic deterministic fixtures only. Test amount/count reconciliation, edge cases and failure paths. Tests must not depend on network access. Any defects discovered retain the requirement and test IDs; fixes are recorded without renumbering.

## Functional test cases (TC-F)

| ID | Requirement | Scenario / steps | Expected result | Priority |
|---|---|---|---|---|
| TC-F-001 | FR-001 | Generate 100 rows twice with seed 42 and compare | Frames identical; metadata states seed/schema version and synthetic source | P1 |
| TC-F-002 | FR-002 | Submit duplicate transaction ID and malformed date/amount | Duplicate/invalid rows are identified and counted; invalid data does not enter active store | P1 |
| TC-F-003 | FR-002 | Submit unknown status/event/channel and non-positive amount | Validation rejects rows with reason; no silent category coercion | P1 |
| TC-F-004 | FR-003 | Initialize DB twice, load sample twice, query counts | Schema initialization idempotent; transaction IDs remain unique; reload count reconciles | P1 |
| TC-F-005 | FR-004 | Filter by date, then loan type, branch, channel and status | Result set obeys all selected predicates; reset returns unfiltered count | P1 |
| TC-F-006 | FR-005 | Fixture with 2 successful disbursements, 1 failed disbursement, 1 repayment | Funded amount/count include only the 2 successes; failure/repayment excluded | P1 |
| TC-F-007 | FR-005 | Select data with zero disbursement attempts | Amount/count = 0; average and attempt success rate show N/A safely | P1 |
| TC-F-008 | FR-006/007 | Compare monthly and category aggregates to hand-calculated fixture | Amounts/counts match; totals reconcile to successful disbursement rows | P1 |
| TC-F-009 | FR-008 | Failed attempts with populated and blank reason | Failures separated from funded totals; blank appears as Unspecified | P2 |
| TC-F-010 | FR-009 | Apply filters and export | Export rows equal filtered preview population and contain synthetic label | P2 |
| TC-F-011 | FR-010 | Open methodology/data-quality view | Seed, row counts, event predicate, currency and delinquency caveat visible | P1 |
| TC-F-012 | FR-011 | Reload bundled sample after modified test DB | Confirmation shown; dataset restores baseline without duplicate rows | P2 |

## Technical/non-functional test cases (TC-T)

| ID | Requirement | Scenario / method | Expected result | Priority |
|---|---|---|---|---|
| TC-T-001 | NFR-001 | Time initial 12k-row dashboard load and filter query on documented dev machine | First load <=5s after DB init; query/filter recompute <=2s; record environment | P1 |
| TC-T-002 | NFR-002 | Re-run generator and metric calculations with fixed input | Output is deterministic and stable | P1 |
| TC-T-003 | NFR-003 | Inspect bundled data, generated outputs and UI copy | No real personal data; synthetic label appears in app/export | P1 |
| TC-T-004 | NFR-004 | Review amount, counts, rates, units and denominator text | Currency, event grain and KPI definitions are explicit; no ambiguous approval label | P1 |
| TC-T-005 | NFR-005 | Review repository queries and pass SQL-like values as filters | Bound parameters used; no query injection; no secrets in source/config | P1 |
| TC-T-006 | NFR-006 | Review modules and setup instructions | UI, persistence, generation and metrics responsibilities separated | P2 |
| TC-T-007 | NFR-007 | Run pytest and coverage on core modules | All tests pass; coverage target reported; gaps disclosed | P1 |
| TC-T-008 | NFR-008 | Keyboard and narrow-width visual review | Controls usable; stacked layout readable; warnings not color-only | P2 |

## Test data and environment

Use deterministic mini-fixtures plus bundled 12,000-row sample. SQLite temporary database for integration tests. Python environment from pinned requirements. No cloud or network needed for test execution. Cloud smoke test is separate and requires publication authorization and account access.

## Defect severity and exit criteria

Critical: wrong disbursement population, synthetic/PII violation, crash/data corruption. High: filter mismatch, KPI mismatch, persistence failure. Medium: incorrect labels/chart, inaccessible core interaction. Low: cosmetic issue. Release candidate requires all P1 tests pass, no critical/high open defect, P2 status documented, and reproducible commands recorded.
