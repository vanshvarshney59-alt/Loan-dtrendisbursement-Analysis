"""SQLite schema and repository operations."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd

from .data import ValidationResult, validate_and_normalize


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS customer (
 customer_id TEXT PRIMARY KEY, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS account (
 account_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES customer(customer_id),
 account_type TEXT NOT NULL CHECK(account_type IN ('Savings','Current')), opened_on TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS branch (
 branch_id TEXT PRIMARY KEY, branch_name TEXT NOT NULL, region TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS loan (
 loan_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES customer(customer_id),
 account_id TEXT NOT NULL REFERENCES account(account_id), loan_type TEXT NOT NULL,
 delinquency_flag INTEGER NOT NULL CHECK(delinquency_flag IN (0,1)), created_on TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS transaction_event (
 transaction_id TEXT PRIMARY KEY, transaction_date TEXT NOT NULL,
 customer_id TEXT NOT NULL REFERENCES customer(customer_id),
 account_id TEXT NOT NULL REFERENCES account(account_id),
 branch_id TEXT NOT NULL REFERENCES branch(branch_id),
 loan_id TEXT REFERENCES loan(loan_id), transaction_type TEXT NOT NULL,
 event_type TEXT NOT NULL, channel TEXT NOT NULL, amount REAL NOT NULL CHECK(amount > 0),
 status TEXT NOT NULL, failure_reason TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS dataset_metadata (
 dataset_id TEXT PRIMARY KEY, schema_version TEXT NOT NULL, seed INTEGER NOT NULL,
 generated_at TEXT NOT NULL, row_count INTEGER NOT NULL CHECK(row_count >= 0),
 source_label TEXT NOT NULL, quality_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_event_date ON transaction_event(transaction_date);
CREATE INDEX IF NOT EXISTS idx_event_type_status_date ON transaction_event(event_type,status,transaction_date);
CREATE INDEX IF NOT EXISTS idx_event_branch_date ON transaction_event(branch_id,transaction_date);
CREATE INDEX IF NOT EXISTS idx_event_channel_date ON transaction_event(channel,transaction_date);
CREATE INDEX IF NOT EXISTS idx_event_loan ON transaction_event(loan_id);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def initialize_database(db_path: str | Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)


def replace_dataset(
    db_path: str | Path,
    frame: pd.DataFrame,
    metadata: dict[str, Any] | None = None,
    source_label: str = "synthetic bundled sample",
) -> dict[str, Any]:
    result: ValidationResult = validate_and_normalize(frame)
    data = result.data
    if metadata:
        result.quality.update(metadata)
    initialize_database(db_path)
    with connect(db_path) as conn:
        try:
            conn.execute("BEGIN IMMEDIATE")
            for table in ("transaction_event", "loan", "account", "branch", "customer", "dataset_metadata"):
                conn.execute(f"DELETE FROM {table}")
            customers = data[["customer_id"]].drop_duplicates()
            conn.executemany("INSERT INTO customer(customer_id) VALUES (?)", customers.itertuples(index=False, name=None))
            account_cols = data[["account_id", "customer_id", "account_type", "transaction_date"]].drop_duplicates("account_id")
            conn.executemany(
                "INSERT INTO account(account_id,customer_id,account_type,opened_on) VALUES (?,?,?,?)",
                [(r.account_id, r.customer_id, r.account_type, pd.Timestamp(r.transaction_date).date().isoformat()) for r in account_cols.itertuples(index=False)],
            )
            branch_cols = data[["branch_id", "branch_name", "region"]].drop_duplicates("branch_id")
            conn.executemany("INSERT INTO branch(branch_id,branch_name,region) VALUES (?,?,?)", branch_cols.itertuples(index=False, name=None))
            loan_cols = data[["loan_id", "customer_id", "account_id", "loan_type", "delinquency_flag", "transaction_date"]].drop_duplicates("loan_id")
            conn.executemany(
                "INSERT INTO loan(loan_id,customer_id,account_id,loan_type,delinquency_flag,created_on) VALUES (?,?,?,?,?,?)",
                [(r.loan_id, r.customer_id, r.account_id, r.loan_type, int(bool(r.delinquency_flag)), pd.Timestamp(r.transaction_date).date().isoformat()) for r in loan_cols.itertuples(index=False)],
            )
            events = data[["transaction_id", "transaction_date", "customer_id", "account_id", "branch_id", "loan_id", "transaction_type", "event_type", "channel", "amount", "status", "failure_reason"]]
            conn.executemany(
                """INSERT INTO transaction_event(transaction_id,transaction_date,customer_id,account_id,branch_id,loan_id,transaction_type,event_type,channel,amount,status,failure_reason)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                [(r.transaction_id, pd.Timestamp(r.transaction_date).date().isoformat(), r.customer_id, r.account_id, r.branch_id, r.loan_id, r.transaction_type, r.event_type, r.channel, float(r.amount), r.status, str(r.failure_reason or "")) for r in events.itertuples(index=False)],
            )
            seed = int((metadata or {}).get("seed", 42))
            schema_version = str(result.quality.get("schema_version", "1.0"))
            conn.execute(
                "INSERT INTO dataset_metadata(dataset_id,schema_version,seed,generated_at,row_count,source_label,quality_json) VALUES(?,?,?,?,?,?,?)",
                ("active", schema_version, seed, pd.Timestamp.now(tz="UTC").isoformat(), len(data), source_label, json.dumps(result.quality, sort_keys=True)),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    return result.quality


QUERY = """SELECT e.transaction_id,e.transaction_date,e.customer_id,e.account_id,a.account_type,
 e.branch_id,b.branch_name,b.region,e.transaction_type,e.event_type,e.channel,e.amount,e.status,
 e.failure_reason,e.loan_id,l.loan_type,l.delinquency_flag
 FROM transaction_event e JOIN customer c ON c.customer_id=e.customer_id
 JOIN account a ON a.account_id=e.account_id JOIN branch b ON b.branch_id=e.branch_id
 LEFT JOIN loan l ON l.loan_id=e.loan_id"""


def read_transactions(db_path: str | Path) -> pd.DataFrame:
    with connect(db_path) as conn:
        data = pd.read_sql_query(QUERY + " ORDER BY e.transaction_date,e.transaction_id", conn, parse_dates=["transaction_date"])
        metadata = conn.execute("SELECT quality_json FROM dataset_metadata WHERE dataset_id='active'").fetchone()
    if not data.empty:
        data["delinquency_flag"] = data["delinquency_flag"].astype(bool)
        data["is_disbursement_attempt"] = data["event_type"].eq("disbursement")
        data["is_successful_disbursement"] = data["is_disbursement_attempt"] & data["status"].eq("success")
        data["is_success"] = data["status"].eq("success")
    return data


def read_metadata(db_path: str | Path) -> dict[str, Any]:
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM dataset_metadata WHERE dataset_id='active'").fetchone()
    if row is None:
        return {}
    result = dict(row)
    result["quality"] = json.loads(result.pop("quality_json"))
    return result
