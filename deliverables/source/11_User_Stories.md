# STEP 11 - USER STORIES AND ACCEPTANCE CRITERIA
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Status:** MVP backlog | **Story format:** As a [role], I want [capability], so that [value]

| ID | User story | Acceptance criteria | Requirement links | Priority |
|---|---|---|---|---|
| US-001 | As SH-001, I want a deterministic synthetic dataset so that I can reproduce the analysis without real borrower data. | Given seed 42, repeated generation returns the same values; dataset notice and metadata identify it as synthetic. | BR-001, BR-009; FR-001 | Must |
| US-002 | As SH-001, I want invalid and duplicate records detected so that analysis is based on a documented valid population. | Invalid rows are counted/reason-coded; duplicate transaction IDs are rejected; clean row counts reconcile. | BR-006; FR-002 | Must |
| US-003 | As SH-001, I want the sample stored in SQLite so that app queries are repeatable and portable. | Schema initializes idempotently; foreign keys are enforced; reload leaves no duplicate events. | BR-009, BR-011; FR-003 | Must |
| US-004 | As SH-003, I want to filter by date, loan type, branch and channel so that I can focus on the activity relevant to my review. | Filter changes update all cards, chart, table and export; reset restores full sample. | BR-004, BR-008; FR-004 | Must |
| US-005 | As SH-003, I want monthly disbursed amount and count charts so that I can see the time pattern. | Charts use successful disbursement events only, have correct units, and reconcile to selected rows. | BR-002; FR-005, FR-006 | Must |
| US-006 | As SH-003, I want loan-type, branch and channel comparisons so that I can identify where synthetic volume is concentrated. | Categorical amount/count aggregates reconcile with filtered successful disbursements. | BR-003, BR-004; FR-007 | Must |
| US-007 | As SH-004, I want failed attempts and reasons summarized separately so that failures are not confused with funded amounts. | Failed disbursements are excluded from successful totals and missing reasons are clearly shown. | BR-005; FR-008 | Should |
| US-008 | As SH-004, I want data quality and sample delinquency notes so that I interpret indicators responsibly. | UI reports quality counts and states flag grain/limitation; no unsupported portfolio-rate label appears. | BR-006, BR-007; FR-010 | Must |
| US-009 | As SH-001, I want a filtered synthetic CSV export so that I can reproduce a displayed view outside the app. | Download respects active filters, retains schema and synthetic label in filename/metadata. | BR-009; FR-009 | Should |
| US-010 | As SH-005, I want setup, tests, deployment guidance, report and slides so that I can review and reproduce the project. | Clean setup documented; tests are runnable; Word report and PPTX are included; cloud limits are explicit. | BR-009, BR-010, BR-012; FR-012 | Must |

## Story sequencing

Foundation: US-001/002/003. Core value: US-004/005/006/008. Completion: US-007/009/010. The planned increments are elaborated in Step 14; a story is not “done” until its acceptance criteria and linked tests have evidence.

## Dependencies and edge cases

US-004 depends on data having valid dates and dimensions. US-005 depends on OQ-001 event semantics and OQ-004 currency. US-008 is constrained by OQ-005. US-010's cloud publication portion depends on OQ-009 and is limited to deployment readiness if access is unavailable.

## Definition of Ready

Story has a stable ID; stakeholder/value is clear; source requirements are traceable; data/rule dependencies and edge cases are stated; acceptance criteria are testable; UI touchpoint is mapped.

## Definition of Done

Code is reviewed, automated tests pass, no unresolved Must defect remains, UI is checked for empty/error states, requirement/test trace is updated, docs are updated, and synthetic-data disclaimers are present.
