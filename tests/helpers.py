import pandas as pd


def mini_frame():
    rows = [
        ("TX001", "2024-01-05", "CU001", "AC001", "Savings", "BR001", "North Branch 01", "North", "credit", "disbursement", "UPI", 10000, "success", "", "LN001", "Home", False),
        ("TX002", "2024-01-20", "CU002", "AC002", "Current", "BR002", "South Branch 02", "South", "credit", "disbursement", "Branch", 5000, "failed", "Compliance review", "LN002", "Vehicle", True),
        ("TX003", "2024-01-25", "CU001", "AC001", "Savings", "BR001", "North Branch 01", "North", "debit", "repayment", "Net Banking", 1000, "success", "", "LN001", "Home", False),
        ("TX004", "2024-03-01", "CU003", "AC003", "Savings", "BR001", "North Branch 01", "North", "credit", "disbursement", "UPI", 25000, "success", "", "LN003", "Home", False),
        ("TX005", "2024-03-04", "CU003", "AC003", "Savings", "BR001", "North Branch 01", "North", "debit", "reversal", "Branch", 4000, "success", "", "LN003", "Home", False),
    ]
    cols = ["transaction_id", "transaction_date", "customer_id", "account_id", "account_type", "branch_id", "branch_name", "region", "transaction_type", "event_type", "channel", "amount", "status", "failure_reason", "loan_id", "loan_type", "delinquency_flag"]
    return pd.DataFrame(rows, columns=cols)
