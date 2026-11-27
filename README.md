# D17 - Loan Disbursement Trend Analysis

**ABES Engineering College | MCA 2nd Year | Data Analyst | Banking & Finance**  
**Learner:** Vansh Varshney, Roll No. 2500320140161 | **Mentor:** Kalpana Dwivedi

Academic analytics project built with Python, pandas, NumPy, Streamlit, SQLite, Plotly, pytest, and a locally bundled Tailwind-compatible style sheet. All records are synthetic. This app is a descriptive demonstration and must not be used for lending or borrower decisions.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python loan_trend_analysis.py
streamlit run app.py
```

The generator creates 12,000 deterministic synthetic transaction events (seed 42, dates 2021-01-01 through 2025-12-31). The Streamlit app creates/loads `data/loan_trend_analysis.db` and starts at the dashboard. To change the sample size/seed, run `python loan_trend_analysis.py --rows 12000 --seed 42`.

## Verify

```powershell
python -m pytest -q
python -m coverage run -m pytest
python -m coverage report
```

Core modules are in `loan_app/`: `data.py` generation/validation, `database.py` SQLite repository, and `analytics.py` filters/KPIs/aggregates. The notebook in `notebooks/loan_disbursement_analysis.ipynb` reproduces the core exploration.

## Data semantics

One CSV row is a transaction event. `event_type` is `disbursement`, `repayment`, or `reversal`; `transaction_type` is credit/debit and does not alone define a disbursement. The headline funded metric includes only `event_type=disbursement` and `status=success`. Failed attempts and reversals are kept separate. A disbursement event count is not necessarily a distinct loan count.

The seed and category distributions are illustrative, not calibrated to a real lender. The sample loan delinquency flag is fictional and has no aging/days-past-due definition. Currency is displayed as INR under assumption A-006; confirm if the academic brief expects another unit.

## Project deliverables

- `01_Project_Understanding.docx` and `deliverables/source/01_Project_Understanding.md` - Step 1.
- `deliverables/02_*.docx` through `deliverables/18_*.docx` - Steps 2-18, with the RTM as Excel at Step 4.
- `deliverables/04_Requirements_Traceability_Matrix.xlsx` - requirement-to-test/task links.
- `deliverables/18_ABES_Slide_Deck.pptx` - final slide deck; also a Word storyboard.
- `outputs/` - run-specific summaries, quality metadata, test/smoke evidence and reports.

## Streamlit Community Cloud

The app entry point is `app.py`; `requirements.txt` and `.streamlit/config.toml` are at repository root. Push to a GitHub repository owned/authorized by the learner, connect it in Streamlit Community Cloud, select the repository/branch and `app.py`, select a compatible Python version, then deploy and smoke-test. Cloud's requirements file is expected alongside the app or at repository root; see [Streamlit dependency guidance](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies) and [deployment steps](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). Deployment requires repository access/permissions; do not share credentials in chat. SQLite local file persistence on the hosted instance is not guaranteed, so the app reloads the synthetic sample if no active dataset is present.

## Local Git

The project is published in the learner's GitHub repository on branch `master` with release tag `d17-v1.0.0`.

## Published project links

- Live Streamlit dashboard: https://loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app/
- GitHub repository: https://github.com/vanshvarshney59-alt/Loan-dtrendisbursement-Analysis
- Submission PDFs and synthetic data bundle: see deliverables/.
