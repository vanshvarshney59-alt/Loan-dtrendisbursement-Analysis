# STEP 15 - BUILD, TEST AND FIX REPORT
## D17 | Loan Disbursement Trend Analysis

**Version:** 1.0 | **Status:** Executed build record | **Build owner:** SH-001

## 1. Build objective

Implement the synthetic-data MVP in Python/Streamlit with SQLite persistence, Plotly charts, locally bundled Tailwind-compatible tokens, deterministic generation, validation, and automated pytest checks. The build follows F-001â€“F-006 and FR/NFR requirements; it is not a production bank integration.

## 2. Implementation inventory

| Area | Implemented component | Requirement links |
|---|---|---|
| Generator | `loan_app/data.py`, `loan_trend_analysis.py` | FR-001, NFR-002 |
| Validation | Required field, type, category, date, amount, duplicate, direction, entity and relationship checks | FR-002, FR-010 |
| Persistence | SQLite normalized schema, FK enforcement, transaction-safe reload and query | FR-003, NFR-005 |
| Metrics | Canonical event predicate, safe ratios, monthly/category/outcome aggregates | FR-005â€“FR-008 |
| UI | Six Streamlit views with filters, KPIs, charts, data-quality notes, preview and export | FR-004â€“FR-010 |
| Styling | Local `assets/tailwind.css` utility tokens; no runtime CDN | UI requirements |
| Tests | 13 deterministic/unit/integration cases | NFR-007 |

## 3. Test execution record

| Test group | Command / environment | Result | Evidence |
|---|---|---|---|
| Automated functional + technical | `python -m pytest -q`, Python 3.14.3, Windows | **14 passed**; one deprecation warning from installed AnyIO pytest plugin | `outputs/test_results.txt` |
| Core module coverage | `python -m coverage run -m pytest -q`; coverage report | **92% total** across `loan_app` data, database and analytics modules | `outputs/test_coverage.txt` |
| Synthetic build smoke | Generate/validate/aggregate 12,000 events | **12,000 valid, 0 rejected; 4,132 successful disbursement events; INR 7,279,333,054.33** | `outputs/build_smoke.json` |
| App rendering | Streamlit `AppTest` harness | Overview and all six named views rendered with **0 app exceptions** | `outputs/qa_notes.md` |
| Performance | Local time measurement after DB initialization | See recorded timings; meets provisional NFR-001 for sample on this environment | `outputs/qa_notes.md` |
| Manual accessibility/cloud | Keyboard/screen reader and hosted cloud smoke | Not executed; Cloud account/repository unavailable | Step 16 deployment gate |

## 4. Defect and fix log

| ID | Requirement/test | Severity | Root cause | Fix | Retest evidence |
|---|---|---|---|---|---|
| DEF-001 | Validator dimension-conflict test | Low | Initial test expected two affected rows, while all three events using the conflicted loan ID were correctly rejected | Corrected expected invalid population to three | Full 13-case suite passed |
| DEF-002 | UI-02 / AppTest | High | Indentation error prevented Product & channel view compilation | Corrected indentation inside table expander | All six AppTest views passed |
| DEF-003 | UI chart/table API | Low | Streamlit emitted deprecation warning for `use_container_width` | Replaced with `width='stretch'` and removed unnecessary CORS override | All six views passed without app exceptions |

## 5. Measured sample results

Seed 42, 12,000 generated transaction events, 2021-01-01 through 2025-12-31. 4,132 successful disbursement events sum to INR 7,279,333,054.33. Transaction success rate is 97.79%; disbursement-attempt success rate is 96.41%. These values characterize only the synthetic generator.

## 6. Release decision

The automated suite and headless UI smoke pass; no known critical/high defect remains in executed scope. The app launches locally, data is labelled synthetic, and definitions are visible. Release is **locally validated and deployment-ready**, not cloud-published. Keyboard/screen-reader review and cloud smoke remain open.

## 7. Limitations

Single-user/small-volume academic MVP using SQLite. Coverage refers to core `loan_app` modules, not complete UI coverage. Performance applies only to the recorded Windows/Python environment and sample. One third-party deprecation warning remains. No production reliability, security certification, actual bank data quality or borrower behavior is asserted.

