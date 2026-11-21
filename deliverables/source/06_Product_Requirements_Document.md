# STEP 6 - PRODUCT REQUIREMENTS DOCUMENT (PRD)
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Status:** MVP baseline for review | **Product owner:** SH-001

## 1. Product vision

Deliver a safe, transparent, reproducible analytics application that lets an academic reviewer and intended business personas explore synthetic loan disbursement events without mistaking demonstration measures for real operational evidence.

## 2. Target users and use cases

- SH-003 Branch Manager persona: filter and compare event amounts/counts for branch/channel/loan type over time.
- SH-004 Risk & Operations Head persona: inspect transaction outcomes, failed reasons, and sample flag distributions.
- SH-001/SH-005: validate definitions, dataset quality, reproducibility, test evidence and limitations.

## 3. Product features

| Feature ID | Feature | Priority | Source |
|---|---|---|---|
| F-001 | Synthetic data load, validation and SQLite persistence | Must | BR-001, BR-006, BR-009 |
| F-002 | KPI calculation and definitions | Must | BR-002, BR-005, BR-007 |
| F-003 | Time-series and loan-type trend exploration | Must | BR-002, BR-003 |
| F-004 | Branch/channel/date/status filtering and drilldown | Must | BR-004, BR-008 |
| F-005 | Data quality, failure and limitation transparency | Must | BR-001, BR-005, BR-006 |
| F-006 | Reproducible tests, documentation and deployment readiness | Must | BR-009–BR-012 |

## 4. Functional requirements

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-001 | Application shall load bundled synthetic CSV records and support deterministic generation via seed. | Must | Default sample loads; identical seed and row count produce the same records. |
| FR-002 | Application shall validate required fields, types, allowed status/event values, positive amount, date parseability and unique transaction ID. | Must | Invalid rows are rejected or excluded with a visible count/reason; no silent coercion to valid business events. |
| FR-003 | Application shall create/update the SQLite schema and persist transactions plus dataset metadata. | Must | Initialization is idempotent; repeated load replaces or versions the demo dataset without duplicate transaction IDs. |
| FR-004 | Application shall allow date range, loan type, branch, channel and outcome filters. | Must | Each selected filter is reflected in all downstream KPIs/charts/table. |
| FR-005 | Application shall calculate disbursed amount, event count, average amount, failed amount, transaction success rate and eligible disbursement success rate. | Must | Values reconcile to filtered row-level definitions; undefined denominators render as N/A, not infinity. |
| FR-006 | Application shall provide monthly disbursed amount and event-count trend charts. | Must | Axis titles specify month and INR/events; zero-event months are represented consistently. |
| FR-007 | Application shall compare successful disbursement amount/count by loan type, branch and channel. | Must | Category totals reconcile to selected eligible disbursement rows. |
| FR-008 | Application shall summarize failed disbursement attempts and failure reasons. | Should | Failed rows are separated from funded totals; missing reason is shown as unspecified. |
| FR-009 | Application shall show bounded transaction-level data preview and allow CSV download of filtered synthetic rows. | Should | Preview is capped; export includes active filter selection and synthetic notice. |
| FR-010 | Application shall expose data-quality counts, schema, KPI definitions and synthetic-data notice. | Must | User can find this information in app without source-code inspection. |
| FR-011 | Application shall provide an explicit reset/reload sample action and report source/seed. | Should | Action provides confirmation; dataset metadata updates. |
| FR-012 | Application shall provide reproducible startup and deployment instructions. | Must | Clean environment commands documented; secrets are not stored in source. |

## 5. Non-functional requirements

| ID | Requirement | Verification |
|---|---|---|
| NFR-001 | For the bundled dataset of 12,000 rows on a typical student laptop, first dashboard load after database initialization should complete within 5 seconds; filter recomputation should complete within 2 seconds. | Timed manual run; disclose machine and cache status. |
| NFR-002 | Same seed/version must produce identical synthetic rows; app calculations must be deterministic for same input and filters. | Unit tests compare generated frames and metrics. |
| NFR-003 | The application must never require real customer data or collect personal identifiers beyond clearly synthetic IDs. | Dataset inspection and source review. |
| NFR-004 | All monetary values show currency code/label; counts, percentages, event grain and denominators are explained. | UI/document review and tests for formatting edge cases. |
| NFR-005 | Inputs are validated and SQL uses parameterized queries or pandas SQLite APIs; uploaded file paths are not interpolated into SQL. | Code review and tests. |
| NFR-006 | Project modules have clear separation between data, persistence, metrics and UI; setup is documented. | Repository review. |
| NFR-007 | Automated tests cover critical metrics, data validation, database persistence and filter reconciliation; target line coverage >=80% for core logic if coverage tooling is available. | pytest plus coverage report; target is provisional until baseline review. |
| NFR-008 | UI labels, color contrast, keyboard-accessible native controls, chart titles and empty-state messages support basic accessibility. | Manual keyboard/readability checklist. |

## 6. UX requirements and content rules

Use a clear title and persistent synthetic-data banner. Place filter controls before KPI cards and charts. Display definitions near the dashboard (expandable or separate Methodology view). Charts use consistent INR formatting; avoid red/green as the only encoding. Empty states explain which filters caused no data. Do not call transaction success “loan approval” or a sample delinquency flag “portfolio delinquency.”

## 7. Data and integration requirements

Input is the versioned synthetic CSV generated by Step 10. SQLite is the local analytical cache/source. No external API or bank connection is in scope. Store generation seed/version and load timestamp. Cloud deployment must document persistence limitations; bundled synthetic data can be reloaded if the hosted filesystem is reset.

## 8. Release and MVP acceptance

MVP includes F-001–F-006 and FR-001–FR-007, FR-010, FR-012; should features may be included if schedule permits. Release readiness requires Must BR traceability, tests passing, no unlabelled synthetic results, clean setup, UI review, and mentor feedback opportunity. Cloud publication remains dependent on repository/account access and approval.

## 9. Open decisions

OQ-001 is resolved for the synthetic MVP by adding explicit `event_type`; real-world semantics remain unresolved. A-006 assumes INR. OQ-005 constrains delinquency interpretation. OQ-008 determines whether Tailwind is bundled CSS or Streamlit-native styling with Tailwind utility tokens. OQ-009 is an external deployment dependency. OQ-010 remains for template finalization.
