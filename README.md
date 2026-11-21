# D17 — Loan Disbursement Trend Analysis

**ABES Engineering College | MCA 2nd Year | Data Analyst skill track**  
An end-to-end, reproducible analysis of loan disbursement transactions using pandas, NumPy, Matplotlib, Seaborn, Plotly, and Jupyter/Colab. CSV summaries are prepared for Power BI or Tableau.

**Suggested duration:** 40 hours across 3 sprints · **Primary users:** Branch Manager and Risk & Operations Head.

## Dataset and definitions

Without `--input`, the project generates 12,000 synthetic transaction records for 2021–2025. The data is illustrative and does not represent real customers or a real lender. Fields follow the project brief: transaction/customer/account/branch IDs, transaction date/type, channel, amount, status/failure reason, loan ID/type, and delinquency flag. `event_type` is an additional convenience field in the generated sample.

For this project, a **successful disbursement** is a transaction with `transaction_type=credit` and `status=success`. The brief's suggested fields do not include a distinct booking event, so this mapping should be validated against real source systems. Delinquency is shown as a sample transaction-level flag, not as a validated loan-level portfolio measure.

Required CSV columns: `transaction_id`, `transaction_date`, `customer_id`, `account_id`, `account_type`, `branch_id`, `transaction_type` (`credit`/`debit`), `channel`, `amount`, `status` (`success`/`failed`), `loan_id`, `loan_type`, `delinquency_flag`. `failure_reason` is optional.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python loan_trend_analysis.py
```

Analyze an approved CSV instead:

```powershell
python loan_trend_analysis.py --input path\to\transactions.csv
```

The notebook at `notebooks/loan_disbursement_analysis.ipynb` documents loading, cleaning, EDA, KPIs, and findings. Run it in Jupyter or upload it to Google Colab. It uses the project module and sample CSV; for Colab, upload both the notebook and `loan_trend_analysis.py`, or place the module beside the notebook.

## Deliverables

- `data/loan_transactions_sample.csv` — generated sample transactions.
- `data/loan_transactions_clean.csv` — cleaned, analysis-ready transactions.
- `outputs/monthly_summary.csv`, `loan_type_summary.csv`, `branch_summary.csv`, `channel_summary.csv` — BI-ready aggregates.
- `outputs/loan_disbursement_trends.png` — static EDA chart.
- `outputs/loan_disbursement_dashboard.html` — filterable dashboard with year, loan type, branch, and channel filters.
- `outputs/insight_report.md` — KPIs, findings, recommendations, cleaning notes, and limitations.
- `outputs/presentation.html` — browser-ready slide presentation; use arrow keys to navigate.
- `outputs/data_quality.json` — input/cleaned row counts and source metadata.

## KPIs

- Disbursed amount = sum of successful credit transaction amounts.
- Disbursement count = number of successful credit transactions.
- Average disbursement = disbursed amount / disbursement count.
- Transaction success rate = successful transactions / all cleaned transactions.
- Delinquency flag rate = flagged transactions / transactions; interpret with care because the suggested schema is not loan-status history.

## Power BI / Tableau

Import the four summary CSVs for quick charts, or import the clean transaction CSV for interactive slicing. Suggested visuals: monthly disbursed amount and count, loan-type and branch comparisons, channel split, success rate, and a delinquency-flag count. Set `transaction_date`/`month` to date types and format amounts as INR. The standalone HTML dashboard already has filters if no BI tool is available.

## Git handoff

Repository name from the brief: `mca2-da-loan-disbursement-trend-analysis`. Add the project files, notebook, report, and generated sample/clean CSVs; commit and tag a release after review. Do not include real customer information or credentials.
