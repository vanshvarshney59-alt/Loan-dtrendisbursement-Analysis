"""Streamlit dashboard for the synthetic D17 loan disbursement project."""
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from loan_app.analytics import (
    calculate_kpis,
    category_summary,
    failure_reason_summary,
    filter_transactions,
    monthly_summary,
    outcome_summary,
)
from loan_app.data import generate_dataset
from loan_app.database import initialize_database, read_metadata, read_transactions, replace_dataset


ROOT = Path(__file__).resolve().parent
SAMPLE_PATH = ROOT / "data" / "loan_transactions_sample.csv"
DEFAULT_DB_PATH = ROOT / "data" / "loan_trend_analysis.db"
DB_PATH = Path(os.getenv("LOAN_DB_PATH", str(DEFAULT_DB_PATH)))

st.set_page_config(page_title="D17 | Loan Disbursement Trends", page_icon="📊", layout="wide")


def load_styles() -> None:
    css_path = ROOT / "assets" / "tailwind.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def ensure_seeded() -> None:
    initialize_database(DB_PATH)
    try:
        current = read_metadata(DB_PATH)
    except Exception:
        current = {}
    if current.get("row_count", 0) == 0:
        if SAMPLE_PATH.exists():
            sample = pd.read_csv(SAMPLE_PATH)
            replace_dataset(DB_PATH, sample, {"seed": 42}, "synthetic bundled sample; seed 42")
        else:
            sample = generate_dataset()
            replace_dataset(DB_PATH, sample, {"seed": 42}, "generated synthetic sample; seed 42")


@st.cache_data(ttl=60, show_spinner="Loading the synthetic sample...")
def get_frame(db_path: str, _db_version: int) -> pd.DataFrame:
    return read_transactions(db_path)


def fmt_inr(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"₹{value:,.0f}"


def all_or_values(values: list[str]) -> list[str] | None:
    return None if not values or "All" in values else values


def reset_filters() -> None:
    st.session_state["date_filter"] = (st.session_state["filter_min"], st.session_state["filter_max"])
    for key in ("loan_filter", "branch_filter", "channel_filter", "status_filter"):
        st.session_state[key] = ["All"]


def synthetic_notice() -> None:
    st.markdown(
        '<div class="synthetic-banner"><strong>Synthetic demonstration data</strong> · '
        'Fictional records only. Results are not evidence about a real bank or borrower population.</div>',
        unsafe_allow_html=True,
    )


def add_plotly(fig, height: int = 380) -> None:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=54, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#24364b"),
        legend_title_text="",
    )
    st.plotly_chart(fig, width="stretch")


def main() -> None:
    load_styles()
    ensure_seeded()
    db_stamp = DB_PATH.stat().st_mtime_ns if DB_PATH.exists() else 0
    raw = get_frame(str(DB_PATH), db_stamp)
    metadata = read_metadata(DB_PATH)
    if raw.empty:
        st.error("The sample dataset is empty. Use Reload sample from the sidebar.")
        st.stop()

    st.sidebar.markdown("# D17 · Analysis")
    st.sidebar.caption("Loan Disbursement Trend Analysis")
    page = st.sidebar.radio(
        "Navigate",
        ["Overview", "Product & channel", "Transaction outcomes", "Data quality", "Transaction explorer", "About"],
        label_visibility="collapsed",
    )
    st.sidebar.markdown("### Filters")
    min_day = raw.transaction_date.min().date()
    max_day = raw.transaction_date.max().date()
    st.session_state["filter_min"] = min_day
    st.session_state["filter_max"] = max_day
    date_range = st.sidebar.date_input("Transaction date range", value=(min_day, max_day), min_value=min_day, max_value=max_day, key="date_filter")
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range

    loan_values = ["All"] + sorted(raw.loan_type.dropna().unique().tolist())
    branch_values = ["All"] + sorted(raw.branch_id.dropna().unique().tolist())
    channel_values = ["All"] + sorted(raw.channel.dropna().unique().tolist())
    status_values = ["All", "success", "failed"]
    loan_selection = st.sidebar.multiselect("Loan type", loan_values, default=["All"], key="loan_filter")
    branch_selection = st.sidebar.multiselect("Branch", branch_values, default=["All"], key="branch_filter")
    channel_selection = st.sidebar.multiselect("Channel", channel_values, default=["All"], key="channel_filter")
    status_selection = st.sidebar.multiselect("Transaction status", status_values, default=["All"], key="status_filter")
    st.sidebar.button("Reset filters", use_container_width=True, on_click=reset_filters)
    if st.sidebar.button("Reload synthetic sample", use_container_width=True):
        sample = generate_dataset(seed=42)
        replace_dataset(DB_PATH, sample, {"seed": 42}, "generated synthetic sample; seed 42")
        get_frame.clear()
        st.rerun()
    st.sidebar.caption(f"Seed: {metadata.get('seed', 'unknown')} · Schema: {metadata.get('schema_version', 'unknown')}")

    selected = filter_transactions(
        raw,
        start_date=start_date,
        end_date=end_date,
        loan_types=all_or_values(loan_selection),
        branches=all_or_values(branch_selection),
        channels=all_or_values(channel_selection),
        statuses=all_or_values(status_selection),
    )
    st.title("Loan Disbursement Trend Analysis")
    synthetic_notice()
    st.caption(
        f"{len(selected):,} of {len(raw):,} transactions · "
        f"{pd.Timestamp(start_date):%d %b %Y} to {pd.Timestamp(end_date):%d %b %Y} · Currency assumed INR"
    )

    if page == "Overview":
        render_overview(selected)
    elif page == "Product & channel":
        render_product(selected)
    elif page == "Transaction outcomes":
        render_outcomes(selected)
    elif page == "Data quality":
        render_quality(raw, metadata)
    elif page == "Transaction explorer":
        render_explorer(selected)
    else:
        render_about(metadata)


def render_overview(frame: pd.DataFrame) -> None:
    st.subheader("Disbursement snapshot")
    kpi = calculate_kpis(frame)
    cols = st.columns(4)
    cols[0].metric("Successful disbursed amount", fmt_inr(kpi["disbursed_amount"]))
    cols[1].metric("Successful disbursement events", f"{kpi['disbursement_count']:,}")
    cols[2].metric("Average event amount", fmt_inr(kpi["average_disbursement"]))
    rate = kpi["disbursement_success_rate"]
    cols[3].metric("Disbursement attempt success", "N/A" if rate is None else f"{rate:.1f}%")
    st.caption("Funded totals include only event_type=disbursement and status=success. Event count is not a distinct loan count.")
    if frame.empty:
        st.info("No transactions match these filters. Use Reset filters in the sidebar.")
        return
    monthly = monthly_summary(frame)
    left, right = st.columns(2)
    with left:
        fig = px.line(monthly, x="month", y="disbursed_amount", markers=True, title="Monthly successful disbursed amount")
        fig.update_yaxes(title="INR")
        add_plotly(fig)
    with right:
        fig = px.bar(monthly, x="month", y="disbursement_count", title="Monthly successful disbursement events")
        fig.update_yaxes(title="Events")
        add_plotly(fig)
    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        by_type = category_summary(frame, "loan_type")
        add_plotly(px.bar(by_type, x="loan_type", y="disbursed_amount", title="Successful disbursed amount by loan type"))
    with bottom_right:
        by_channel = category_summary(frame, "channel")
        add_plotly(px.bar(by_channel, x="channel", y="disbursed_amount", title="Successful disbursed amount by channel"))
    with st.expander("How these KPIs are defined"):
        st.markdown(
            "- **Disbursed amount:** sum of amount for successful disbursement events.\n"
            "- **Disbursement count:** number of successful disbursement events, not unique loans.\n"
            "- **Average event amount:** disbursed amount divided by successful event count.\n"
            "- **Disbursement attempt success:** successful disbursement events / all disbursement attempts.\n"
            "- **Transaction success:** includes all selected event types and is shown on the outcomes page."
        )


def render_product(frame: pd.DataFrame) -> None:
    st.subheader("Product, branch and channel analysis")
    if frame.empty:
        st.info("No transactions match these filters. Use Reset filters in the sidebar.")
        return
    metric = st.radio("Measure", ["disbursed_amount", "disbursement_count"], horizontal=True, format_func=lambda x: "INR amount" if x == "disbursed_amount" else "Event count")
    for dim, label in (("loan_type", "Loan type"), ("branch_name", "Branch"), ("channel", "Channel")):
        summary = category_summary(frame, dim)
        fig = px.bar(summary, x=dim, y=metric, title=f"Successful disbursements by {label.lower()}", text_auto=".2s")
        fig.update_yaxes(title="INR" if metric == "disbursed_amount" else "Events")
        add_plotly(fig, height=420)
        with st.expander(f"View {label.lower()} summary table"):
            st.dataframe(summary, width="stretch", hide_index=True)


def render_outcomes(frame: pd.DataFrame) -> None:
    st.subheader("Transaction outcomes and exceptions")
    if frame.empty:
        st.info("No transactions match these filters. Use Reset filters in the sidebar.")
        return
    kpi = calculate_kpis(frame)
    cols = st.columns(3)
    cols[0].metric("Transaction success rate", "N/A" if kpi["transaction_success_rate"] is None else f"{kpi['transaction_success_rate']:.1f}%")
    cols[1].metric("Failed disbursement amount", fmt_inr(kpi["failed_disbursement_amount"]))
    cols[2].metric("Flagged loan share (sample)", "N/A" if kpi["flagged_loan_share"] is None else f"{kpi['flagged_loan_share']:.1f}%")
    st.caption("The sample delinquency flag is synthetic and has no days-past-due definition; it is not a portfolio delinquency measure.")
    summary = outcome_summary(frame)
    left, right = st.columns(2)
    with left:
        add_plotly(px.bar(summary, x="event_type", y="transaction_count", color="status", barmode="group", title="Transaction outcomes by event"))
    with right:
        reasons = failure_reason_summary(frame)
        add_plotly(px.bar(reasons, x="failure_reason", y="transaction_count", title="Failed transaction reasons"))
    st.dataframe(summary, width="stretch", hide_index=True)


def render_quality(frame: pd.DataFrame, metadata: dict) -> None:
    st.subheader("Data quality and methodology")
    quality = metadata.get("quality", {})
    cols = st.columns(4)
    cols[0].metric("Input rows", f"{quality.get('input_rows', len(frame)):,}")
    cols[1].metric("Valid rows", f"{quality.get('valid_rows', len(frame)):,}")
    cols[2].metric("Rejected rows", f"{quality.get('rejected_rows', 0):,}")
    cols[3].metric("Duplicate IDs", f"{quality.get('duplicate_rows', 0):,}")
    st.markdown("**Source label:** synthetic demonstration data  ")
    st.markdown(f"**Schema:** {metadata.get('schema_version', 'unknown')} · **Seed:** {metadata.get('seed', 'unknown')} · **Loaded:** {metadata.get('generated_at', 'unknown')}")
    st.markdown("### Event and KPI rules")
    st.markdown(
        "A successful disbursement is an event with `event_type=disbursement` and `status=success`. "
        "Repayments and reversals are not added to gross successful disbursement amount. Failed disbursement attempts are shown separately. "
        "The sample delinquency flag is assigned at loan level for synthetic demonstration only; no aging or days-past-due threshold exists."
    )
    st.markdown("### Validation counts")
    st.json(quality.get("reason_counts", {}))
    st.markdown("### Dataset profile")
    st.write({"Date range": f"{frame.transaction_date.min().date()} to {frame.transaction_date.max().date()}",
              "Unique transactions": int(frame.transaction_id.nunique()), "Unique loans": int(frame.loan_id.nunique()),
              "Unique branches": int(frame.branch_id.nunique()), "Unique customers": int(frame.customer_id.nunique())})


def render_explorer(frame: pd.DataFrame) -> None:
    st.subheader("Filtered transaction explorer")
    st.caption("Preview is capped at 500 rows. The complete filtered synthetic result can be downloaded.")
    st.dataframe(frame.head(500), width="stretch", hide_index=True)
    csv_bytes = frame.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered synthetic CSV", data=csv_bytes,
        file_name="d17_synthetic_filtered_transactions.csv", mime="text/csv",
        disabled=frame.empty,
    )


def render_about(metadata: dict) -> None:
    st.subheader("About this academic demonstration")
    st.markdown(
        "**D17 | Loan Disbursement Trend Analysis**  \n"
        "ABES Engineering College · MCA 2nd Year · Data Analyst · Banking and Finance  \n"
        "Learner: Vansh Varshney · Mentor: Kalpana Dwivedi"
    )
    st.info("All records are synthetic. This application is not connected to a bank and must not be used for lending, credit, or customer decisions.")
    st.write({"Seed": metadata.get("seed"), "Schema version": metadata.get("schema_version"), "Sample rows": metadata.get("row_count"), "Source": metadata.get("source_label")})
    st.markdown("The hosted SQLite file may be ephemeral. Reload the bundled synthetic sample after a restart if needed.")


if __name__ == "__main__":
    main()
