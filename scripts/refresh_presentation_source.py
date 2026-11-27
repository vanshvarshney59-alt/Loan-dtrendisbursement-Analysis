"""Refresh the final metrics and hosted link in the generated ABES deck."""
from pathlib import Path

path = Path(__file__).with_name("build_office_deliverables.py")
lines = path.read_text(encoding="utf-8-sig").splitlines()
updated = []
for line in lines:
    if "13 automated tests passed; core-module coverage 92%." in line:
        line = line.replace("13 automated tests passed", "14 automated tests passed")
    if "para.text =" in line and "+ bullet;" in line:
        line = "        para.text = bullet;" + line.split(";", 1)[1]
    if "Deployment and limitations" in line:
        line = (
            '        ("Deployment and limitations", '
            '["Published on Streamlit Community Cloud.", '
            '"Live app: loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app", '
            '"Hosted SQLite storage may be ephemeral; app reloads the sample if missing.", '
            '"No authentication, production SLA, live data or validated risk measures."], '
            '"Use the live app link for the deployed academic demonstration."),'
        )
    line = line.replace("Â·", "|")
    updated.append(line)
path.write_text("\n".join(updated) + "\n", encoding="utf-8")
