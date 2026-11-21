from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"
PAGES = ["Overview", "Product & channel", "Transaction outcomes", "Data quality", "Transaction explorer", "About"]


def test_all_streamlit_views_render_without_exceptions(tmp_path, monkeypatch):
    monkeypatch.setenv("LOAN_DB_PATH", str(tmp_path / "app.sqlite"))
    app = AppTest.from_file(str(APP))
    for index, page in enumerate(PAGES):
        if index:
            app.radio[0].set_value(page)
        app.run(timeout=60)
        assert not app.exception, f"{page} raised: {app.exception}"
