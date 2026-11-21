# STEP 1 - PROJECT UNDERSTANDING
## Loan Disbursement Trend Analysis

**Project code:** D17 | **Domain:** Banking and Finance | **Track:** Data Analyst  
**Learner:** Vansh Varshney | **Roll No.:** 2500320140161 | MCA 2nd Year, ABES Engineering College  
**Mentor:** Kalpana Dwivedi | **Product direction:** Python + Streamlit application  
**Document status:** Step 1 baseline | **Version:** 1.0 | **Date:** 21 November 2026

## 1. Purpose of this step

This document records a shared, initial understanding of the project before requirements are elicited or solution details are finalized. It establishes the business context, intended users, project objectives, scope boundaries, known constraints, assumptions, and questions that need resolution in later steps. This is a planning baseline, not an approved BRD or technical design.

## 2. Executive project understanding

D17 is an academic Data Analyst project in the Banking and Finance domain. The project will analyze synthetic loan transaction data to describe disbursement trends over time and across loan types, and to present the results through an interactive analytical product.

The proposed product is a Python and Streamlit application. The stated technology direction includes Python-based EDA and statistics, Plotly visualizations, SQLite storage, a Tailwind-styled interface, automated tests with pytest, and deployment to Streamlit Community Cloud. The exact implementation, data model, business rules, and hosting procedure are to be defined in their designated later steps.

The final academic submission is expected to include an ABES project document based on the required Word template and an ABES slide deck. This step does not invent or finalize the template or presentation requirements.

## 3. Business context and problem statement

Loan disbursements are financial events that can be examined by date, loan type, channel, branch, and transaction outcome. A business user needs a clear way to understand how successful disbursement volumes vary across these dimensions and to inspect the underlying trends without manually compiling transaction records.

At kickoff, the exact operational problem, existing reporting process, decision cadence, and accepted definition of a disbursement have not been supplied. The project therefore begins with a descriptive-analysis intent: organize a synthetic transaction dataset, calculate transparent summary measures, and visualize patterns for discussion. It must not present synthetic findings as evidence about a real lender.

## 4. Intended users and stakeholders

### Primary business users

- **SH-003 Branch Manager:** intended to review disbursement patterns by time, branch, loan type, and channel for operational monitoring.
- **SH-004 Risk and Operations Head:** intended to review portfolio transaction patterns and exception indicators for oversight and follow-up.

### Project and academic stakeholders

- **SH-001 Learner and project owner:** Vansh Varshney, Roll No. 2500320140161, MCA 2nd Year Data Analyst, ABES Engineering College.
- **SH-002 Academic mentor:** Kalpana Dwivedi.
- **SH-005 Academic review panel:** ABES Engineering College project submission; exact review and acceptance process remains to be confirmed.

## 5. Project objectives

- Create a documented, synthetic, transaction-level dataset suitable for repeatable analysis.
- Clean and profile the records, documenting data-quality handling and exclusions.
- Describe loan disbursement amount and count trends over time and by loan type, with relevant branch and channel views where supported by the data.
- Define and present understandable KPIs, filters, and interactive visualizations.
- Provide reproducible analysis, automated quality checks, a usable Streamlit product, and deployment instructions.
- Prepare the required academic project document and slide deck with findings, limitations, and recommendations.

## 6. Initial scope boundary

### In scope

- Synthetic data only; no real or identifiable customer information.
- Transaction fields suggested in the assignment: transaction ID/date, customer ID, account ID/type, branch ID, transaction type, channel, amount, status, failure reason, loan ID/type, and delinquency flag.
- Descriptive analysis of disbursement trends and transaction outcomes; a clear definition of which transactions count as a disbursement must be agreed before implementation.
- Python analytical workflow, SQLite-backed application direction, Streamlit user interface, Plotly charts, pytest checks, and Streamlit Community Cloud deployment direction.
- Academic documentation and presentation deliverables.

### Out of scope unless later approved

- Production banking integration, live customer data, account actions, payment processing, or operational lending decisions.
- Credit scoring, loan approval recommendations, causal claims, or financial advice.
- Claims that synthetic data represents actual market, customer, branch, or portfolio performance.
- Any deployment requiring credentials, private integrations, or a real institution account before access and authorization are established.

## 7. Initial data understanding

The supplied assignment suggests a transaction-grain dataset. Candidate fields are `transaction_id`, `transaction_date`, `customer_id`, `account_id`, `account_type`, `branch_id`, `transaction_type` (credit/debit), `channel` (ATM/UPI/Net Banking/Branch), `amount`, `status` (success/failed), `failure_reason`, `loan_id`, `loan_type`, and `delinquency_flag`. These are suggested fields rather than a finalized schema.

The phrase loan disbursement trend suggests that amount and transaction date are central, with loan type as a key breakdown. A transaction may also represent a repayment, reversal, or another event. The schema and business definition must distinguish these cases before KPIs are committed.

## 8. Product and technology direction

- Python for analysis and application logic.
- Streamlit as the interactive application framework.
- pandas and NumPy for data handling and analysis; Plotly for interactive charts.
- SQLite as the local project data store, subject to the database design step.
- Tailwind UI styling direction; integration approach and compatibility need to be confirmed in the UI step.
- pytest for automated tests and Streamlit Community Cloud as the proposed hosting platform.
- Git for version history and tagged release; remote repository and release procedure are not yet specified.

## 9. Success indicators for project understanding

At the end of the project, a reviewer should be able to inspect documented business requirements and traceability; identify the synthetic data source and cleaning rules; reproduce the analysis; understand each KPI and its limitation; use the interactive filters and charts; run the automated test suite; and follow the deployment and academic submission instructions. Numerical acceptance thresholds and test coverage targets are intentionally deferred to requirements and test planning steps.

## 10. Assumptions

- **A-001:** The supplied identity details and mentor name are correct as written and should appear in project materials.
- **A-002:** Synthetic records will be generated for this academic project; no real personal data will be used.
- **A-003:** The listed primary users, Branch Manager and Risk and Operations Head, are intended analytical audiences and not confirmed operational approvers.
- **A-004:** Streamlit, SQLite, Plotly, pytest, and Streamlit Community Cloud are the requested solution direction, subject to detailed feasibility and requirement definition.
- **A-005:** The application is for descriptive learning and demonstration, not live banking operations or automated credit decisions.
- **A-006:** INR is a reasonable initial display currency given the academic and institution context in India; confirm this before finalizing dataset fields and visual labels.
- **A-007:** The provided field list is a candidate dataset schema; required versus optional fields and allowed values remain open.
- **A-008:** The ABES Word template and slide format will be supplied or identified before the final documentation and presentation steps.

## 11. Open questions to carry forward

- **OQ-001:** What exact business event qualifies as a loan disbursement: successful credit transaction, loan booking event, or another source-system event? How should reversals and duplicate postings be treated?
- **OQ-002:** What analysis period, record volume, and date granularity should the synthetic dataset represent?
- **OQ-003:** Which loan types, channel values, transaction outcomes, branch dimensions, and failure reasons are required?
- **OQ-004:** What currency and amount precision should the dataset and dashboard use? Is INR confirmed?
- **OQ-005:** What is the authoritative meaning of `delinquency_flag`, its grain, and any aging threshold? Should the project include it in KPIs or only data profiling?
- **OQ-006:** Should the application load CSV files, use only the SQLite database, or support both? Who is expected to maintain or refresh the synthetic dataset?
- **OQ-007:** Which filters, KPI definitions, and access patterns are essential for the Branch Manager and Risk and Operations Head?
- **OQ-008:** Is Tailwind required as a specific CSS framework, and what Streamlit-compatible implementation approach is acceptable?
- **OQ-009:** Is a Streamlit Community Cloud account/repository available, and what branch, secret-management, and publication expectations apply?
- **OQ-010:** Which ABES Word template, slide count/format, citation rules, and submission deadline govern the final deliverables?

## 12. Risks and dependencies

- **R-001:** Ambiguous disbursement semantics can produce misleading metrics. Mitigation: resolve OQ-001 and document the rule before analysis.
- **R-002:** Synthetic data may look realistic and be misread as observed banking performance. Mitigation: label it visibly in the UI, reports, and slides.
- **R-003:** Suggested delinquency and transaction fields may not support valid loan-level risk measures. Mitigation: define grain and explicitly limit interpretations.
- **R-004:** Streamlit Community Cloud access, repository permissions, and secrets handling may affect deployment. Mitigation: confirm prerequisites before deployment.
- **R-005:** ABES templates and formatting rules are not yet available. Mitigation: obtain them before final-document production.

## 13. Step boundary and next work

This Step 1 baseline does not define HMW statements, detailed business requirements, functional or non-functional requirements, database entities, user stories, UI screens, test cases, code, or deployment configuration. Those are reserved for their numbered steps. Any change to this baseline should be recorded and traced rather than silently changing identifiers or definitions. Stakeholder identifiers SH-001 through SH-005 are established here for reuse throughout the project.

Prepared as the Step 1 project-understanding deliverable for D17. End of Step 1.
