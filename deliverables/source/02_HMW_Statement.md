# STEP 2 - HOW MIGHT WE (HMW) STATEMENTS
## D17 | Loan Disbursement Trend Analysis

**Owner:** Vansh Varshney | **Mentor:** Kalpana Dwivedi | **Version:** 1.0 | **Status:** Proposed design framing

## Purpose

Convert the Step 1 understanding into user-centered opportunity statements. HMW statements frame a solvable problem while avoiding premature commitment to features or implementation. They do not replace elicitation or establish approval.

## Stakeholder and context recap

- **SH-001:** Learner/project owner responsible for analysis, implementation, and submission.
- **SH-002:** Academic mentor guiding scope and academic quality.
- **SH-003:** Branch Manager, intended operational audience.
- **SH-004:** Risk and Operations Head, intended oversight audience.
- **SH-005:** ABES academic review panel.

## HMW statements

### HMW-001 - Make time trends understandable

How might we help SH-003 and SH-004 understand changes in successful loan disbursement volume over time and by loan type, while making the metric definition and time period clear?

**Design opportunity:** provide clear time-based amount and count views, loan-type breakdowns, explicit definitions, and a selectable period. **Evidence needed:** agreement on what constitutes a booked/disbursed loan, event date, reversals, and reporting grain (OQ-001, OQ-002).

### HMW-002 - Support useful operational exploration

How might we let SH-003 and SH-004 explore synthetic disbursement activity by branch, channel, outcome, and loan type without forcing them to inspect raw records manually?

**Design opportunity:** contextual filters, drillable aggregate views, transparent failed-transaction summaries, and accessible labels. **Evidence needed:** user priority and approved filter set (OQ-003, OQ-007).

### HMW-003 - Make insights reproducible and trustworthy

How might we help SH-001 and SH-005 reproduce the analysis and distinguish demonstration data from real banking evidence?

**Design opportunity:** deterministic synthetic data, documented cleaning and KPI definitions, an audit-friendly local store, automated tests, and prominent synthetic-data notices. **Evidence needed:** acceptable validation and academic submission criteria (OQ-006, OQ-010).

## Prioritization

| ID | User value | Feasibility in academic scope | Priority | Rationale |
|---|---|---|---|---|
| HMW-001 | High | High | P1 | Central project question and core dashboard story |
| HMW-002 | High | Medium | P1 | Enables business exploration; depends on synthetic fields and agreed definitions |
| HMW-003 | High | High | P1 | Required for academic reproducibility and safe interpretation |

## Non-goals for ideation

- HMW statements do not authorize use of real customer data or a live bank connection.
- They do not imply that synthetic patterns are business findings.
- They do not specify loan approval automation, risk scoring, causal inference, or operational action-taking.

## Assumptions and unresolved questions

- **A-002** and **A-005** remain in force: synthetic-only, descriptive demonstration.
- **OQ-001** through **OQ-010** remain open until addressed in the relevant requirement/design steps.
- HMW-001 relies on transaction-to-disbursement mapping; if the business definition changes, revise downstream BR/FR/KPI trace links without renumbering IDs.

## Exit criteria

Three opportunity statements are framed around identified stakeholders, each with a design direction, open evidence need, priority, and non-goals. Step 3 will translate these into business requirements and measurable acceptance outcomes.
