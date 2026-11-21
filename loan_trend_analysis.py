"""Loan disbursement trend analysis with reproducible synthetic transaction data."""
from __future__ import annotations

from pathlib import Path
import argparse
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
LOAN_TYPES = ["Personal", "Home", "Vehicle", "Education", "Business"]
CHANNELS = ["ATM", "UPI", "Net Banking", "Branch"]
REGIONS = ["North", "South", "East", "West", "Central"]
REQUIRED = {
    "transaction_id", "transaction_date", "customer_id", "account_id", "account_type",
    "branch_id", "transaction_type", "channel", "amount", "status", "loan_id",
    "loan_type", "delinquency_flag",
}


def make_sample_data(rows: int = 12000, seed: int = 42) -> pd.DataFrame:
    """Create illustrative transaction records; data is synthetic, never real borrower data."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2021-01-01", "2025-12-31", freq="D")
    weights = (0.78 + (dates.year.to_numpy() - 2021) * 0.11) * (
        1 + 0.12 * np.sin(2 * np.pi * dates.day_of_year.to_numpy() / 365.25)
    )
    weights = weights / weights.sum()
    tx_date = pd.to_datetime(rng.choice(dates, rows, p=weights))
    loan_type = rng.choice(LOAN_TYPES, rows, p=[0.32, 0.22, 0.20, 0.12, 0.14])
    event = rng.choice(["Disbursement", "Repayment"], rows, p=[0.39, 0.61])
    tx_type = np.where(event == "Disbursement", "credit", "debit")
    amount = np.array([
        rng.uniform(*({"Personal": (15000, 500000), "Home": (500000, 8000000),
                       "Vehicle": (100000, 2500000), "Education": (50000, 2000000),
                       "Business": (200000, 6000000)}[kind])) if txn == "Disbursement"
        else rng.uniform(3000, 75000)
        for kind, txn in zip(loan_type, event)
    ]).round(2)
    success_probability = np.where(event == "Disbursement", 0.965, 0.985)
    successful = rng.random(rows) < success_probability
    status = np.where(successful, "success", "failed")
    reasons = np.array(["Insufficient balance", "Network timeout", "Compliance review", "Invalid account"])
    failure_reason = np.where(successful, "", rng.choice(reasons, rows))
    region = rng.choice(REGIONS, rows)
    branch_no = rng.integers(1, 31, rows)
    channel = rng.choice(CHANNELS, rows, p=[0.12, 0.29, 0.37, 0.22])
    account_type = rng.choice(["Savings", "Current"], rows, p=[0.74, 0.26])
    delinquency = rng.random(rows) < np.where(loan_type == "Business", 0.12, 0.075)
    # Stable customer/account/loan identifiers create sensible repeated activity.
    customer_num = rng.integers(1, max(2, rows // 3), rows)
    loan_num = rng.integers(1, max(2, rows // 2), rows)
    frame = pd.DataFrame({
        "transaction_id": [f"TX{i:07d}" for i in range(1, rows + 1)],
        "transaction_date": tx_date,
        "customer_id": [f"CU{x:06d}" for x in customer_num],
        "account_id": [f"AC{x:06d}" for x in customer_num],
        "account_type": account_type,
        "branch_id": [f"{r[:2].upper()}-BR{b:03d}" for r, b in zip(region, branch_no)],
        "transaction_type": tx_type,
        "channel": channel,
        "amount": amount,
        "status": status,
        "failure_reason": failure_reason,
        "loan_id": [f"LN{x:06d}" for x in loan_num],
        "loan_type": loan_type,
        "delinquency_flag": delinquency,
        "event_type": event,
    })
    return frame.sort_values("transaction_date").reset_index(drop=True)


def clean_data(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
    df = frame.copy()
    original_rows = len(df)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["status"] = df["status"].astype("string").str.strip().str.lower()
    df["transaction_type"] = df["transaction_type"].astype("string").str.strip().str.lower()
    df["loan_type"] = df["loan_type"].astype("string").str.strip().str.title()
    df["channel"] = df["channel"].astype("string").str.strip()
    df["delinquency_flag"] = df["delinquency_flag"].astype("string").str.strip().str.lower().map(
        {"true": True, "1": True, "yes": True, "false": False, "0": False, "no": False}
    )
    for column in ["failure_reason"]:
        if column not in df:
            df[column] = ""
    df["failure_reason"] = df["failure_reason"].fillna("").astype(str).str.strip()
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    df = df.dropna(subset=list(REQUIRED - {"failure_reason"}))
    df = df[(df.amount > 0) & df.status.isin(["success", "failed"])
            & df.transaction_type.isin(["credit", "debit"])]
    df["failure_reason"] = df.failure_reason.where(df.status.eq("failed"), "")
    df["month"] = df.transaction_date.dt.to_period("M").dt.to_timestamp()
    df["is_disbursement"] = df.transaction_type.eq("credit") & df.status.eq("success")
    df["is_success"] = df.status.eq("success")
    metadata = {"input_rows": original_rows, "clean_rows": len(df), "dropped_rows": original_rows - len(df)}
    return df.sort_values("transaction_date").reset_index(drop=True), metadata


def summarize(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    d = df.copy()
    d["disbursed_amount"] = d.amount.where(d.is_disbursement, 0)
    d["disbursement_count"] = d.is_disbursement.astype(int)
    monthly = d.groupby("month", as_index=False).agg(
        transactions=("transaction_id", "size"), disbursement_count=("disbursement_count", "sum"),
        disbursed_amount=("disbursed_amount", "sum"), successful_transactions=("is_success", "sum"),
        delinquent_transactions=("delinquency_flag", "sum"))
    monthly["success_rate_pct"] = (monthly.successful_transactions / monthly.transactions * 100).round(2)
    monthly["avg_disbursement_amount"] = (monthly.disbursed_amount / monthly.disbursement_count.replace(0, np.nan)).round(2)
    monthly["delinquency_rate_pct"] = (monthly.delinquent_transactions / monthly.transactions * 100).round(2)

    def group_summary(column: str) -> pd.DataFrame:
        result = d.groupby(column, as_index=False).agg(
            transactions=("transaction_id", "size"), disbursement_count=("disbursement_count", "sum"),
            disbursed_amount=("disbursed_amount", "sum"), successful_transactions=("is_success", "sum"),
            delinquent_transactions=("delinquency_flag", "sum"))
        result["success_rate_pct"] = (result.successful_transactions / result.transactions * 100).round(2)
        result["delinquency_rate_pct"] = (result.delinquent_transactions / result.transactions * 100).round(2)
        return result.sort_values("disbursed_amount", ascending=False).reset_index(drop=True)

    return {"monthly": monthly, "loan_type": group_summary("loan_type"),
            "branch": group_summary("branch_id"), "channel": group_summary("channel")}


def create_visuals(df: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    monthly = tables["monthly"]
    by_type = tables["loan_type"].sort_values("disbursed_amount", ascending=False)
    by_channel = tables["channel"].sort_values("disbursed_amount", ascending=False)
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes[0, 0].plot(monthly.month, monthly.disbursed_amount / 1e6, color="#1769aa")
    axes[0, 0].set(title="Monthly successful disbursements", xlabel="Month", ylabel="INR (millions)")
    axes[0, 1].plot(monthly.month, monthly.disbursement_count, color="#16836b")
    axes[0, 1].set(title="Monthly disbursement count", xlabel="Month", ylabel="Transactions")
    sns.barplot(data=by_type, x="loan_type", y="disbursed_amount", ax=axes[1, 0])
    axes[1, 0].set(title="Disbursed amount by loan type", xlabel="Loan type", ylabel="INR")
    sns.barplot(data=by_channel, x="channel", y="disbursed_amount", ax=axes[1, 1])
    axes[1, 1].set(title="Disbursed amount by channel", xlabel="Channel", ylabel="INR")
    for ax in axes.flat:
        ax.tick_params(axis="x", rotation=20)
    fig.suptitle("Loan Disbursement Trend Analysis", fontsize=17, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "loan_disbursement_trends.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def create_dashboard(df: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    """Write a filterable, self-contained HTML dashboard (Plotly JS loaded from CDN)."""
    filter_data = df[["month", "loan_type", "branch_id", "channel", "transaction_type", "status",
                      "amount", "delinquency_flag", "is_disbursement"]].copy()
    filter_data["month"] = filter_data.month.dt.strftime("%Y-%m-%d")
    payload = filter_data.to_json(orient="records")
    loan_types = sorted(df.loan_type.dropna().unique())
    channels = sorted(df.channel.dropna().unique())
    branches = sorted(df.branch_id.dropna().unique())
    html = r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Loan Disbursement Dashboard</title><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>body{font:15px Arial,sans-serif;background:#f3f6fa;color:#172b4d;margin:0;padding:24px}h1{margin:0 0 6px}.note{color:#53657d;margin:0 0 18px}.filters,.cards,.charts{display:grid;gap:14px}.filters{grid-template-columns:repeat(auto-fit,minmax(160px,1fr));background:white;padding:16px;border-radius:10px}.filters label{font-weight:600}.filters select{display:block;width:100%;margin-top:7px;padding:9px;border:1px solid #ccd5e0;border-radius:6px}.cards{grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin:16px 0}.card,.chart{background:white;border-radius:10px;padding:16px;box-shadow:0 1px 4px #d8e0eb}.label{color:#53657d;font-size:13px}.value{font-size:25px;font-weight:700;margin-top:8px}.charts{grid-template-columns:repeat(auto-fit,minmax(360px,1fr))}.chart{min-height:350px}.foot{font-size:12px;color:#667;margin-top:16px}</style></head><body>
<h1>Loan Disbursement Trend Analysis</h1><p class="note">Use filters to explore successful credit disbursements. Currency values are INR.</p>
<section class="filters"><label>Loan type<select id="loan"><option value="">All loan types</option></select></label><label>Branch<select id="branch"><option value="">All branches</option></select></label><label>Channel<select id="channel"><option value="">All channels</option></select></label><label>Year<select id="year"><option value="">All years</option></select></label></section>
<section class="cards"><div class="card"><div class="label">Disbursed amount</div><div class="value" id="amount"></div></div><div class="card"><div class="label">Successful disbursements</div><div class="value" id="count"></div></div><div class="card"><div class="label">Average disbursement</div><div class="value" id="average"></div></div><div class="card"><div class="label">Transaction success rate</div><div class="value" id="success"></div></div></section>
<section class="charts"><div class="chart" id="trend"></div><div class="chart" id="types"></div><div class="chart" id="channels"></div><div class="chart" id="delinquency"></div></section>
<p class="foot">Illustrative synthetic dataset. A disbursement is counted as a successful credit transaction. Delinquency flag is a transaction-level sample attribute, not a validated portfolio delinquency measure.</p>
<script>const rows=__DATA__;
function addOptions(id,values){const s=document.getElementById(id);[...new Set(values)].sort().forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;s.appendChild(o)})}
addOptions('loan',rows.map(x=>x.loan_type));addOptions('branch',rows.map(x=>x.branch_id));addOptions('channel',rows.map(x=>x.channel));addOptions('year',rows.map(x=>x.month.slice(0,4)));
function currency(n){return new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(n)}
function render(){const loan=document.getElementById('loan').value,branch=document.getElementById('branch').value,channel=document.getElementById('channel').value,year=document.getElementById('year').value;
const selected=rows.filter(x=>(!loan||x.loan_type===loan)&&(!branch||x.branch_id===branch)&&(!channel||x.channel===channel)&&(!year||x.month.startsWith(year)));
const disb=selected.filter(x=>x.is_disbursement),amount=disb.reduce((a,x)=>a+x.amount,0),success=selected.filter(x=>x.status==='success').length;
document.getElementById('amount').textContent=currency(amount);document.getElementById('count').textContent=disb.length.toLocaleString();document.getElementById('average').textContent=currency(disb.length?amount/disb.length:0);document.getElementById('success').textContent=(selected.length?100*success/selected.length:0).toFixed(1)+'%';
const monthly={};disb.forEach(x=>{monthly[x.month]=(monthly[x.month]||0)+x.amount});const keys=Object.keys(monthly).sort();Plotly.react('trend',[{x:keys,y:keys.map(k=>monthly[k]),type:'scatter',mode:'lines',line:{color:'#1769aa'}}],{title:'Monthly successful disbursed amount',yaxis:{title:'INR'},margin:{t:48}} ,{responsive:true});
function sums(field){const z={};disb.forEach(x=>z[x[field]]=(z[x[field]]||0)+x.amount);return Object.entries(z).sort((a,b)=>b[1]-a[1])}
const byType=sums('loan_type'),byChannel=sums('channel');Plotly.react('types',[{x:byType.map(x=>x[0]),y:byType.map(x=>x[1]),type:'bar',marker:{color:'#16836b'}}],{title:'Disbursed amount by loan type',yaxis:{title:'INR'},margin:{t:48}},{responsive:true});
Plotly.react('channels',[{x:byChannel.map(x=>x[0]),y:byChannel.map(x=>x[1]),type:'bar',marker:{color:'#7654a8'}}],{title:'Disbursed amount by channel',yaxis:{title:'INR'},margin:{t:48}},{responsive:true});
const flags=selected.filter(x=>x.is_disbursement),dcount=flags.filter(x=>x.delinquency_flag).length;Plotly.react('delinquency',[{x:['Flagged','Not flagged'],y:[dcount,flags.length-dcount],type:'bar',marker:{color:['#d65d5d','#82a7c9']}}],{title:'Disbursements by delinquency flag (sample)',yaxis:{title:'Transactions'},margin:{t:48}},{responsive:true});}
['loan','branch','channel','year'].forEach(id=>document.getElementById(id).addEventListener('change',render));render();</script></body></html>'''.replace("__DATA__", payload)
    (OUTPUT_DIR / "loan_disbursement_dashboard.html").write_text(html, encoding="utf-8")


def write_report(df: pd.DataFrame, tables: dict[str, pd.DataFrame], metadata: dict) -> None:
    monthly, types = tables["monthly"], tables["loan_type"]
    total = df.loc[df.is_disbursement, "amount"].sum()
    count = int(df.is_disbursement.sum())
    rate = 100 * df.is_success.mean() if len(df) else 0
    period = f"{df.transaction_date.min():%b %Y}–{df.transaction_date.max():%b %Y}"
    best_month = monthly.loc[monthly.disbursed_amount.idxmax()] if len(monthly) else None
    top_type = types.iloc[0] if len(types) else None
    type_lines = "\n".join(f"- **{r.loan_type}:** INR {r.disbursed_amount:,.0f} across {int(r.disbursement_count):,} successful credits."
                           for r in types.itertuples())
    peak_line = (f"- Peak month by amount: **{best_month.month:%B %Y}**, INR {best_month.disbursed_amount:,.0f}."
                 if best_month is not None else "- No monthly disbursement data was available.")
    top_line = (f"- Largest loan type by disbursed amount: **{top_type.loan_type}** (INR {top_type.disbursed_amount:,.0f}, "
                f"{100*top_type.disbursed_amount/total:.1f}% of total)." if top_type is not None and total else "")
    text = f'''# Loan Disbursement Trend Analysis — Insight Report

**Project D17 | Banking & Finance | ABES Engineering College, MCA 2nd Year**  
**Skill track:** Data Analyst  
**Analysis period:** {period}  
**Data:** synthetic and illustrative; not actual customer or bank records.

## Executive summary

The cleaned dataset contains **{len(df):,} transactions** ({metadata['dropped_rows']:,} rows removed during cleaning). It includes **{count:,} successful credit disbursements** totaling **INR {total:,.0f}**. The transaction-level success rate is **{rate:.1f}%**.

## Key findings

{peak_line}
{top_line}
- Successful disbursement count is used as a proxy for loans disbursed because the suggested schema does not include a separate loan approval or loan booking event.
- Delinquency flag rates describe flagged transactions in this illustrative dataset. A loan-level delinquency rate should be calculated from a validated loan status and an agreed delinquency definition.

### Disbursed amount by loan type

{type_lines}

## KPI definitions

- **Disbursed amount:** sum of `amount` for rows where `transaction_type = credit` and `status = success`.
- **Disbursement count:** count of those successful credit rows.
- **Average disbursement:** disbursed amount divided by disbursement count.
- **Transaction success rate:** all successful transaction rows divided by all cleaned transaction rows. It is not the disbursement success rate.
- **Delinquency flag:** count/rate of rows with `delinquency_flag = true`; interpret cautiously at transaction grain.

## Data preparation

Parsed transaction dates and numeric amounts, normalized category labels, removed duplicate transaction IDs, excluded rows missing required fields or with invalid amounts/status/type, and cleared failure reasons for successful records. **{metadata['input_rows']:,} input rows** became **{metadata['clean_rows']:,} clean rows**.

## Recommendations

1. Compare monthly disbursed amounts and counts by loan type; investigate major shifts with business context before attributing causes.
2. Review failed transaction reasons and branch/channel patterns to identify operational follow-up areas.
3. Replace sample data with approved, privacy-safe source data and validate definitions with the business owner.
4. Add a stable loan-level disbursement event and dated delinquency status to support loan-level conversion and portfolio quality measures.

## Limitations

The sample data is generated for demonstration and has no real-world evidentiary value. The schema does not define approved amounts, unique loan origination events, reversals, or a delinquency aging threshold. A credit transaction is treated as a disbursement for this project; real deployments must validate that mapping.
'''
    (OUTPUT_DIR / "insight_report.md").write_text(text, encoding="utf-8")


def create_presentation(df: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    total = df.loc[df.is_disbursement, "amount"].sum()
    count = int(df.is_disbursement.sum())
    rate = 100 * df.is_success.mean() if len(df) else 0
    monthly = tables["monthly"]
    peak = monthly.loc[monthly.disbursed_amount.idxmax()] if len(monthly) else None
    loan_types = tables["loan_type"].head(5)
    type_rows = "".join(f"<tr><td>{r.loan_type}</td><td>{int(r.disbursement_count):,}</td><td>INR {r.disbursed_amount:,.0f}</td></tr>" for r in loan_types.itertuples())
    peak_text = f"{peak.month:%B %Y}: INR {peak.disbursed_amount:,.0f}" if peak is not None else "No disbursement records"
    slide = r'''<section class="slide title"><div class="tag">D17 · Banking & Finance</div><h1>Loan Disbursement<br>Trend Analysis</h1><p>ABES Engineering College · MCA 2nd Year · Data Analyst</p><small>Synthetic transaction data · 2021–2025</small></section>
<section class="slide"><div class="tag">01 · Purpose</div><h2>What we set out to learn</h2><ul><li>How successful disbursement amounts and counts change over time</li><li>How disbursement volume differs by loan type, branch and channel</li><li>What operational and data quality questions to investigate next</li></ul><p class="callout">A successful credit transaction is used as the disbursement proxy because the suggested fields do not identify a separate booking event.</p></section>
<section class="slide"><div class="tag">02 · Headline KPIs</div><h2>Disbursement snapshot</h2><div class="cards"><div><small>Successful credit disbursements</small><strong>__COUNT__</strong></div><div><small>Total disbursed amount</small><strong>__TOTAL__</strong></div><div><small>Transaction success rate</small><strong>__RATE__</strong></div><div><small>Clean transactions</small><strong>__ROWS__</strong></div></div><p>Transaction success rate includes both credits and debits; it is not the disbursement success rate.</p></section>
<section class="slide"><div class="tag">03 · Time trend</div><h2>When was disbursement volume highest?</h2><p class="big">__PEAK__</p><p>Review month-to-month changes alongside policy, seasonality and operating context before assigning causes.</p><div class="chart"><img src="loan_disbursement_trends.png" alt="Monthly disbursement trend chart"></div></section>
<section class="slide"><div class="tag">04 · Product mix</div><h2>Successful disbursements by loan type</h2><table><thead><tr><th>Loan type</th><th>Count</th><th>Amount</th></tr></thead><tbody>__TYPE_ROWS__</tbody></table><p>Compare counts as well as amounts; larger average ticket size can shift total volume.</p></section>
<section class="slide"><div class="tag">05 · Method and quality</div><h2>Reproducible, transaction-level analysis</h2><ul><li>Parsed dates and numeric amounts; normalized labels and flags</li><li>Removed duplicate transaction IDs and rows with invalid required values</li><li>Produced monthly, loan-type, branch and channel summaries</li><li>Kept synthetic sample data clearly labeled</li></ul><p class="callout">Delinquency is only a sample transaction-level flag here. A portfolio delinquency rate requires validated loan status history and a defined aging threshold.</p></section>
<section class="slide"><div class="tag">06 · Recommended next steps</div><h2>Turn the trends into decisions</h2><ol><li>Validate the credit-to-disbursement mapping with operations.</li><li>Review failed reasons by branch and channel to target process improvements.</li><li>Replace synthetic records with an approved, privacy-safe dataset.</li><li>Add loan booking, reversals and dated delinquency status for portfolio KPIs.</li></ol><p class="callout">Illustrative synthetic data has no real-world evidentiary value.</p></section>'''
    slide = (slide.replace("__COUNT__", f"{count:,}").replace("__TOTAL__", f"INR {total:,.0f}")
             .replace("__RATE__", f"{rate:.1f}%").replace("__ROWS__", f"{len(df):,}")
             .replace("__PEAK__", peak_text).replace("__TYPE_ROWS__", type_rows))
    html = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>D17 Loan Disbursement — Presentation</title><style>
*{box-sizing:border-box}body{margin:0;background:#101a2d;color:#162a45;font:20px Arial,sans-serif}.slide{display:none;position:relative;background:#fff;width:min(1100px,94vw);height:min(700px,88vh);margin:5vh auto;padding:7% 8%;border-radius:18px;box-shadow:0 20px 70px #0006;overflow:auto}.slide.active{display:block}.title{background:linear-gradient(135deg,#fff 65%,#dcecff)}.tag{color:#2672b8;text-transform:uppercase;font-weight:bold;font-size:14px;letter-spacing:1px}h1{font-size:clamp(42px,7vw,74px);line-height:1.05;margin:13% 0 20px}h2{font-size:clamp(30px,4vw,46px);margin:20px 0 30px}p,li{line-height:1.55}li{margin:13px 0}.title small{display:block;color:#65758b;margin-top:50px}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:30px 0}.cards div{background:#f0f5fb;border-radius:12px;padding:22px}.cards small{display:block;color:#61728a}.cards strong{display:block;font-size:clamp(23px,3vw,36px);margin-top:12px}.big{font-size:42px;font-weight:bold;color:#11735f}.callout{background:#eef5fc;border-left:5px solid #2672b8;padding:17px;margin-top:28px}.chart{height:300px}.chart img{width:100%;height:100%;object-fit:contain}table{border-collapse:collapse;width:100%;margin:25px 0}td,th{text-align:left;border-bottom:1px solid #dbe3ed;padding:14px}footer{position:fixed;bottom:15px;left:0;right:0;text-align:center;color:#dce7f6;font-size:13px}.controls{position:fixed;right:22px;top:15px;color:white}button{padding:10px 16px;border:0;border-radius:7px;margin-left:8px;cursor:pointer}@media(max-height:650px){.slide{height:82vh;padding:4% 6%}.chart{height:220px}}
</style></head><body>__SLIDES__<div class="controls"><button onclick="move(-1)">←</button><span id="counter"></span><button onclick="move(1)">→</button></div><footer>Use ← / → keys to navigate · D17 Loan Disbursement Trend Analysis</footer><script>const s=[...document.querySelectorAll('.slide')];let i=0;function show(){s.forEach((x,n)=>x.classList.toggle('active',n===i));document.getElementById('counter').textContent=(i+1)+' / '+s.length}function move(d){i=(i+d+s.length)%s.length;show()}document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){move(1)}if(e.key==='ArrowLeft'){move(-1)}});show()</script></body></html>'''.replace("__SLIDES__", slide)
    (OUTPUT_DIR / "presentation.html").write_text(html, encoding="utf-8")


def run(input_path: Path | None = None, rows: int = 12000) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    if input_path:
        raw = pd.read_csv(input_path)
        source = str(input_path)
    else:
        raw = make_sample_data(rows)
        raw.to_csv(DATA_DIR / "loan_transactions_sample.csv", index=False)
        source = "generated synthetic sample"
    df, metadata = clean_data(raw)
    metadata["source"] = source
    df.to_csv(DATA_DIR / "loan_transactions_clean.csv", index=False)
    tables = summarize(df)
    for name, table in tables.items():
        table.to_csv(OUTPUT_DIR / f"{name}_summary.csv", index=False)
    create_visuals(df, tables)
    create_dashboard(df, tables)
    write_report(df, tables, metadata)
    create_presentation(df, tables)
    (OUTPUT_DIR / "data_quality.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return {"data": df, "tables": tables, "metadata": metadata}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Optional CSV of transaction-level loan data")
    parser.add_argument("--rows", type=int, default=12000, help="Sample transactions generated when --input is omitted")
    args = parser.parse_args()
    result = run(args.input, args.rows)
    d = result["data"]
    total = d.loc[d.is_disbursement, "amount"].sum()
    print(f"Source: {result['metadata']['source']}")
    print(f"Rows: {result['metadata']['clean_rows']:,} clean / {result['metadata']['input_rows']:,} input")
    print(f"Successful disbursements: {int(d.is_disbursement.sum()):,}")
    print(f"Disbursed amount: INR {total:,.0f}")
    print(f"Outputs saved under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
