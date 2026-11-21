"""Synthetic transaction generation, validation, and normalization."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


SCHEMA_VERSION = "1.0"
CHANNELS = ("ATM", "UPI", "Net Banking", "Branch")
LOAN_TYPES = ("Personal", "Home", "Vehicle", "Education", "Business")
ACCOUNT_TYPES = ("Savings", "Current")
EVENT_TYPES = ("disbursement", "repayment", "reversal")
STATUSES = ("success", "failed")
TRANSACTION_TYPES = ("credit", "debit")
REGIONS = ("North", "South", "East", "West", "Central")
REQUIRED_COLUMNS = (
    "transaction_id", "transaction_date", "customer_id", "account_id", "account_type",
    "branch_id", "transaction_type", "event_type", "channel", "amount", "status",
    "failure_reason", "loan_id", "loan_type", "delinquency_flag",
)


@dataclass
class ValidationResult:
    data: pd.DataFrame
    quality: dict[str, Any]


def generate_dataset(rows: int = 12_000, seed: int = 42) -> pd.DataFrame:
    """Return deterministic, fictitious transaction events with consistent dimensions."""
    if rows < 1:
        raise ValueError("rows must be at least 1")
    if seed < 0:
        raise ValueError("seed must be non-negative")

    rng = np.random.default_rng(seed)
    customer_count = max(1, rows // 3)
    loan_count = max(1, rows // 2)
    customer_ids = np.array([f"CU{i:06d}" for i in range(1, customer_count + 1)])
    account_ids = np.array([f"AC{i:06d}" for i in range(1, customer_count + 1)])
    customer_for_loan = rng.choice(customer_ids, size=loan_count)
    account_by_customer = dict(zip(customer_ids, account_ids))
    loan_ids = np.array([f"LN{i:06d}" for i in range(1, loan_count + 1)])
    loan_types = rng.choice(LOAN_TYPES, size=loan_count, p=[.32, .22, .20, .12, .14])
    account_types = rng.choice(ACCOUNT_TYPES, size=customer_count, p=[.74, .26])
    account_type_by_id = dict(zip(account_ids, account_types))
    delinquency = rng.random(loan_count) < np.where(loan_types == "Business", .12, .075)

    dates = pd.date_range("2021-01-01", "2025-12-31", freq="D")
    weights = (0.82 + (dates.year.to_numpy() - 2021) * .09) * (
        1 + .10 * np.sin(2 * np.pi * dates.day_of_year.to_numpy() / 365.25)
    )
    weights = weights / weights.sum()
    tx_dates = pd.to_datetime(rng.choice(dates.to_numpy(), size=rows, p=weights))

    loan_idx = rng.integers(0, loan_count, size=rows)
    event_types = rng.choice(EVENT_TYPES, size=rows, p=[.36, .60, .04])
    transaction_types = np.where(event_types == "disbursement", "credit", "debit")
    tx_loan_types = loan_types[loan_idx]
    ranges = {
        "Personal": (15_000, 500_000), "Home": (500_000, 8_000_000),
        "Vehicle": (100_000, 2_500_000), "Education": (50_000, 2_000_000),
        "Business": (200_000, 6_000_000),
    }
    amounts = np.empty(rows, dtype=float)
    for i, (kind, event) in enumerate(zip(tx_loan_types, event_types)):
        low, high = ranges[kind]
        if event == "repayment":
            amounts[i] = rng.uniform(max(500, low * .01), max(5_000, min(high * .015, 80_000)))
        else:
            amounts[i] = rng.uniform(low, high)
    amounts = amounts.round(2)

    success_prob = np.select(
        [event_types == "disbursement", event_types == "repayment"], [.965, .985], default=.99
    )
    statuses = np.where(rng.random(rows) < success_prob, "success", "failed")
    failure_values = np.array(["Insufficient balance", "Network timeout", "Compliance review", "Invalid account"])
    failure_reasons = np.where(statuses == "failed", rng.choice(failure_values, rows), "")

    branch_no = rng.integers(1, 31, size=rows)
    regions = np.array([REGIONS[(n - 1) // 6] for n in branch_no])
    branch_ids = np.array([f"BR{n:03d}" for n in branch_no])
    channels = rng.choice(CHANNELS, size=rows, p=[.12, .29, .37, .22])
    rows_customer = customer_for_loan[loan_idx]
    rows_account = np.array([account_by_customer[c] for c in rows_customer])

    return pd.DataFrame({
        "transaction_id": [f"TX{i:07d}" for i in range(1, rows + 1)],
        "transaction_date": tx_dates,
        "customer_id": rows_customer,
        "account_id": rows_account,
        "account_type": [account_type_by_id[a] for a in rows_account],
        "branch_id": branch_ids,
        "branch_name": [f"{r} Branch {int(b[2:]):02d}" for r, b in zip(regions, branch_ids)],
        "region": regions,
        "transaction_type": transaction_types,
        "event_type": event_types,
        "channel": channels,
        "amount": amounts,
        "status": statuses,
        "failure_reason": failure_reasons,
        "loan_id": loan_ids[loan_idx],
        "loan_type": tx_loan_types,
        "delinquency_flag": delinquency[loan_idx],
        "seed_version": f"seed-{seed}-schema-{SCHEMA_VERSION}",
    }).sort_values(["transaction_date", "transaction_id"]).reset_index(drop=True)


def validate_and_normalize(frame: pd.DataFrame) -> ValidationResult:
    """Validate rows; return valid rows plus auditable exclusion counts."""
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = frame.copy()
    original_count = len(df)
    reasons = pd.Series("", index=df.index, dtype="string")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    for col in ("transaction_id", "customer_id", "account_id", "account_type", "branch_id",
                "transaction_type", "event_type", "channel", "status", "loan_id", "loan_type"):
        df[col] = df[col].astype("string").str.strip()
    for col in ("transaction_type", "event_type", "status"):
        df[col] = df[col].str.lower()
    df["loan_type"] = df["loan_type"].str.title()
    df["channel"] = df["channel"].str.strip()
    df["failure_reason"] = df["failure_reason"].fillna("").astype("string").str.strip()
    df["delinquency_flag"] = df["delinquency_flag"].astype("string").str.strip().str.lower().map(
        {"true": True, "1": True, "yes": True, "false": False, "0": False, "no": False}
    )

    invalid = pd.Series(False, index=df.index)
    invalid |= df[list(REQUIRED_COLUMNS)].isna().any(axis=1)
    invalid |= df["transaction_date"].isna()
    invalid |= df["amount"].isna() | (df["amount"] <= 0)
    invalid |= ~df["status"].isin(STATUSES)
    invalid |= ~df["transaction_type"].isin(TRANSACTION_TYPES)
    invalid |= ~df["event_type"].isin(EVENT_TYPES)
    invalid |= ~df["channel"].isin(CHANNELS)
    invalid |= ~df["loan_type"].isin(LOAN_TYPES)
    invalid |= ~df["account_type"].isin(ACCOUNT_TYPES)
    expected_direction = df["event_type"].map({"disbursement": "credit", "repayment": "debit", "reversal": "debit"})
    invalid |= df["transaction_type"] != expected_direction
    duplicated = df["transaction_id"].duplicated(keep="first")
    invalid |= duplicated
    identity_conflict = pd.Series(False, index=df.index)
    for key, attributes in {
        "account_id": ["customer_id", "account_type"],
        "loan_id": ["customer_id", "account_id", "loan_type", "delinquency_flag"],
        "branch_id": ["branch_name", "region"],
    }.items():
        if key in df.columns and all(attr in df.columns for attr in attributes):
            conflict_ids = set()
            for attr in attributes:
                conflicts = df.groupby(key, dropna=False)[attr].nunique(dropna=False)
                conflict_ids.update(conflicts[conflicts > 1].index.tolist())
            identity_conflict |= df[key].isin(conflict_ids)
    invalid |= identity_conflict
    account_owner = df.dropna(subset=["account_id", "customer_id"]).drop_duplicates("account_id").set_index("account_id")["customer_id"]
    loan_owner = df.dropna(subset=["loan_id", "customer_id", "account_id"]).drop_duplicates("loan_id")
    loan_customer = loan_owner.set_index("loan_id")["customer_id"]
    loan_account = loan_owner.set_index("loan_id")["account_id"]
    account_mismatch = df["account_id"].map(account_owner).ne(df["customer_id"])
    loan_mismatch = df["loan_id"].map(loan_customer).ne(df["customer_id"]) | df["loan_id"].map(loan_account).ne(df["account_id"])
    relationship_mismatch = account_mismatch | loan_mismatch
    invalid |= relationship_mismatch

    reason_counts = {
        "missing_required_or_unparseable": int(df[list(REQUIRED_COLUMNS)].isna().any(axis=1).sum()),
        "invalid_amount": int((df["amount"].isna() | (df["amount"] <= 0)).sum()),
        "invalid_enum_or_event_direction": int((
            ~df["status"].isin(STATUSES) | ~df["transaction_type"].isin(TRANSACTION_TYPES)
            | ~df["event_type"].isin(EVENT_TYPES) | ~df["channel"].isin(CHANNELS)
            | ~df["loan_type"].isin(LOAN_TYPES) | ~df["account_type"].isin(ACCOUNT_TYPES)
            | (df["transaction_type"] != expected_direction)
        ).sum()),
        "duplicate_transaction_id": int(duplicated.sum()),
        "inconsistent_dimension_mapping": int(identity_conflict.sum()),
        "foreign_key_mismatch": int(relationship_mismatch.sum()),
    }
    clean = df.loc[~invalid].copy()
    if "region" not in clean:
        clean["region"] = "Unknown"
    if "branch_name" not in clean:
        clean["branch_name"] = clean["branch_id"].astype(str)
    clean["is_disbursement_attempt"] = clean["event_type"].eq("disbursement")
    clean["is_successful_disbursement"] = clean["is_disbursement_attempt"] & clean["status"].eq("success")
    clean["is_success"] = clean["status"].eq("success")
    quality = {
        "input_rows": int(original_count),
        "valid_rows": int(len(clean)),
        "rejected_rows": int(original_count - len(clean)),
        "duplicate_rows": int(duplicated.sum()),
        "reason_counts": reason_counts,
        "schema_version": SCHEMA_VERSION,
    }
    return ValidationResult(clean.sort_values(["transaction_date", "transaction_id"]).reset_index(drop=True), quality)
