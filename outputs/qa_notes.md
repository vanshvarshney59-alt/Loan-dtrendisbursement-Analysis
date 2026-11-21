# QA Notes - D17

- Environment: Windows; Python 3.14.3; Streamlit 1.66.0.
- Dataset: 12,000 synthetic events, seed 42, 2021-01-01 to 2025-12-31.
- Data quality: 12,000 input, 12,000 valid, 0 rejected.
- AppTest: overview plus six app views rendered; no app exceptions.
- Timing (seconds): validation 0.360; SQLite initialize/load 1.526; SQLite read 0.287; filtered metrics/aggregates 0.097; overview render 3.398.
- The local DB-load figure includes schema setup and sample insertion; it is not the NFR-001 post-initialization query target.
- Keyboard/screen-reader accessibility was not manually evaluated. This headless check is not a Cloud deployment smoke test.
- KPI and trend results are synthetic outputs and have no real-bank evidentiary value.
