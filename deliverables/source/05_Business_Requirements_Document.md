# STEP 5 - BUSINESS REQUIREMENTS DOCUMENT (BRD)
## D17 | Loan Disbursement Trend Analysis

**Prepared by:** Vansh Varshney | **Mentor:** Kalpana Dwivedi | **Status:** Draft for review | **Version:** 1.0

## 1. Document purpose

Define the business need, users, outcomes, boundaries, proposed business rules, risks, dependencies and acceptance approach for the academic project. Detailed software behavior is specified in the PRD; this BRD remains technology-independent except where the kickoff explicitly names the requested product direction.

## 2. Executive summary

D17 is a descriptive analytics project for synthetic Banking and Finance data. It will organize transaction-level loan records and help the intended users examine successful disbursement activity by time, loan type, branch and channel. The deliverable is a reproducible Streamlit demonstration supported by SQLite, Plotly and pytest, with an ABES project document and presentation. It is not a live bank system or a credit decision product.

## 3. Business context and rationale

The academic brief identifies loan disbursement trends as the subject and lists transaction fields such as date, amount, type, status, branch, channel and loan type. A consistent analytical view can make temporal and categorical comparisons easier to understand. Because no bank, source system, current-state workflow or validated data was supplied, the project will not claim to solve a verified operational pain point. It will demonstrate a repeatable analysis and transparently identify assumptions requiring business confirmation.

## 4. Stakeholders and interests

| ID | Stakeholder | Interest / responsibility |
|---|---|---|
| SH-001 | Vansh Varshney, learner/project owner | Scope, synthetic data, implementation, testing and submission |
| SH-002 | Kalpana Dwivedi, mentor | Academic guidance and review (approval not yet recorded) |
| SH-003 | Branch Manager | Operationally oriented trend exploration |
| SH-004 | Risk and Operations Head | Oversight-oriented transaction/outcome exploration |
| SH-005 | ABES review panel | Evaluate project document, reproducibility and presentation |

SH-003/004 are intended personas from the brief, not confirmed interview participants.

## 5. Business objectives and outcomes

1. Reproducibly create or load synthetic transaction records and record data-quality outcomes.
2. Define a transparent successful-disbursement measure and distinguish it from transaction success rate.
3. Show monthly amount/count and categorical comparisons, with filters.
4. Provide documented assumptions, KPI formulas, limitations and recommendations.
5. Demonstrate a testable application and a deploy-ready configuration without exposing credentials.
6. Submit project documentation and slide deck in the ABES-required formats when templates are available.

## 6. Scope

**In scope:** deterministic synthetic dataset; date, amount, transaction outcome, loan type, branch and channel analysis; documented transaction-level quality checks; SQLite persistence; interactive Streamlit/Plotly dashboard; pytest test suite; deployment-ready files; Word/Excel/PPTX artifacts.

**Out of scope:** real personal or bank data; banking-system integration; payment execution; borrower-level advice; credit underwriting; causal or predictive claims; production SLAs; user authentication or role-based access unless later required; publication without account/owner authorization.

## 7. Business requirements

BR-001 to BR-012 from Step 3 are incorporated without renumbering. Must requirements: BR-001, BR-002, BR-003, BR-005, BR-006, BR-007, BR-008, BR-009, BR-010, BR-011. Should requirements: BR-004 and BR-012. Priorities are proposed for the academic MVP and require mentor review.

## 8. Business rules and KPI definitions

### Proposed event rule

The generated schema will include an explicit `event_type` with `disbursement`, `repayment`, or `reversal`. A successful disbursement is `event_type='disbursement' AND status='success'`. Reversal netting is excluded from first-release headline totals unless paired reversal logic is implemented and approved; reversal activity is shown separately. This resolves the ambiguity by choosing a controlled synthetic model, not by asserting a real bank rule. The production analogue remains OQ-001.

### KPI catalogue

| KPI | Definition | Grain / unit | Caveat |
|---|---|---|---|
| Successful disbursed amount | Sum amount for successful disbursement events | INR per selected period | Excludes repayments, failed disbursements and reversals in MVP |
| Successful disbursement count | Count of successful disbursement events | Events | Not necessarily unique loans if multiple events exist |
| Average disbursement amount | Successful disbursed amount / successful disbursement count | INR/event | Null/zero-safe when no events |
| Transaction success rate | Successful transactions / all transactions | Percent | Not disbursement success rate |
| Disbursement success rate | Successful disbursement events / all disbursement attempts | Percent | Requires attempt event population; displayed only when denominator exists |
| Failed amount | Amount for failed disbursement attempts | INR | Not funded amount |
| Flagged transaction share | Flagged rows / selected transactions | Percent | Synthetic, transaction-level marker only; not portfolio delinquency |

## 9. Business process and operating concept

1. Load the bundled synthetic dataset or generate it with the documented seed.
2. Validate field types, allowed category values, uniqueness and required fields.
3. Persist validated rows and dataset metadata in SQLite.
4. User selects date range, loan type, branch, channel and status filters.
5. Application recomputes selected KPIs, monthly trends and categorical views.
6. User inspects definitions/data-quality notes and downloads the filtered synthetic records if desired.
7. Findings are interpreted descriptively and documented with limits.

## 10. Acceptance approach

Acceptance is by evidence, not assumed business sign-off: row reconciliation between selected records and aggregate measures; correct filter application; clear units and KPI definitions; deterministic seeded data; test pass evidence; a clean launch from setup instructions; and final deliverable inventory. Exact business-user acceptance thresholds remain open where the supplied context lacks a validated baseline.

## 11. Assumptions, constraints, risks, dependencies

Carry forward A-001–A-008 and OQ-001–OQ-010. Constraints: synthetic-only; academic timeline; requested tool stack; no cloud credentials/repository supplied. Key risks R-001–R-005 from Step 1 remain active. Additional risks: an amount/count mismatch from confusing loan versus event grain; timezone/date aggregation errors; and SQLite file persistence differences on cloud. Mitigate with explicit definitions, deterministic fixtures, UTC-naive date contract for synthetic data, tests, and ephemeral-cloud storage disclosure.

## 12. Governance and sign-off

This draft is prepared for mentor review. Approval fields: SH-002 review date ______; SH-001 acceptance date ______; version/change summary ______. Any changes to scope, event rule, currency, or users must update the RTM and downstream artifacts.
