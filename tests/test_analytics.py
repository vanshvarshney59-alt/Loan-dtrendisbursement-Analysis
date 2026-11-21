import pytest

from loan_app.analytics import (
    calculate_kpis, category_summary, failure_reason_summary, filter_transactions,
    monthly_summary, outcome_summary,
)
from loan_app.data import validate_and_normalize
from tests.helpers import mini_frame


@pytest.fixture
def data():
    return validate_and_normalize(mini_frame()).data


def test_disbursement_kpis_do_not_count_repayment_reversal_or_failure(data):
    kpis = calculate_kpis(data)
    assert kpis["disbursed_amount"] == 35_000
    assert kpis["disbursement_count"] == 2
    assert kpis["average_disbursement"] == 17_500
    assert kpis["failed_disbursement_amount"] == 5_000
    assert kpis["transaction_success_rate"] == 80
    assert kpis["disbursement_success_rate"] == pytest.approx(2 / 3 * 100)
    assert kpis["flagged_loan_share"] == pytest.approx(1 / 3 * 100)


def test_zero_denominator_and_empty_state_are_safe(data):
    empty = calculate_kpis(data.iloc[0:0])
    assert empty["disbursed_amount"] == 0
    assert empty["average_disbursement"] is None
    no_attempts = data[data.event_type == "repayment"]
    assert calculate_kpis(no_attempts)["disbursement_success_rate"] is None


def test_date_and_category_filters_apply_as_and(data):
    filtered = filter_transactions(data, "2024-01-01", "2024-01-31", loan_types=["Home"], channels=["UPI"])
    assert filtered.transaction_id.tolist() == ["TX001"]


def test_monthly_summary_fills_gaps_and_reconciles(data):
    summary = monthly_summary(data)
    assert len(summary) == 3
    assert summary.loc[summary.month.dt.month.eq(1), "disbursed_amount"].iloc[0] == 10_000
    assert summary.loc[summary.month.dt.month.eq(2), "disbursed_amount"].iloc[0] == 0
    assert summary.disbursed_amount.sum() == 35_000
    assert summary.disbursement_count.sum() == 2


def test_category_outcomes_and_failure_reason_aggregates(data):
    by_type = category_summary(data, "loan_type")
    assert by_type.disbursed_amount.sum() == 35_000
    outcomes = outcome_summary(data)
    assert outcomes.transaction_count.sum() == len(data)
    reasons = failure_reason_summary(data)
    assert reasons.iloc[0].failure_reason == "Compliance review"
    assert reasons.iloc[0].transaction_count == 1


def test_unsupported_aggregate_dimension_is_rejected(data):
    with pytest.raises(ValueError, match="Unsupported dimension"):
        category_summary(data, "customer_id")
