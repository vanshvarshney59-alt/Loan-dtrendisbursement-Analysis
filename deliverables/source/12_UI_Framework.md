# STEP 12 - UI FRAMEWORK AND SCREEN SPECIFICATION
## D17 | Loan Disbursement Trend Analysis

**Framework:** Streamlit | **Charts:** Plotly | **Visual direction:** Tailwind utility-style tokens, locally bundled | **Version:** 1.0

## 1. Experience goals

Let SH-003/SH-004 understand selected synthetic disbursement activity quickly, filter consistently, inspect definitions, and avoid confusing event counts, transaction success, loan count and funded amounts. Use responsive layout and native Streamlit controls for accessibility and reliability.

## 2. Navigation and screen inventory

| UI ID | Screen/view | Main purpose | Linked stories |
|---|---|---|---|
| UI-01 | Overview dashboard | KPIs, monthly trends, top-line filters | US-004, US-005, US-006 |
| UI-02 | Product and channel analysis | Loan type, branch, channel comparisons | US-006 |
| UI-03 | Transaction outcomes | Success/failure and reason breakdown | US-007 |
| UI-04 | Data quality and methodology | Dataset info, cleaning, definitions, limitations | US-002, US-008 |
| UI-05 | Transaction explorer | Bounded filtered preview and synthetic CSV export | US-004, US-009 |
| UI-06 | About / deployment | Project identity, synthetic notice, version/setup information | US-001, US-010 |

## 3. UI-01 overview layout

1. Header with D17 title, subtitle, persistent “Synthetic demonstration data” badge and dataset version/date range.
2. Sidebar filters: date range, loan type, branch, channel, transaction outcome; reset button.
3. KPI row: successful disbursed amount (INR), successful disbursement events, average event amount, disbursement attempt success rate.
4. Primary monthly line charts: amount and count; secondary views for loan-type mix and branch/channel comparison.
5. Expandable methodology note listing event predicate, units, grain and denominator.
6. Empty-state message if filters remove all rows; warnings if denominator is zero.

## 4. UI-02 through UI-06 behavior

- **UI-02:** selectable metric (amount/count), sorted category bars, branch/channel/loan type; labels avoid unexplained IDs.
- **UI-03:** transactions by status; failed attempts by reason; failed amount shown separately; no use of “approval rate.”
- **UI-04:** counts read/valid/rejected/duplicate; schema and category values; clean rules; sample flag caveat; seed/version.
- **UI-05:** configurable preview cap (default <=500 rows); sorted table; export honors active filters and adds a synthetic label.
- **UI-06:** project name/code, learner/mentor metadata, version, setup/deployment guide links, no secrets.

## 5. Visual system

Use slate/navy text, light neutral surfaces, blue primary accents and teal success accents. Use red/amber only for failure/warning states and pair with text/icons. Use a bundled local Tailwind-compatible utility stylesheet with defined design tokens; avoid runtime CDN dependence. Streamlit native components remain the interaction layer; no inaccessible custom control replaces a native input.

Typography: clear page title, section headings and readable body text. Chart rules: explicit titles, axis units and zero-denominator states; consistent INR number formatting; colorblind-safe palette; avoid 3D charts and unlabeled dual axes. Provide captions for what is included/excluded.

## 6. Filter contract

Filters apply as AND conditions across date range, loan type, branch, channel and optional status. All aggregate queries, table preview, download and KPI denominator use the same filtered event set. Reset restores full sample. Selection shows filtered transaction count and date window. Filter order is stable and defaults to all values.

## 7. Responsiveness and accessibility

Sidebar collapses on narrow screens; KPI cards wrap; chart columns stack on mobile. Maintain readable contrast, keyboard navigation via Streamlit controls, descriptive chart titles, text alternatives/captions, and labels not reliant on color. Respect browser zoom. Ensure a fresh user can find methodology and data warnings without scrolling through the entire page.

## 8. UI states

Loading: spinner and selected dataset metadata. Empty: “No transactions match these filters” plus reset. Invalid dataset: visible error and action to reload bundled sample. Database unavailable: safe explanation, no traceback in UI. Export unavailable: explain empty selection. Dataset loading: confirmed action, then updated timestamp. Cloud persistence warning: dataset may reset on app restart.

## 9. UI acceptance checks

Verify each UI ID against story acceptance criteria; all filters update all outputs; currency and percentages have units; 0 denominators produce N/A; synthetic notice is persistent; screen works at laptop and mobile width; keyboard-only operation is possible; no chart implies causality or real borrower risk.

## 10. Assumptions and decisions

OQ-008 is provisionally resolved for MVP as local bundled Tailwind-compatible CSS tokens plus Streamlit-native components; no CDN is required. Filters listed in OQ-007 are included. Final branding and ABES template alignment remain subject to mentor review.
