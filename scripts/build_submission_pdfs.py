"""Build PDFs for the D17 code, report, and presentation using PyMuPDF."""
from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

import pymupdf as fitz
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
APP_URL = "https://loan-dtrendisbursement-analysis-eptjqtxqqd2gt8uwxvpln7.streamlit.app/"
GITHUB_URL = "https://github.com/vanshvarshney59-alt/Loan-dtrendisbursement-Analysis"


def code_pdf() -> None:
    files = [ROOT / "app.py", ROOT / "loan_trend_analysis.py"]
    files += sorted((ROOT / "loan_app").glob("*.py"))
    files += sorted((ROOT / "tests").glob("*.py"))
    files += [ROOT / "scripts" / "build_office_deliverables.py"]
    files += [ROOT / "scripts" / "build_submission_pdfs.py"]
    doc = fitz.open()
    page = None
    y = 0
    page_no = 0

    def new_page(filename: str, line_no: int) -> None:
        nonlocal page, y, page_no
        page = doc.new_page(width=612, height=792)
        page_no += 1
        page.draw_rect(fitz.Rect(0, 0, 612, 44), color=None, fill=(0.07, 0.16, 0.29))
        page.insert_text((34, 28), "D17 | SOURCE CODE", fontname="hebo", fontsize=10, color=(1, 1, 1))
        page.insert_text((34, 65), filename, fontname="hebo", fontsize=11, color=(0.07, 0.16, 0.29))
        page.insert_text((34, 78), f"Starting at source line {line_no}", fontname="helv", fontsize=7, color=(0.35, 0.4, 0.48))
        y = 96
        page.insert_text((34, 770), f"Vansh Varshney | D17 | Page {page_no}", fontname="helv", fontsize=7, color=(0.4, 0.43, 0.48))

    for file in files:
        lines = file.read_text(encoding="utf-8").splitlines() or [""]
        rel = file.relative_to(ROOT).as_posix()
        new_page(rel, 1)
        for source_no, source in enumerate(lines, start=1):
            # Courier at 7.2 pt fits about 110 characters in the code area.
            visual = textwrap.wrap(source, width=110, replace_whitespace=False, drop_whitespace=False) or [""]
            for part in visual:
                if y > 752:
                    new_page(rel, source_no)
                page.insert_text((35, y), f"{source_no:4d}  {part}", fontname="cour", fontsize=7.2, color=(0.12, 0.16, 0.22))
                y += 9.4
    doc.set_metadata({"title": "D17 Loan Disbursement Trend Analysis - Source Code", "author": "Vansh Varshney"})
    doc.save(OUT / "Source_Code.pdf", garbage=4, deflate=True)


def report_pdf() -> None:
    source = (OUT / "source" / "17_ABES_Project_Document.md").read_text(encoding="utf-8-sig")
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    y = 48
    page_no = 1

    def fresh_page() -> None:
        nonlocal page, y, page_no
        page = doc.new_page(width=595, height=842)
        page_no += 1
        y = 48

    def write(text: str, *, size: float = 10, font: str = "helv", color=(0.18, 0.22, 0.29), leading: float | None = None) -> None:
        nonlocal y
        leading = leading or size * 1.4
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"`([^`]+)`", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 (\2)", text)
        width = 90 if size <= 10 else 64
        lines = textwrap.wrap(text, width=width, break_long_words=True, break_on_hyphens=False) or [""]
        for ln in lines:
            if y > 790:
                fresh_page()
            page.insert_text((48, y), ln, fontname=font, fontsize=size, color=color)
            y += leading

    # Cover block
    page.draw_rect(fitz.Rect(0, 0, 595, 225), color=None, fill=(0.07, 0.16, 0.29))
    page.insert_text((48, 72), "ABES ENGINEERING COLLEGE", fontname="hebo", fontsize=13, color=(0.72, 0.84, 0.96))
    page.insert_textbox(fitz.Rect(48, 95, 545, 163), "Loan Disbursement\nTrend Analysis", fontname="hebo", fontsize=25, lineheight=1.15, color=(1, 1, 1))
    page.insert_text((48, 194), "Project Report | MCA 2nd Year | Data Analyst", fontname="helv", fontsize=11, color=(0.88, 0.92, 0.97))
    y = 260
    for raw in source.splitlines():
        line = raw.strip()
        if not line or line.startswith("> The official ABES"):
            continue
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            y += 7
            write(line[3:], size=16, font="hebo", color=(0.07, 0.16, 0.29), leading=22)
        elif line.startswith("### "):
            write(line[4:], size=12, font="hebo", color=(0.12, 0.28, 0.46), leading=17)
        elif line.startswith(("- ", "• ")):
            write("-  " + line[2:], size=9.5, leading=13)
        elif re.match(r"\d+\. ", line):
            write(line, size=9.5, leading=13)
        else:
            write(line, size=9.5, leading=13)
        y += 3
    # End sheet with clearly visible clickable project links.
    if y > 700:
        fresh_page()
    page.draw_line((48, y + 8), (547, y + 8), color=(0.75, 0.8, 0.86), width=0.8)
    page.insert_text((48, y + 28), "LIVE STREAMLIT DASHBOARD", fontname="hebo", fontsize=9, color=(0.07, 0.16, 0.29))
    rect = fitz.Rect(48, y + 36, 547, y + 54)
    page.insert_textbox(rect, APP_URL, fontname="helv", fontsize=8.5, color=(0.05, 0.34, 0.64))
    page.insert_link({"kind": fitz.LINK_URI, "from": rect, "uri": APP_URL})
    rect2 = fitz.Rect(48, y + 58, 547, y + 76)
    page.insert_textbox(rect2, GITHUB_URL, fontname="helv", fontsize=8.5, color=(0.05, 0.34, 0.64))
    page.insert_link({"kind": fitz.LINK_URI, "from": rect2, "uri": GITHUB_URL})
    for n, p in enumerate(doc, 1):
        p.insert_text((48, 824), f"Vansh Varshney | D17 | Page {n}", fontname="helv", fontsize=7, color=(0.4, 0.43, 0.48))
    doc.set_metadata({"title": "D17 Loan Disbursement Trend Analysis - Project Report", "author": "Vansh Varshney"})
    doc.save(OUT / "17_ABES_Project_Document.pdf", garbage=4, deflate=True)


def slides_pdf() -> None:
    prs = Presentation(OUT / "18_ABES_Slide_Deck.pptx")
    width, height = 960, 540
    doc = fitz.open()
    for idx, slide in enumerate(prs.slides, start=1):
        page = doc.new_page(width=width, height=height)
        page.draw_rect(page.rect, color=None, fill=(0.96, 0.97, 0.985))
        page.draw_rect(fitz.Rect(0, 0, width, 94), color=None, fill=(0.07, 0.16, 0.29))
        title = next((s.text.strip() for s in slide.shapes if s.has_text_frame and s.text.strip() and s.top < 1_300_000), f"D17 | Slide {idx}")
        page.insert_textbox(fitz.Rect(44, 26, 910, 82), title, fontname="hebo", fontsize=24, color=(1, 1, 1))
        pictures = [s for s in slide.shapes if s.shape_type == 13]
        picture = pictures[0] if pictures else None
        body_rect = fitz.Rect(56, 126, 570 if picture else 900, 450)
        y = body_rect.y0
        for shape in slide.shapes:
            if not shape.has_text_frame or shape.text.strip() == title:
                continue
            st = shape.text.strip()
            if not st or st.startswith("D17 | Vansh"):
                continue
            if shape.top < 700_000:
                continue
            # Preserve paragraphs as separate bullets and remove legacy symbol-font artifacts.
            for para in shape.text_frame.paragraphs:
                text = para.text.strip().replace("\ufffd", "")
                text = re.sub(r"^[\W_]+", "", text)
                if not text or text.startswith("D17 | Vansh"):
                    continue
                lines = textwrap.wrap(text, width=58 if picture else 90)
                block = "\n".join(("* " if para.level == 0 else "- ") + ln if j == 0 else "   " + ln for j, ln in enumerate(lines))
                box = fitz.Rect(body_rect.x0, y, body_rect.x1, min(y + 70, 490))
                page.insert_textbox(box, block, fontname="helv", fontsize=15, lineheight=1.25, color=(0.13, 0.18, 0.27))
                y += max(32, (len(lines) + 1) * 22)
                if y > 450:
                    break
        if picture:
            rect = fitz.Rect(picture.left / 914400 * 72 + 130, 145, 910, 425)
            try:
                pix = fitz.Pixmap(picture.image.blob)
                page.insert_image(rect, pixmap=pix, keep_proportion=True)
            except Exception:
                pass
        if idx == 11:
            link_rect = fitz.Rect(54, 448, 905, 478)
            page.insert_textbox(link_rect, APP_URL, fontname="hebo", fontsize=13, color=(0.05, 0.34, 0.64))
            page.insert_link({"kind": fitz.LINK_URI, "from": link_rect, "uri": APP_URL})
        page.draw_line((44, 505), (916, 505), color=(0.78, 0.82, 0.88), width=0.8)
        page.insert_text((44, 526), "Vansh Varshney | D17 | Synthetic demonstration data", fontname="helv", fontsize=9, color=(0.35, 0.4, 0.48))
        page.insert_text((890, 526), f"{idx:02d}", fontname="hebo", fontsize=9, color=(0.35, 0.4, 0.48))
    doc.set_metadata({"title": "D17 Loan Disbursement Trend Analysis - Presentation", "author": "Vansh Varshney"})
    doc.save(OUT / "18_ABES_Slide_Deck.pdf", garbage=4, deflate=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    code_pdf()
    report_pdf()
    slides_pdf()
    print("Created Source_Code.pdf, 17_ABES_Project_Document.pdf, and 18_ABES_Slide_Deck.pdf")


if __name__ == "__main__":
    main()
