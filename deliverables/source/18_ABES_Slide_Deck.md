# STEP 18 - ABES PRESENTATION / SLIDE STORYBOARD
## D17 | Loan Disbursement Trend Analysis

**Presenter:** Vansh Varshney | **Roll No.:** 2500320140161 | **Mentor:** Kalpana Dwivedi  
**Format:** 12-slide academic draft; apply official ABES deck template if supplied (OQ-010).

## Slide 1 - Title

D17 Loan Disbursement Trend Analysis; ABES Engineering College, MCA 2nd Year, Data Analyst; Banking and Finance; presenter/mentor. Include visible synthetic-data badge.

## Slide 2 - Context and problem

The assignment asks to analyze loan disbursement volumes across time and loan types. No verified bank process or real dataset was supplied. Goal is a synthetic, reproducible descriptive demonstration, not an operational finding.

## Slide 3 - Objectives and users

Create documented synthetic data, define KPIs, support interactive exploration, describe patterns, test and prepare deployment. Personas: SH-003 Branch Manager and SH-004 Risk and Operations Head; academic stakeholders SH-001, SH-002 and SH-005.

## Slide 4 - Scope and safe use

In scope: synthetic transaction events, Python/Streamlit/SQLite/Plotly, tests and submission artifacts. Out: real personal data, bank integration, lending decisions and causal claims. A persistent synthetic-data notice appears in the app.

## Slide 5 - Data model

Transaction grain; customer/account/branch/loan entities; disbursement/repayment/reversal event types; success/failed outcomes; amount/date/channel/product. Show the ER diagram. Event type prevents every credit from being interpreted as a loan disbursement.

## Slide 6 - Method and architecture

Seeded sample -> validation -> SQLite -> metrics service -> Streamlit filters -> Plotly charts/export -> pytest. Explain no external bank integration.

## Slide 7 - KPI definitions

Successful disbursed amount; successful event count; average amount; disbursement attempt success rate; transaction success rate shown separately; sample delinquency flag caveat. Include units and formulas.

## Slide 8 - Trend results

Seed 42; period 2021-01-01 to 2025-12-31; 12,000 valid rows; 4,132 successful disbursement events; INR 7,279,333,054.33 total. Highest generated month is May 2025 at INR 187,898,932.46. These are generated outputs, not observed business behavior.

## Slide 9 - Product mix

Home has the largest generated amount: INR 3,588,918,561.66 across 840 successful events. Show amount and count bars by loan type, branch and channel. Do not say one product is better or riskier based on generated volume.

## Slide 10 - Quality and testing

12,000 input/valid and 0 rejected rows; validation covers required fields, types, enums, duplicates, event direction and entity consistency. Report 14 automated tests passed, 92% core-module coverage and six headless UI views passed. Note fixed Product & channel indentation issue and one third-party AnyIO warning.

## Slide 11 - Deployment and limitations

Published on Streamlit Community Cloud: [Open the live Loan Disbursement Trend Analysis dashboard](https://loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app/). SQLite file persistence may be ephemeral. Limitations: synthetic data, no validated delinquency aging, no live bank, no production SLA or user authentication.

## Slide 12 - Recommendations and close

Validate event mapping; replace synthetic records only with authorized privacy-safe data; define delinquency aging; investigate actual failure patterns only after source validation; evaluate durable storage and access controls before production. End with thank you and viva questions.

## Speaker guidance

Target 8-10 minutes. Explain why disbursement amount is not event count, transaction success or distinct loan count. Demonstrate a filter. State limitations before interpreting peak month or product mix. The slide deck is an academic draft and must be transferred to the official ABES template if required.


