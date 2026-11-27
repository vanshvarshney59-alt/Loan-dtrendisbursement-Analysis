"""Add the final public links to the project README."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "README.md"
text = path.read_text(encoding="utf-8-sig")
text = text.replace(
    "Repository was initialized in this folder. Commit and tag history are local until a remote is configured. Repository name requested by the academic brief: `mca2-da-loan-disbursement-trend-analysis`.",
    "The project is published in the learner's GitHub repository on branch `master` with release tag `d17-v1.0.0`.",
)
text = text.replace("\\n## Published project links\\n\\n", "\n## Published project links\n\n")
text = text.replace("\\n", "\n")
path.write_text(text, encoding="utf-8")
