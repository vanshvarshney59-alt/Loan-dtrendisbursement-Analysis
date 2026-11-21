# STEP 4 - REQUIREMENTS TRACEABILITY MATRIX (RTM)
## D17 | Loan Disbursement Trend Analysis

**Workbook companion:** `04_Requirements_Traceability_Matrix.xlsx` | **Version:** 1.0 | **Status:** Baseline for review

## Purpose and use

The Excel RTM links the original stakeholder needs and HMW framing to business requirements, product features, functional/non-functional requirements, user stories, UI screens, test cases, and implementation tasks. It is the authoritative cross-reference; IDs are persistent and are not reused after retirement.

## Identifier register

| Prefix | Meaning | Examples |
|---|---|---|
| SH | Stakeholder | SH-001 through SH-005 |
| OQ | Open question | OQ-001 through OQ-010 |
| HMW | How might we opportunity | HMW-001 through HMW-003 |
| BR | Business requirement | BR-001 through BR-012 |
| F | Product feature | F-001 through F-006 |
| FR | Functional requirement | FR-001 through FR-012 |
| NFR | Non-functional requirement | NFR-001 through NFR-008 |
| US | User story | US-001 through US-010 |
| UI | User interface screen/view | UI-01 through UI-06 |
| TC-F / TC-T | Functional / technical test case | TC-F-001 etc. / TC-T-001 etc. |
| T | Build-plan task | T-001 through T-014 |

## Relationship model

SH and OQ inform HMW; HMW maps to BR; BR maps to product features; features decompose into FR/NFR; FR/NFR are realized by US and UI; TC-F/TC-T verify requirements; T tasks implement and evidence them. Each workbook row represents a leaf requirement (FR/NFR) and includes every applicable upstream and downstream link.

## Workbook columns

`BR ID`, `HMW ID`, `SH ID`, `OQ ID`, `Feature ID`, `Requirement ID`, `Requirement Type`, `Priority`, `User Story ID`, `UI ID`, `Test Case ID`, `Task ID`, `Status`, `Evidence`, `Notes / Assumption`. The workbook includes a legend and filterable rows. Multiple links are comma-separated only where one leaf requirement genuinely has multiple sources or verifications.

## Coverage and change control

- No Must BR may remain without at least one FR/NFR and one verification case at release review.
- Every FR/NFR must link to at least one stakeholder/BR and one test case.
- A failed test opens a defect linked back to its TC and FR/NFR; a fix does not alter original IDs.
- When an assumption or OQ is resolved, update the trace row notes and dependent design/test artifacts. Preserve the original identifier and record the change history.
- The current version is proposed; mentor review and approval date remain pending.
