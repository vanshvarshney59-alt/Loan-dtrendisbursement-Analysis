"""Compile the project Markdown sources and build the RTM workbook and ABES deck."""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from pptx import Presentation
from pptx.dml.color import RGBColor as PPTColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches as PptInches, Pt as PptPt


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "deliverables" / "source"
OUT = ROOT / "deliverables"
NAVY = "17365D"
BLUE = "2563EB"
PALE = "EAF1F8"
DOCS = {
    "01_Project_Understanding": "01_Project_Understanding.docx",
    "02_HMW_Statement": "02_HMW_Statement.docx",
    "03_Needs_Analysis_Business_Requirements": "03_Needs_Analysis_Business_Requirements.docx",
    "04_Requirements_Traceability_Matrix": "04_Requirements_Traceability_Matrix.docx",
    "05_Business_Requirements_Document": "05_Business_Requirements_Document.docx",
    "06_Product_Requirements_Document": "06_Product_Requirements_Document.docx",
    "07_Technical_Business_Document": "07_Technical_Business_Document.docx",
    "08_Database_Design": "08_Database_Design.docx",
    "09_ER_Diagram": "09_ER_Diagram.docx",
    "10_Synthetic_Dataset_Generation": "10_Synthetic_Dataset_Generation.docx",
    "11_User_Stories": "11_User_Stories.docx",
    "12_UI_Framework": "12_UI_Framework.docx",
    "13_Test_Cases": "13_Test_Cases.docx",
    "14_Build_Plan_ID": "14_Build_Plan_ID.docx",
    "15_Build_Test_Fix": "15_Build_Test_Fix.docx",
    "16_Deployment_Plan": "16_Deployment_Plan.docx",
    "17_ABES_Project_Document": "17_ABES_Project_Document.docx",
    "18_ABES_Slide_Deck": "18_ABES_Slide_Deck.docx",
}


def shade_cell(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    tr_pr.append(repeat)


def inline_runs(paragraph, text: str, base_size: int = 10) -> None:
    pattern = re.compile(r"(\*\*.+?\*\*|`.+?`|\*.+?\*)")
    last = 0
    for match in pattern.finditer(text):
        if match.start() > last:
            run = paragraph.add_run(text[last:match.start()])
            run.font.size = Pt(base_size)
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2]); run.bold = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1]); run.font.name = "Consolas"; run.font.size = Pt(base_size - 1)
        else:
            run = paragraph.add_run(token[1:-1]); run.italic = True
        if run.font.size is None:
            run.font.size = Pt(base_size)
        last = match.end()
    if last < len(text):
        run = paragraph.add_run(text[last:]); run.font.size = Pt(base_size)


def markdown_table(lines: list[str], doc: Document) -> None:
    parsed = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    parsed = [row for row in parsed if not all(re.fullmatch(r":?-{2,}:?", cell.replace(" ", "")) for cell in row)]
    if not parsed:
        return
    cols = max(len(row) for row in parsed)
    table = doc.add_table(rows=0, cols=cols)
    table.style = "Light Shading Accent 1"
    table.autofit = True
    for row_index, values in enumerate(parsed):
        cells = table.add_row().cells
        if row_index == 0:
            set_repeat_table_header(table.rows[0])
        for index in range(cols):
            cell = cells[index]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cell.text = ""
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(2)
            value = values[index] if index < len(values) else ""
            inline_runs(paragraph, value, 8)
            if row_index == 0:
                shade_cell(cell, NAVY)
                for run in paragraph.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)


def add_page_field(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("D17 | Page ")
    run.font.size = Pt(8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def compile_docx(source: Path, target: Path) -> None:
    text = source.read_text(encoding="utf-8")
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7)
    sec.left_margin = Inches(.78); sec.right_margin = Inches(.78)
    # Use landscape for genuinely wide markdown tables.
    widest = max((len(line.strip().strip("|").split("|")) for line in text.splitlines() if line.strip().startswith("|") and "---" not in line), default=0)
    if widest > 5:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
        sec.left_margin = Inches(.55); sec.right_margin = Inches(.55)
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"; normal.font.size = Pt(10); normal.font.color.rgb = RGBColor(36, 54, 75)
    normal.paragraph_format.space_after = Pt(6)
    for name, size, color in (("Title", 25, NAVY), ("Heading 1", 16, NAVY), ("Heading 2", 12, BLUE), ("Heading 3", 11, NAVY)):
        style = doc.styles[name]
        style.font.name = "Aptos Display"; style.font.size = Pt(size); style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.keep_with_next = True
    for name in ("List Bullet", "List Number"):
        doc.styles[name].font.name = "Aptos"; doc.styles[name].font.size = Pt(10)
    header = sec.header.paragraphs[0]
    header.text = "ABES ENGINEERING COLLEGE  |  D17 LOAN DISBURSEMENT TREND ANALYSIS"
    header.style = "Caption"
    footer = sec.footer.paragraphs[0]
    add_page_field(footer)
    doc.core_properties.author = "Vansh Varshney"
    doc.core_properties.subject = "D17 academic project deliverable"
    doc.core_properties.title = source.stem.replace("_", " ")

    lines = text.splitlines()
    index = 0
    in_code = False
    while index < len(lines):
        raw = lines[index]
        line = raw.strip()
        if not line:
            index += 1; continue
        if line.startswith("```"):
            in_code = not in_code
            index += 1; continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index]); index += 1
            markdown_table(rows, doc)
            continue
        if in_code:
            para = doc.add_paragraph()
            para.paragraph_format.left_indent = Inches(.25)
            run = para.add_run(raw); run.font.name = "Consolas"; run.font.size = Pt(8)
            index += 1; continue
        if line.startswith("### "):
            p = doc.add_paragraph(style="Heading 3"); inline_runs(p, line[4:]); index += 1; continue
        if line.startswith("## "):
            p = doc.add_paragraph(style="Heading 1"); inline_runs(p, line[3:]); index += 1; continue
        if line.startswith("# "):
            p = doc.add_paragraph(style="Title"); inline_runs(p, line[2:], 22); index += 1; continue
        if line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet"); inline_runs(p, line[2:]); index += 1; continue
        if re.match(r"^\d+\.\s", line):
            p = doc.add_paragraph(style="List Number"); inline_runs(p, re.sub(r"^\d+\.\s", "", line)); index += 1; continue
        if line.startswith("> "):
            p = doc.add_paragraph(style="Quote"); inline_runs(p, line[2:]); index += 1; continue
        p = doc.add_paragraph(); inline_runs(p, line)
        index += 1
    target.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target)


ID_ROWS = [
    ("FR-001","HMW-003","SH-001, SH-005","OQ-002","F-001","BR-001, BR-009","Functional","Must","US-001","UI-06","TC-F-001, TC-T-002","T-003","Implemented / verified","13-test suite; deterministic seeded generator"),
    ("FR-002","HMW-003","SH-001","OQ-003","F-001","BR-006","Functional","Must","US-002","UI-04","TC-F-002, TC-F-003","T-004","Implemented / verified","Validator covers duplicates, parse, enum, event direction and relationships"),
    ("FR-003","HMW-003","SH-001","OQ-006","F-001","BR-009, BR-011","Functional","Must","US-003","UI-06","TC-F-004","T-005","Implemented / verified","SQLite idempotent schema/load/reload tests"),
    ("FR-004","HMW-002","SH-003, SH-004","OQ-007","F-004","BR-004, BR-008","Functional","Must","US-004","UI-01, UI-02, UI-03, UI-05","TC-F-005","T-008","Implemented / verified","AppTest six views; filter unit reconciliation"),
    ("FR-005","HMW-001","SH-003, SH-004","OQ-001, OQ-004","F-002","BR-002, BR-005, BR-007","Functional","Must","US-005","UI-01","TC-F-006, TC-F-007","T-006","Implemented / verified","KPI fixture verifies success/failure/repayment/reversal separation"),
    ("FR-006","HMW-001","SH-003","OQ-002, OQ-004","F-003","BR-002","Functional","Must","US-005","UI-01","TC-F-008","T-008","Implemented / verified","Monthly aggregation gap-fills and reconciles"),
    ("FR-007","HMW-001, HMW-002","SH-003","OQ-003, OQ-007","F-003, F-004","BR-003, BR-004","Functional","Must","US-006","UI-02","TC-F-008","T-009","Implemented / verified","Category amount/count aggregate reconciliation"),
    ("FR-008","HMW-002","SH-004","OQ-003","F-005","BR-005","Functional","Should","US-007","UI-03","TC-F-009","T-009","Implemented / verified","Failure reason aggregation unit test"),
    ("FR-009","HMW-003","SH-001","OQ-006","F-005","BR-009","Functional","Should","US-009","UI-05","TC-F-010","T-010","Built; download interaction pending","Filtered preview/export present; page rendered; download click not automated"),
    ("FR-010","HMW-003","SH-001, SH-005","OQ-005","F-005","BR-001, BR-006, BR-007","Functional","Must","US-008","UI-04","TC-F-011","T-009","Built; content assertion pending","Quality/methodology view rendered; manual copy review remains"),
    ("FR-011","HMW-003","SH-001","OQ-006","F-001","BR-009","Functional","Should","US-001","UI-04, UI-06","TC-F-012","T-010","Built; reload click pending","Reload callback implemented; not clicked in test harness"),
    ("FR-012","HMW-003","SH-001, SH-002, SH-005","OQ-009, OQ-010","F-006","BR-009, BR-010, BR-012","Functional","Must","US-010","UI-06","TC-T-006","T-013, T-014","Prepared; cloud deployment pending","README and Step 16; no authorized remote/account"),
    ("NFR-001","HMW-001, HMW-002","SH-003, SH-004","OQ-007","F-004","BR-008","Non-functional","Must","US-004","UI-01","TC-T-001","T-012","Measured pass (local)","App overview 3.398s; filtered calculations 0.097s after DB init; Windows/Python 3.14.3"),
    ("NFR-002","HMW-003","SH-001","OQ-002","F-001, F-002","BR-009","Non-functional","Must","US-001","UI-06","TC-F-001, TC-T-002","T-003, T-006","Verified","Seeded frame equality and deterministic KPI tests"),
    ("NFR-003","HMW-003","SH-001, SH-005","-","F-005","BR-001","Non-functional","Must","US-001, US-008","UI-01, UI-06","TC-T-003","T-004, T-009","Source inspection passed","Synthetic data and persistent app notice; no real personal data"),
    ("NFR-004","HMW-001","SH-003, SH-004","OQ-001, OQ-004","F-002","BR-007","Non-functional","Must","US-005","UI-01","TC-T-004","T-006, T-012","Implemented; manual review pending","KPI definitions/units in app; formal accessibility/content review remains"),
    ("NFR-005","HMW-003","SH-001","OQ-006","F-001","BR-011","Non-functional","Must","US-003","-","TC-T-005","T-005","Code review passed","Fixed SQL statements; UI filter values do not form SQL fragments"),
    ("NFR-006","HMW-003","SH-001","-","F-006","BR-009","Non-functional","Should","US-010","UI-06","TC-T-006","T-007, T-014","Module review passed","Separate data, database, analytics and UI modules"),
    ("NFR-007","HMW-003","SH-001, SH-002","-","F-006","BR-009","Non-functional","Must","US-010","-","TC-T-007","T-011","Verified","13 passed; 92% coverage across core loan_app modules"),
    ("NFR-008","HMW-002","SH-003, SH-004","OQ-007, OQ-008","F-004","BR-008","Non-functional","Should","US-004","UI-01","TC-T-008","T-007, T-012","Manual review pending","Responsive layout and native controls implemented; keyboard/screen-reader check not executed"),
]


def build_rtm() -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "RTM"
    headers = ["Requirement ID", "HMW ID", "SH ID", "OQ ID", "Feature ID", "BR ID", "Requirement Type", "Priority", "User Story ID", "UI ID", "Test Case ID", "Task ID", "Status", "Evidence / Notes"]
    sheet.append(headers)
    for row in ID_ROWS:
        sheet.append(row)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    table = Table(displayName="D17_RTM", ref=sheet.dimensions)
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    sheet.add_table(table)
    widths = [17,18,20,17,18,24,19,12,18,28,25,18,34,70]
    for index, width in enumerate(widths, 1):
        sheet.column_dimensions[chr(64 + index)].width = width
    for cell in sheet[1]:
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    sheet.row_dimensions[1].height = 32
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        sheet.row_dimensions[row[0].row].height = 54
    legend = workbook.create_sheet("ID Legend")
    legend.append(["Prefix", "Meaning", "Current range / usage"])
    items = [
        ("SH", "Stakeholder", "SH-001 to SH-005"), ("OQ", "Open question", "OQ-001 to OQ-010"),
        ("HMW", "How might we opportunity", "HMW-001 to HMW-003"), ("BR", "Business requirement", "BR-001 to BR-012"),
        ("F", "Product feature", "F-001 to F-006"), ("FR", "Functional requirement", "FR-001 to FR-012"),
        ("NFR", "Non-functional requirement", "NFR-001 to NFR-008"), ("US", "User story", "US-001 to US-010"),
        ("UI", "Application screen/view", "UI-01 to UI-06"), ("TC-F", "Functional test case", "TC-F-001 and onward"),
        ("TC-T", "Technical/non-functional test case", "TC-T-001 and onward"), ("T", "Build-plan task", "T-001 to T-014"),
    ]
    for item in items:
        legend.append(item)
    legend.freeze_panes = "A2"
    legend.column_dimensions["A"].width = 18; legend.column_dimensions["B"].width = 34; legend.column_dimensions["C"].width = 45
    log = workbook.create_sheet("Change Log")
    log.append(["Version", "Date", "Change", "Owner", "Approval status"])
    log.append(["1.0", "2026-11-21", "Initial full traceability baseline; implementation evidence added after Step 15.", "SH-001", "Mentor review pending"])
    log.column_dimensions["A"].width = 12; log.column_dimensions["B"].width = 16; log.column_dimensions["C"].width = 85; log.column_dimensions["D"].width = 18; log.column_dimensions["E"].width = 28
    for tab in workbook.worksheets[1:]:
        for cell in tab[1]:
            cell.fill = PatternFill("solid", fgColor=NAVY); cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        tab.auto_filter.ref = tab.dimensions
    workbook.save(OUT / "04_Requirements_Traceability_Matrix.xlsx")


def add_slide(prs, number, title, bullets, callout=None, image_path=None, image_left=True):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill; bg.solid(); bg.fore_color.rgb = PPTColor(245, 248, 252)
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, PptInches(.62))
    header.fill.solid(); header.fill.fore_color.rgb = PPTColor(23, 54, 93); header.line.fill.background()
    title_box = slide.shapes.add_textbox(PptInches(.55), PptInches(.07), PptInches(11.8), PptInches(.45))
    p = title_box.text_frame.paragraphs[0]; p.text = title; p.font.name = "Aptos Display"; p.font.size = PptPt(23); p.font.bold = True; p.font.color.rgb = PPTColor(255,255,255)
    body_left = PptInches(.72); body_width = PptInches(5.6 if image_path else 11.8)
    body_top = PptInches(1.05); body_height = PptInches(5.7)
    if image_path and image_left:
        slide.shapes.add_picture(str(image_path), PptInches(6.45), PptInches(1.2), width=PptInches(6.15))
    box = slide.shapes.add_textbox(body_left, body_top, body_width, body_height)
    tf = box.text_frame; tf.word_wrap = True; tf.margin_left = PptInches(.1); tf.margin_right = PptInches(.1)
    for i, bullet in enumerate(bullets):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = bullet; para.level = 0; para.font.name = "Aptos"; para.font.size = PptPt(19); para.font.color.rgb = PPTColor(36,54,75)
        para.space_after = PptPt(14); para.bullet = True
    if callout:
        y = PptInches(6.2)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PptInches(.72), y, PptInches(11.85), PptInches(.55))
        shape.fill.solid(); shape.fill.fore_color.rgb = PPTColor(225,238,251); shape.line.color.rgb = PPTColor(191,219,254)
        tfc = shape.text_frame; tfc.clear(); tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tfc.paragraphs[0]; p.text = callout; p.font.name="Aptos"; p.font.size=PptPt(12); p.font.color.rgb=PPTColor(23,54,93); p.alignment=PP_ALIGN.CENTER
    foot = slide.shapes.add_textbox(PptInches(.72), PptInches(7.08), PptInches(11.8), PptInches(.22))
    p = foot.text_frame.paragraphs[0]; p.text = f"D17 | Vansh Varshney | Synthetic demonstration data | {number:02d}"
    p.font.name="Aptos"; p.font.size=PptPt(9); p.font.color.rgb=PPTColor(100,116,139)
    return slide


def build_pptx() -> None:
    prs = Presentation()
    prs.slide_width = PptInches(13.333); prs.slide_height = PptInches(7.5)
    trend = ROOT / "outputs" / "loan_disbursement_trends.png"
    product = ROOT / "outputs" / "loan_type_breakdown.png"
    slides = [
        ("D17 | Loan Disbursement Trend Analysis", ["ABES Engineering College · MCA 2nd Year · Data Analyst", "Banking and Finance", "Vansh Varshney · Roll 2500320140161", "Mentor: Kalpana Dwivedi"], "Synthetic-data academic demonstration"),
        ("Context and problem", ["The assignment asks for loan disbursement trends over time and loan types.", "No real bank process or validated operational dataset was supplied.", "This project demonstrates transparent descriptive analysis, not a verified business finding."], "All sample records are fictional; they do not represent a lender."),
        ("Objectives and intended users", ["Create and document reproducible synthetic data.", "Define measurable KPIs and interactive views.", "Help SH-003 Branch Manager and SH-004 Risk & Operations Head explore patterns.", "Provide tests, deployment readiness and ABES submission artifacts."], None),
        ("Scope and safe use", ["In scope: synthetic transactions, Python, Streamlit, SQLite, Plotly and pytest.", "Out of scope: live bank integration, personal data, underwriting, credit decisions and causal claims.", "A persistent in-app notice labels data and results as synthetic."], "Never use the app for lending or borrower decisions."),
        ("Data model and event semantics", ["One row represents one transaction event.", "Events: disbursement, repayment or reversal; outcomes: success or failed.", "A disbursement KPI uses event_type=disbursement AND status=success.", "Credit/debit alone does not define a disbursement."], "Event count is not necessarily distinct loan count."),
        ("Method and architecture", ["Seeded generator creates fictitious entities and events.", "Validation checks types, IDs, event direction and relationships.", "SQLite persists data; shared metric service computes filtered aggregates.", "Streamlit renders filters, KPIs, Plotly charts and synthetic CSV export."], "No external bank system or API is connected."),
        ("KPI definitions", ["Successful disbursed amount = sum of successful disbursement event amounts.", "Disbursement count = successful event count.", "Transaction success rate includes every selected event type.", "Disbursement attempt success rate uses disbursement attempts only.", "Sample delinquency flag has no days-past-due definition."], None),
        ("Trend results | synthetic sample", ["Seed 42 · 12,000 valid events · 2021-01-01 to 2025-12-31.", "4,132 successful disbursement events.", "Total amount: INR 7,279,333,054.33.", "Highest generated month: May 2025, INR 187,898,932.46."], "These are generator outputs, not observed business behavior.", trend),
        ("Loan-type mix | synthetic sample", ["Home: INR 3,588,918,561.66 across 840 events.", "Business: INR 1,731,591,218.16 across 573 events.", "Vehicle: INR 1,136,144,487.98 across 875 events.", "The generator assigns different ticket ranges by type; totals are not evidence of demand."], "Compare amount and count together; do not infer product quality.", product),
        ("Data quality and verification", ["12,000 input rows; 12,000 valid; 0 rejected.", "14 automated tests passed; core-module coverage 92%.", "All six Streamlit views rendered in the headless AppTest smoke check.", "Local overview render 3.398 seconds; filtered calculations 0.097 seconds."], "One third-party pytest deprecation warning remains."),
        ("Deployment and limitations", ["Published on Streamlit Community Cloud.", "Live app: loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app", "Hosted SQLite storage may be ephemeral; app reloads the sample if missing.", "No authentication, production SLA, live data or validated risk measures."], "Use the live app link for the deployed academic demonstration."),
        ("Recommendations and close", ["Validate event mapping and reversal handling with a domain owner.", "Use real records only with authorization and privacy review.", "Define loan-level delinquency and aging before risk reporting.", "Review actual failure patterns only after the source data is validated.", "Thank you."], "Questions welcome"),
    ]
    for index, slide in enumerate(slides, 1):
        if len(slide) == 4:
            title, bullets, callout, image = slide
        else:
            title, bullets, callout = slide; image = None
        add_slide(prs, index, title, bullets, callout, image)
    prs.core_properties.title = "D17 Loan Disbursement Trend Analysis"
    prs.core_properties.author = "Vansh Varshney"
    prs.core_properties.subject = "ABES MCA Data Analyst project presentation"
    prs.save(OUT / "18_ABES_Slide_Deck.pptx")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, filename in DOCS.items():
        source = SRC / f"{stem}.md"
        if source.exists():
            compile_docx(source, OUT / filename)
        else:
            raise FileNotFoundError(source)
    # Also keep the original Step 1 file at the project root current.
    compile_docx(SRC / "01_Project_Understanding.md", ROOT / "01_Project_Understanding.docx")
    build_rtm()
    build_pptx()
    print(f"Built {len(DOCS)} Word files, RTM workbook, and ABES PowerPoint deck in {OUT}")


if __name__ == "__main__":
    main()
