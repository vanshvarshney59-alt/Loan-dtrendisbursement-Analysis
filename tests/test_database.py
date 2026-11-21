import sqlite3

import pytest

from loan_app.database import initialize_database, read_metadata, read_transactions, replace_dataset
from tests.helpers import mini_frame


def test_database_load_is_idempotent_and_preserves_event_grain(tmp_path):
    path = tmp_path / "test.sqlite"
    initialize_database(path)
    initialize_database(path)
    replace_dataset(path, mini_frame(), {"seed": 13}, "test synthetic")
    first = read_transactions(path)
    replace_dataset(path, mini_frame(), {"seed": 13}, "test synthetic")
    second = read_transactions(path)
    assert len(first) == len(second) == 5
    assert second.transaction_id.is_unique
    assert read_metadata(path)["seed"] == 13
    assert second.event_type.tolist().count("reversal") == 1


def test_invalid_relationship_rolls_back_replacement(tmp_path):
    path = tmp_path / "test.sqlite"
    replace_dataset(path, mini_frame(), {"seed": 13})
    before = read_transactions(path)
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TRIGGER reject_test_event BEFORE INSERT ON transaction_event
            WHEN NEW.transaction_id='TX001' BEGIN SELECT RAISE(ABORT,'forced rollback check'); END""")
    with pytest.raises(sqlite3.IntegrityError):
        replace_dataset(path, mini_frame(), {"seed": 99})
    after = read_transactions(path)
    assert after.transaction_id.tolist() == before.transaction_id.tolist()
