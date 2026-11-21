"""Generate D17 synthetic data and BI-ready descriptive summaries."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from loan_app.analytics import calculate_kpis, category_summary, monthly_summary
from loan_app.data import generate_dataset, validate_and_normalize


def write_report(frame, quality, monthly, by_type, by_branch, by_channel):
    kpis = calculate_kpis(frame)
    peak = monthly.loc[monthly.disbursed_amount.idxmax()] if len(monthly) else None
    top_type = by_type.iloc[0] if len(by_type) else None
    top_branch = by_branch.iloc[0] if len(by_branch) else None
    peak_line = f"{peak.month:%B %Y} (INR {peak.disbursed_amount:,.0f})" if peak is not None else "not available"
    type_line = f"{top_type.loan_type} (INR {top_type.disbursed_amount:,.0f})" if top_type is not None else "not available"
    branch_line = f"{top_branch.branch_name} (INR {top_branch.disbursed_amount:,.0f})" if top_branch is not None else "not available"
    report = f'''# D17 - Loan Disbursement Trend Analysis: Insight Report

**ABES Engineering College | MCA 2nd Year | Data Analyst**  
**Learner:** Vansh Varshney | **Roll:** 2500320140161 | **Mentor:** Kalpana Dwivedi  
**Data:** Synthetic only | **Period:** {frame.transaction_date.min():%Y-%m-%d} to {frame.transaction_date.max():%Y-%m-%d} | **Seed:** 42

## Executive summary

The generated dataset has **{len(frame):,} valid synthetic transaction events** and **{quality['rejected_rows']:,} rejected rows**. It contains **{kpis['disbursement_count']:,} successful disbursement events** totaling **INR {kpis['disbursed_amount']:,.2f}**. Transaction success rate is **{kpis['transaction_success_rate']:.2f}%**; disbursement-attempt success rate is **{kpis['disbursement_success_rate']:.2f}%**.

## Descriptive findings

- Highest monthly successful disbursement amount in this generated sample: **{peak_line}**.
- Highest loan-type amount in this sample: **{type_line}**.
- Highest branch amount in this sample: **{branch_line}**.
- The chart and filters support comparison by date, loan type, branch, channel and status.

These are descriptive outputs of the specified random generator, not findings about an actual bank, customer base, or market.

## KPI definitions

- **Successful disbursed amount:** sum of `amount` where `event_type=disbursement` and `status=success`.
- **Disbursement event count:** count of those successful events; not necessarily distinct loans.
- **Average disbursement:** amount divided by successful disbursement event count.
- **Transaction success rate:** successful transactions divided by all selected transactions.
- **Disbursement-attempt success rate:** successful disbursement events divided by all disbursement attempts.
- **Failed disbursement amount:** failed disbursement attempt amount, displayed separately from funded amount.

## Data preparation and quality

Rows checked: {quality['input_rows']:,}; valid: {quality['valid_rows']:,}; rejected: {quality['rejected_rows']:,}. The generator/validator checks required fields, parsing, category values, event-direction consistency, positive amounts, duplicate transaction IDs, stable entity mappings and relationship consistency. Seed/version metadata is saved in `outputs/data_quality.json`.

## Recommendations for a real analysis

1. Confirm the event-system definition of disbursement and reversal netting before interpreting any total.
2. Replace synthetic data only with an authorized, privacy-safe dataset and preserve lineage/quality checks.
3. Define delinquency with an agreed loan-level grain and days-past-due threshold before reporting risk measures.
4. Review observed failure patterns with business owners; do not infer causes from these generated records.

## Limitations

This dataset is synthetic, seeded, and intentionally illustrative. INR is an assumption. Gross disbursement totals exclude reversal netting. Sample loan flags have no arrears aging definition. No causal, predictive, approval, or creditworthiness inference is supported.
'''
    (ROOT / "outputs" / "insight_report.md").write_text(report, encoding="utf-8")


def write_static_chart(monthly, by_type, by_branch, by_channel):
    sns.set_theme(style="whitegrid", palette="deep")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes[0, 0].plot(monthly.month, monthly.disbursed_amount / 1_000_000, color="#2563eb")
    axes[0, 0].set(title="Monthly successful disbursement amount", ylabel="INR millions", xlabel="Month")
    sns.barplot(data=by_type, x="loan_type", y="disbursed_amount", ax=axes[0, 1])
    axes[0, 1].set(title="Disbursed amount by loan type", ylabel="INR", xlabel="Loan type")
    sns.barplot(data=by_branch.head(10), x="branch_name", y="disbursed_amount", ax=axes[1, 0])
    axes[1, 0].set(title="Top 10 branches by sample amount", ylabel="INR", xlabel="Branch")
    sns.barplot(data=by_channel, x="channel", y="disbursed_amount", ax=axes[1, 1])
    axes[1, 1].set(title="Disbursed amount by channel", ylabel="INR", xlabel="Channel")
    for ax in axes.flat:
        ax.tick_params(axis="x", rotation=25)
    fig.suptitle("D17 | Synthetic Loan Disbursement Trends", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(ROOT / "outputs" / "loan_disbursement_trends.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    product_fig, product_ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=by_type, x="loan_type", y="disbursed_amount", ax=product_ax, color="#2563eb")
    product_ax.set(title="Successful synthetic disbursement amount by loan type", ylabel="INR", xlabel="Loan type")
    product_ax.tick_params(axis="x", rotation=15)
    product_fig.tight_layout()
    product_fig.savefig(ROOT / "outputs" / "loan_type_breakdown.png", dpi=160, bbox_inches="tight")
    plt.close(product_fig)


def build_artifacts(rows: int = 12_000, seed: int = 42) -> dict:
    data_dir = ROOT / "data"
    output_dir = ROOT / "outputs"
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    raw = generate_dataset(rows=rows, seed=seed)
    raw.to_csv(data_dir / "loan_transactions_sample.csv", index=False)
    result = validate_and_normalize(raw)
    clean = result.data
    clean.to_csv(data_dir / "loan_transactions_clean.csv", index=False)
    result.quality.update({"seed": seed, "source": "synthetic generator", "schema_version": "1.0"})
    (output_dir / "data_quality.json").write_text(json.dumps(result.quality, indent=2), encoding="utf-8")
    summaries = {
        "monthly_summary.csv": monthly_summary(clean),
        "loan_type_summary.csv": category_summary(clean, "loan_type"),
        "branch_summary.csv": category_summary(clean, "branch_name"),
        "channel_summary.csv": category_summary(clean, "channel"),
    }
    for filename, frame in summaries.items():
        frame.to_csv(output_dir / filename, index=False)
    trend = summaries["monthly_summary.csv"]
    by_type = summaries["loan_type_summary.csv"]
    by_branch = summaries["branch_summary.csv"]
    by_channel = summaries["channel_summary.csv"]
    fig = px.line(trend, x="month", y="disbursed_amount", markers=True, title="Monthly successful synthetic disbursement amount")
    fig.update_yaxes(title="INR")
    fig.write_html(output_dir / "loan_disbursement_trends.html", include_plotlyjs="cdn")
    write_static_chart(trend, by_type, by_branch, by_channel)
    write_report(clean, result.quality, trend, by_type, by_branch, by_channel)
    return {"data": clean, "quality": result.quality, "summaries": summaries}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=12_000, help="Synthetic transaction count")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic generator seed")
    args = parser.parse_args()
    built = build_artifacts(args.rows, args.seed)
    data = built["data"]
    successful = data.loc[data.is_successful_disbursement]
    print(f"Synthetic transactions: {len(data):,}")
    print(f"Successful disbursements: {len(successful):,}")
    print(f"Successful disbursed amount: INR {successful.amount.sum():,.2f}")
    print(f"Outputs: {ROOT / 'data'} and {ROOT / 'outputs'}")


if __name__ == "__main__":
    main()
