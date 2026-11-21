import pandas as pd
import pytest

from loan_app.data import generate_dataset, validate_and_normalize
from tests.helpers import mini_frame


def test_generator_is_deterministic_and_has_required_fields():
    first = generate_dataset(rows=250, seed=7)
    second = generate_dataset(rows=250, seed=7)
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 250
    assert first.transaction_id.is_unique
    assert {"event_type", "delinquency_flag", "branch_id"}.issubset(first.columns)


def test_generated_dimensions_are_consistent():
    data = generate_dataset(rows=500, seed=9)
    assert data.groupby("loan_id").loan_type.nunique().max() == 1
    assert data.groupby("account_id").customer_id.nunique().max() == 1
    assert data.groupby("branch_id").region.nunique().max() == 1


def test_validator_rejects_duplicate_bad_amount_and_bad_direction():
    data = mini_frame()
    bad = data.iloc[[0]].copy()
    bad.loc[:, "transaction_id"] = "TX001"
    invalid_amount = data.iloc[[1]].copy()
    invalid_amount.loc[:, "transaction_id"] = "TX006"
    invalid_amount.loc[:, "amount"] = -5
    invalid_direction = data.iloc[[0]].copy()
    invalid_direction.loc[:, "transaction_id"] = "TX007"
    invalid_direction.loc[:, "transaction_type"] = "debit"
    result = validate_and_normalize(pd.concat([data, bad, invalid_amount, invalid_direction], ignore_index=True))
    assert result.quality["rejected_rows"] == 3
    assert result.quality["duplicate_rows"] == 1
    assert len(result.data) == 5


def test_validator_rejects_inconsistent_loan_dimensions():
    data = mini_frame()
    conflict = data.iloc[[0]].copy()
    conflict.loc[:, "transaction_id"] = "TX008"
    conflict.loc[:, "loan_type"] = "Personal"
    result = validate_and_normalize(pd.concat([data, conflict], ignore_index=True))
    assert result.quality["reason_counts"]["inconsistent_dimension_mapping"] == 3
    assert len(result.data) == 3


def test_missing_required_column_is_explicit_error():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_and_normalize(mini_frame().drop(columns=["event_type"]))
