# STEP 14 - BUILD PLAN AND TASK IDs
## D17 | Loan Disbursement Trend Analysis

**Plan:** 3 sprints / 40 suggested hours | **Owner:** SH-001 | **Version:** 1.0

## Sprint plan

| Sprint | Hours (suggested) | Goal | Exit evidence |
|---|---:|---|---|
| Sprint 1 - Define and model | 12 | Requirements, RTM, database, ER, deterministic synthetic data | Approved baseline or recorded assumptions; schema/data checks; sample dataset |
| Sprint 2 - Build and validate | 18 | Stories, Streamlit UI, metrics, persistence, tests | MVP runs locally; P1 functional/technical tests pass; defect log |
| Sprint 3 - Release and submit | 10 | Deployment readiness, report, ABES document, deck, tagged release | Reproduction guide, final files, local tagged commit; cloud limitation recorded if access unavailable |

## Task backlog (stable T IDs)

| ID | Work item | Dependencies | Output / linked requirements | Estimate |
|---|---|---|---|---:|
| T-001 | Confirm assumptions and baseline IDs | Steps 1-4 | RTM; BR-001..012 | 1h |
| T-002 | Finalize synthetic schema and event rule | T-001 | FR-001/002; DB/ER | 1h |
| T-003 | Implement deterministic entity/event generator | T-002 | US-001; TC-F-001 | 2h |
| T-004 | Implement cleaning and quality report | T-002/T-003 | US-002; TC-F-002/003 | 2h |
| T-005 | Create SQLite schema/repository and transactional loader | T-002..004 | US-003; TC-F-004 | 3h |
| T-006 | Implement canonical metrics and aggregations | T-002..005 | US-005/006; TC-F-006..008 | 3h |
| T-007 | Build Tailwind-token styling and Streamlit shell | T-001 | UI-01..06; FR-012 | 2h |
| T-008 | Implement filters, KPI cards and monthly charts | T-005..007 | US-004/005; TC-F-005 | 3h |
| T-009 | Implement categorical/outcome/quality views | T-008 | US-006/007/008; FR-007/008/010 | 3h |
| T-010 | Implement preview, export, reload behavior | T-008/T-009 | US-009; FR-009/011 | 2h |
| T-011 | Build unit/integration tests and fix defects | T-003..010 | TC-F/TC-T; NFR-007 | 4h |
| T-012 | Performance/accessibility review and fixes | T-008..011 | NFR-001/004/008 | 2h |
| T-013 | Prepare Cloud config, requirements and deployment guide | T-011/T-012 | FR-012; BR-012 | 2h |
| T-014 | Finalize ABES document, slide deck and tagged release | All | BR-010; US-010 | 2h |

**Total:** T-001 through T-014 estimate 32 hours. The remaining 8 hours are reserved for mentor feedback, requirement clarification, report/deck review, presentation rehearsal, and contingency, giving the suggested 40-hour project envelope. Estimates are planning estimates, not timesheet evidence.

## Sequencing and gates

Gate 1: event rule and schema stable before generating final sample. Gate 2: metrics tests pass before UI sign-off. Gate 3: P1 test cases pass before deployment readiness. Gate 4: final doc/deck reconcile to implemented behavior. No task may silently change requirement IDs; update RTM links and retain history.

## Risks, buffers and change handling

Tailwind integration, Cloud account access and ABES template availability may consume time; use local bundled styling and deployment-readiness documentation as fallback, while clearly recording the limitation. If an OQ resolution changes scope, estimate impact and update this plan without renumbering completed tasks. T-014 includes actual Git tag only after final artifacts are committed.
