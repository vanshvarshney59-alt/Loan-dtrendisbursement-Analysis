# STEP 17 - ABES PROJECT DOCUMENT
## D17 | Loan Disbursement Trend Analysis

**ABES Engineering College | MCA 2nd Year | Data Analyst Skill Track**  
**Prepared by:** Vansh Varshney | **Roll No.:** 2500320140161  
**Mentor:** Kalpana Dwivedi | **Domain:** Banking and Finance  
**Document status:** Academic submission draft | **Version:** 1.0

> The official ABES Word template was not supplied. This document uses a clean academic structure. Apply the official template before formal submission if required (OQ-010/A-008).

## Abstract

This project demonstrates a reproducible loan disbursement trend analysis workflow using synthetic transaction records. It models transaction events, validates data, stores records in SQLite, calculates descriptive KPIs, and presents interactive views in a Streamlit application. Python, pandas, NumPy, Plotly and pytest support analysis and verification. The data is synthetic and does not represent actual customers, a lender, or observed performance. The application is an academic descriptive demonstration, not a credit decision or production banking system.

## 1. Introduction

Loan disbursement activity can be described by time and product dimensions, but transaction event semantics matter: credits, repayments, failed attempts and reversals are not interchangeable. D17 explicitly models event type and outcome so successful disbursement measures are transparent. The project responds to an academic brief, not a verified real-bank process gap.

## 2. Problem and objectives

The project objective is to make a synthetic transaction dataset reproducible, derive explainable volume and amount measures, and enable interactive exploration by date, loan type, branch and channel. Outcomes include clean documented data, KPI rules, an interactive application, automated checks, deployment readiness, report and slide deck.

## 3. Scope and stakeholders

Stakeholders SH-001 through SH-005 are the learner/owner, mentor, Branch Manager persona, Risk and Operations Head persona, and ABES review panel. Scope excludes live bank connections, real customer data, loan approvals, underwriting, causal claims and a durable multi-user production service.

## 4. Requirements and traceability

Business requirements BR-001..BR-012; features F-001..F-006; functional requirements FR-001..FR-012; non-functional requirements NFR-001..NFR-008; stories US-001..US-010; screens UI-01..UI-06; test cases TC-F and TC-T; build tasks T-001..T-014. The RTM workbook links requirements to evidence. Full identifiers and acceptance criteria remain in Steps 3-14 artifacts.

## 5. Methodology

1. Generate deterministic, fictitious entities and transaction events using a documented seed.
2. Validate fields, dates, event/outcome values, amounts, identifiers and referential integrity.
3. Load normalized records to SQLite with transaction boundaries and metadata.
4. Apply the same filters to metrics, charts, table and exports.
5. Define successful disbursement as `event_type='disbursement' AND status='success'`; show repayments, failed attempts and reversals separately.
6. Aggregate monthly amount/count and compare by loan type, branch and channel; keep transaction success rate separate from disbursement attempt success.
7. Verify business rules/persistence with pytest and document deployment limits.

## 6. Data and KPI definitions

Dataset grain is one transaction event. It includes transaction/customer/account/branch/loan IDs, event date/type, channel, amount, status/failure reason, loan type and a sample delinquency flag. Successful disbursed amount is the sum of successful disbursement event amounts. Event count is not necessarily unique loan count. Average event amount is amount/count. Transaction success rate uses all event types. Attempt success rate uses disbursement attempts only. Sample delinquency flags are not calibrated or tied to days-past-due.

## 7. System design

Architecture: synthetic generator and validation -> SQLite normalized schema -> metrics service -> Streamlit app -> Plotly charts and filtered CSV. Tables: customer, account, branch, loan, transaction_event, dataset_metadata. Bound parameters, foreign-key enforcement, idempotent schema initialization, transactional reload and tests support consistency. Tailwind-compatible CSS tokens are bundled locally with Streamlit native controls.

## 8. Implementation and verification

The final run used seed 42 and 12,000 generated transactions; all 12,000 validated, with zero rejected. The automated suite completed **14 passed tests**. Core `loan_app` modules recorded **92% coverage**. Streamlit headless smoke rendered all six views with no app exceptions. A Product & channel indentation issue and a test expectation issue were fixed; `use_container_width` deprecation was removed. One third-party AnyIO/Pytest deprecation warning remains. Evidence: `outputs/test_results.txt`, `outputs/test_coverage.txt`, `outputs/build_smoke.json`, `outputs/qa_notes.md`.

## 9. Results and discussion

Period: 2021-01-01 through 2025-12-31. The generated sample contains **4,132 successful disbursement events** totaling **INR 7,279,333,054.33**. Transaction success rate is **97.79%** and disbursement-attempt success rate is **96.41%**. Home loans have the largest generated amount (**INR 3,588,918,561.66**, 840 successful events). May 2025 has the largest generated monthly amount (**INR 187,898,932.46**).

These are outputs of the synthetic generator; they are not real-world business findings. The generated pattern is not evidence that Home loans are more valuable or that May is a real seasonal peak. Filtered totals reconcile to successful disbursement event rows. See `outputs/insight_report.md` and summary CSV files.

## 10. Deployment

The application is published on Streamlit Community Cloud: [Open the live Loan Disbursement Trend Analysis dashboard](https://loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app/). Deployment configuration and operating notes are in Step 16. Streamlit Community Cloud deployment selects a GitHub repository, branch and entrypoint, with dependencies declared in the project; see the official [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). Hosted SQLite is treated as ephemeral and sample reload behavior is documented.

## 11. Limitations and future work

Synthetic data; event mapping is not validated against a bank; no causal analysis; no time-varying loan status; no days-past-due; sample flags are not risk model output; SQLite is not multi-writer; cloud persistence/availability are not guaranteed; no user authentication. Future work with authorization could include validated source mapping, dated loan status, access control, managed persistence and review by domain owners.

## 12. Conclusion

D17 provides a transparent academic demonstration of transaction-grain loan disbursement analytics. Its contribution is reproducibility and disciplined definitions, not claims about lender performance. Final academic submission requires applying the official ABES template if available and mentor review. The live dashboard URL is listed in Section 10.

## References and appendices

- Streamlit Community Cloud deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Streamlit app dependency setup: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Appendices: RTM, data dictionary, ER model, test cases/results, UI views, deployment checklist and slide deck.


