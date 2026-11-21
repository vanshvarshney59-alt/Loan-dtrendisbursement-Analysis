# STEP 3 - NEEDS ANALYSIS AND BUSINESS REQUIREMENTS
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Status:** Draft for mentor review | **Business domain:** Banking and Finance

## 1. Need analysis method

Inputs: Step 1 project understanding and open questions OQ-001–OQ-010; Step 2 HMW-001–HMW-003. The user groups are academic and operational proxies rather than interviewed production stakeholders. Requirements below are proposed for the academic demonstration and should be validated before claiming operational suitability.

## 2. Stakeholder needs

| Stakeholder | Need | Expected value | Evidence / limitation |
|---|---|---|---|
| SH-001 Project owner | Reproduce data generation, cleaning, KPI calculation and presentation | Auditable project workflow and reliable viva demonstration | Synthetic records only; academic acceptance criteria pending |
| SH-002 Mentor | Review traceable scope, assumptions, design, implementation and evidence | Assessable and coherent project | Mentor sign-off not yet received |
| SH-003 Branch Manager | Compare disbursement trends across time, branches, loan types and channels | Identify patterns for follow-up discussion | Not an operational decision tool |
| SH-004 Risk & Operations Head | View transaction outcomes and descriptive delinquency flag distribution | Surface data questions and potential exception areas | No validated loan-level delinquency semantics |
| SH-005 Review panel | Inspect clear methodology, limitations, tests, document and presentation | Reproducible academic submission | ABES template/rubric remains to be supplied |

## 3. Business requirements

| ID | Business requirement | Priority | Source | Acceptance outcome |
|---|---|---|---|---|
| BR-001 | The project shall analyze synthetic transaction-level loan data only and label it as synthetic in user-facing and submission materials. | Must | A-002, A-005; HMW-003 | Dataset, application, reports and presentation identify synthetic data; no real borrower data is included. |
| BR-002 | The project shall present disbursement activity over time using the agreed disbursement event and event date. | Must | HMW-001; OQ-001, OQ-002 | KPI definition is documented and a time series displays amount and transaction count for selected dates. |
| BR-003 | The project shall support comparison by loan type. | Must | HMW-001 | A user can compare totals and counts by loan type; totals reconcile to the selected successful disbursement population. |
| BR-004 | The project shall support exploratory comparison by branch and channel. | Should | HMW-002; OQ-003, OQ-007 | Branch and channel summaries are filterable and show selected-population totals. |
| BR-005 | The project shall distinguish successful from failed transaction activity and provide failure-reason summaries when present. | Must | HMW-002; suggested schema | Outcome counts/rates are clearly labeled and do not conflate transaction success with disbursement rate. |
| BR-006 | Data quality treatment and exclusions shall be documented and reproducible. | Must | HMW-003 | Input, cleaned and excluded row counts and cleaning rules are available. |
| BR-007 | KPI definitions shall be visible and unambiguous. | Must | HMW-001, HMW-003 | Each displayed KPI has a name, unit, grain and numerator/denominator or aggregation rule. |
| BR-008 | The solution shall provide an interactive dashboard usable by SH-003 and SH-004. | Must | HMW-002 | Date, loan type, branch and channel filters update the relevant metrics and visualizations. |
| BR-009 | The analysis shall be reproducible from versioned project artifacts. | Must | HMW-003 | Instructions generate/load data, initialize storage, run tests and launch the application from a clean checkout. |
| BR-010 | The final submission shall include the ABES project document and presentation, with assumptions and limitations. | Must | SH-005; OQ-010 | Both deliverables are present and clearly identify pending template adaptation if the official template is unavailable. |
| BR-011 | The application shall use Python, Streamlit, SQLite, Plotly and pytest as the requested solution direction. | Must | Project kickoff | Runtime dependencies, local database, interactive visualization and automated tests are included. |
| BR-012 | The project shall be prepared for Streamlit Community Cloud deployment without exposing secrets. | Should | Project kickoff; OQ-009 | Deployment instructions/configuration are included; publication occurs only when account/repository access is available. |

## 4. Business process (current / target)

**Current academic baseline:** no verified bank reporting workflow or source system was supplied. Do not assert that a real process is manual or deficient. **Target project flow:** generate deterministic synthetic transactions -> validate and normalize -> load to SQLite -> filter and aggregate in the application -> show documented KPIs/charts -> export/inspect artifacts -> present limitations and recommendations.

## 5. Business rules proposed for requirement elaboration

- A successful disbursement is initially defined as a record marked `event_type=disbursement` and `status=success`; a credit-only proxy may be used only if the dataset event field is unavailable and the assumption is visibly stated.
- Failed, reversed, repayment and non-disbursement credits must not inflate successful disbursement amount/count.
- Amounts are non-negative numeric values; valid currency is assumed INR pending OQ-004.
- Transaction grain is not loan grain. Loan counts must use distinct loan IDs only when event semantics and duplicate behavior are clear.
- Synthetic delinquency flags are descriptive placeholders, not validated arrears or portfolio quality measures.

## 6. Assumptions and open questions

Carry forward A-001–A-008 and OQ-001–OQ-010. BR-002 acceptance depends on resolving OQ-001/002. Currency display depends on OQ-004. Delinquency KPI inclusion depends on OQ-005. Filter acceptance priorities depend on OQ-007. Cloud publishing depends on OQ-009. Template conformance depends on OQ-010.

## 7. Approval status

All BRs are proposed academic requirements, not validated production requirements. Record mentor review, date, changes, and version at the next approval checkpoint. Do not silently renumber BR IDs; retire an ID with rationale if a requirement is withdrawn.
