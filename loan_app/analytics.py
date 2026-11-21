"""Canonical filters, KPIs, and descriptive aggregates."""
from __future__ import annotations

from typing import Any

import pandas as pd


def filter_transactions(
    frame: pd.DataFrame,
    start_date: Any = None,
    end_date: Any = None,
    loan_types: list[str] | None = None,
    branches: list[str] | None = None,
    channels: list[str] | None = None,
    statuses: list[str] | None = None,
) -> pd.DataFrame:
    data = frame.copy()
    if not pd.api.types.is_datetime64_any_dtype(data["transaction_date"]):
        data["transaction_date"] = pd.to_datetime(data["transaction_date"], errors="coerce")
    mask = data["transaction_date"].notna()
    if start_date is not None:
        mask &= data["transaction_date"].dt.date >= pd.Timestamp(start_date).date()
    if end_date is not None:
        mask &= data["transaction_date"].dt.date <= pd.Timestamp(end_date).date()
    for col, selected in (("loan_type", loan_types), ("branch_id", branches), ("channel", channels), ("status", statuses)):
        if selected:
            mask &= data[col].isin(selected)
    return data.loc[mask].copy().reset_index(drop=True)


def calculate_kpis(frame: pd.DataFrame) -> dict[str, int | float | None]:
    if frame.empty:
        return {"disbursed_amount": 0.0, "disbursement_count": 0, "average_disbursement": None,
                "failed_disbursement_amount": 0.0, "transaction_success_rate": None,
                "disbursement_success_rate": None, "flagged_loan_share": None,
                "transaction_count": 0}
    successful = frame["event_type"].eq("disbursement") & frame["status"].eq("success")
    attempts = frame["event_type"].eq("disbursement")
    failed = attempts & frame["status"].eq("failed")
    amount = float(frame.loc[successful, "amount"].sum())
    count = int(successful.sum())
    attempt_count = int(attempts.sum())
    unique_loans = frame.dropna(subset=["loan_id"]).drop_duplicates("loan_id")
    flag_share = None
    if not unique_loans.empty:
        flag_share = float(unique_loans["delinquency_flag"].astype(bool).mean() * 100)
    return {
        "disbursed_amount": amount,
        "disbursement_count": count,
        "average_disbursement": amount / count if count else None,
        "failed_disbursement_amount": float(frame.loc[failed, "amount"].sum()),
        "transaction_success_rate": float(frame["status"].eq("success").mean() * 100),
        "disbursement_success_rate": float(successful.sum() / attempt_count * 100) if attempt_count else None,
        "flagged_loan_share": flag_share,
        "transaction_count": int(len(frame)),
    }


def monthly_summary(frame: pd.DataFrame) -> pd.DataFrame:
    columns = ["month", "disbursed_amount", "disbursement_count", "failed_amount", "transaction_count"]
    if frame.empty:
        return pd.DataFrame(columns=columns)
    data = frame.copy()
    data["month"] = pd.to_datetime(data["transaction_date"]).dt.to_period("M").dt.to_timestamp()
    success = data["event_type"].eq("disbursement") & data["status"].eq("success")
    fail = data["event_type"].eq("disbursement") & data["status"].eq("failed")
    data["disbursed_amount"] = data["amount"].where(success, 0.0)
    data["disbursement_count"] = success.astype(int)
    data["failed_amount"] = data["amount"].where(fail, 0.0)
    summary = data.groupby("month", as_index=False).agg(
        disbursed_amount=("disbursed_amount", "sum"),
        disbursement_count=("disbursement_count", "sum"),
        failed_amount=("failed_amount", "sum"),
        transaction_count=("transaction_id", "size"),
    )
    month_range = pd.date_range(summary.month.min(), summary.month.max(), freq="MS")
    return summary.set_index("month").reindex(month_range, fill_value=0).rename_axis("month").reset_index()


def category_summary(frame: pd.DataFrame, dimension: str) -> pd.DataFrame:
    allowed = {"loan_type", "branch_id", "branch_name", "region", "channel"}
    if dimension not in allowed:
        raise ValueError(f"Unsupported dimension: {dimension}")
    cols = [dimension, "disbursement_count", "disbursed_amount", "failed_attempt_count"]
    if frame.empty:
        return pd.DataFrame(columns=cols)
    data = frame.copy()
    success = data["event_type"].eq("disbursement") & data["status"].eq("success")
    failed = data["event_type"].eq("disbursement") & data["status"].eq("failed")
    data["disbursement_count"] = success.astype(int)
    data["disbursed_amount"] = data["amount"].where(success, 0.0)
    data["failed_attempt_count"] = failed.astype(int)
    return data.groupby(dimension, as_index=False, dropna=False).agg(
        disbursement_count=("disbursement_count", "sum"),
        disbursed_amount=("disbursed_amount", "sum"),
        failed_attempt_count=("failed_attempt_count", "sum"),
    ).sort_values("disbursed_amount", ascending=False).reset_index(drop=True)


def outcome_summary(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["status", "event_type", "transaction_count", "amount"])
    return frame.groupby(["status", "event_type"], as_index=False).agg(
        transaction_count=("transaction_id", "size"), amount=("amount", "sum")
    )


def failure_reason_summary(frame: pd.DataFrame) -> pd.DataFrame:
    failed = frame.loc[frame["status"].eq("failed")].copy()
    if failed.empty:
        return pd.DataFrame(columns=["failure_reason", "transaction_count", "amount"])
    failed["failure_reason"] = failed["failure_reason"].replace("", "Unspecified")
    return failed.groupby("failure_reason", as_index=False).agg(
        transaction_count=("transaction_id", "size"), amount=("amount", "sum")
    ).sort_values("transaction_count", ascending=False).reset_index(drop=True)
