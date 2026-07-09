#!/usr/bin/env python3
"""
Deterministic renderer for the tax-audit-workpaper skill.

Takes a single structured JSON file describing a client's Form 3CA/3CB-3CD
clause-by-clause workpaper (produced by Claude after reading the client's
source documents) and renders it as:
  1. <slug>_tax_audit_workpaper.docx  - for copy/paste into the CA's tax
     audit software
  2. <slug>_tax_audit_workpaper.html  - a polished, reviewable HTML version

Usage:
    python3 render_output.py <input_workpaper.json> <output_dir>

The script owns all layout/formatting. It does not compute or judge
anything about tax law - that happens upstream when the JSON is built.
See references/workpaper_schema.md for the JSON shape this expects.
"""
import sys
import os
import json
import html as htmlmod
from datetime import datetime

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

STATUS_META = {
    "filled":         {"label": "",                                   "color_docx": None,               "css_class": "status-filled"},
    "missing":        {"label": "[MISSING — CONFIRM WITH CLIENT]", "color_docx": RGBColor(0xC0, 0x00, 0x00), "css_class": "status-missing"},
    "judgment":       {"label": "[JUDGMENT CALL — CA TO CONFIRM]", "color_docx": RGBColor(0xB8, 0x6A, 0x00), "css_class": "status-judgment"},
    "not_applicable": {"label": "[N/A]",                               "color_docx": RGBColor(0x70, 0x70, 0x70), "css_class": "status-na"},
}

# Canonical clause checklist used only to warn about omissions - does not
# block rendering. Keep numbers as strings to match sub-clause labels like "8a", "21(b)".
# NOTE: Clauses 28 and 29 (Sec 56(2)(viia)/(viib)) were DELETED from Form 3CD by
# CBDT Notification No. 23/2025 dated 28-Mar-2025, effective for audit reports signed
# on/after 1-Apr-2025 - i.e. they no longer exist in the AY 2026-27 form. Left out here
# deliberately; do not re-add without checking references/clauses-27-to-35.md first.
# NOTE: Clause 21 is the one clause reported as separate lettered sub-clauses
# (21(a) through 21(i)) rather than a single number - matches how
# references/clauses-18-to-26.md and the official schema both structure it. Every
# other multi-part clause (9, 11, 13, 20, 26, 31, 34, etc.) stays a single entry
# with its sub-items folded into that one clause's answer/table/notes.
CANONICAL_CLAUSES = [
    "1","2","3","4","5","6","7","8","8a",
    "9","10","11","12","13","14","15","16","17",
    "18","19","20",
    "21(a)","21(b)","21(c)","21(d)","21(e)","21(f)","21(g)","21(h)","21(i)",
    "22","23","24","25","26",
    "27","29A","29B","30","30A","30B","30C",
    "31","32","33","34","35","36","36A","36B","37","38","39",
    "40","41","42","43","44",
]


def slugify(name):
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")[:60] or "client"


def cell_set_shading(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)


# ---------------------------------------------------------------------------
# DOCX rendering
# ---------------------------------------------------------------------------

def render_docx(data, out_path):
    doc = Document()

    for section in doc.sections:
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    client = data.get("client", {})
    form_type = data.get("form_type", "3CB")

    title = doc.add_heading(f"Tax Audit Workpaper — Form {form_type}-3CD", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph(f"Draft prepared {datetime.now().strftime('%d-%b-%Y')} — for CA review before filing")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].italic = True

    doc.add_heading("Client Details", level=1)
    table = doc.add_table(rows=0, cols=2)
    table.style = "Light Grid Accent 1"
    for key, val in client.items():
        row = table.add_row().cells
        row[0].text = key.replace("_", " ").title()
        row[1].text = "" if val is None else str(val)

    # Review summary dashboard
    counts = {"filled": 0, "missing": 0, "judgment": 0, "not_applicable": 0}
    clauses = data.get("clauses", [])
    for c in clauses:
        counts[c.get("status", "filled")] = counts.get(c.get("status", "filled"), 0) + 1

    doc.add_heading("Review Summary", level=1)
    sp = doc.add_paragraph()
    sp.add_run(
        f"{len(clauses)} clauses drafted — "
        f"{counts.get('filled',0)} filled, "
        f"{counts.get('judgment',0)} flagged for CA judgment, "
        f"{counts.get('missing',0)} missing data, "
        f"{counts.get('not_applicable',0)} not applicable."
    ).bold = True

    missing_nums = [c["number"] for c in clauses if c.get("status") == "missing"]
    judgment_nums = [c["number"] for c in clauses if c.get("status") == "judgment"]
    if missing_nums:
        doc.add_paragraph(f"Clauses with missing data: {', '.join(missing_nums)}")
    if judgment_nums:
        doc.add_paragraph(f"Clauses needing CA judgment: {', '.join(judgment_nums)}")

    expected = set(CANONICAL_CLAUSES)
    present = set(c["number"] for c in clauses)
    omitted = sorted(expected - present, key=lambda x: CANONICAL_CLAUSES.index(x))
    if omitted:
        warn = doc.add_paragraph()
        warn.add_run(
            f"⚠ {len(omitted)} standard Form 3CD clause(s) do not appear in this draft at all "
            f"(not even as N/A): {', '.join(omitted)}. Confirm whether these were deliberately "
            f"skipped or missed."
        ).font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    doc.add_page_break()
    doc.add_heading("Clause-by-Clause Workpaper", level=1)

    for c in clauses:
        status = c.get("status", "filled")
        meta = STATUS_META.get(status, STATUS_META["filled"])

        h = doc.add_heading(f"Clause {c['number']} — {c.get('title','')}", level=2)

        if meta["label"]:
            flag_p = doc.add_paragraph()
            run = flag_p.add_run(meta["label"])
            run.bold = True
            if meta["color_docx"]:
                run.font.color.rgb = meta["color_docx"]

        answer = c.get("answer")
        if answer:
            ap = doc.add_paragraph(str(answer))

        rows = c.get("table")
        if rows:
            headers = list(rows[0].keys()) if isinstance(rows[0], dict) else None
            t = doc.add_table(rows=0, cols=len(headers) if headers else len(rows[0]))
            t.style = "Light Grid Accent 1"
            if headers:
                hdr = t.add_row().cells
                for i, hcol in enumerate(headers):
                    hdr[i].text = str(hcol)
                    for p in hdr[i].paragraphs:
                        for r in p.runs:
                            r.bold = True
                    cell_set_shading(hdr[i], "D9E1F2")
                for row in rows:
                    cells = t.add_row().cells
                    for i, hcol in enumerate(headers):
                        cells[i].text = "" if row.get(hcol) is None else str(row.get(hcol))
            else:
                for row in rows:
                    cells = t.add_row().cells
                    for i, v in enumerate(row):
                        cells[i].text = "" if v is None else str(v)

        notes = c.get("notes")
        if notes:
            np_ = doc.add_paragraph()
            nrun = np_.add_run(f"Note: {notes}")
            nrun.italic = True
            nrun.font.size = Pt(9.5)

    doc.save(out_path)


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Tax Audit Workpaper - {client_name}</title>
<style>
  :root {{
    --bg: #ffffff; --fg: #1a1a1a; --muted: #666; --border: #ddd;
    --header-bg: #1f3a5f; --header-fg: #ffffff;
    --filled: #1a7a3c; --missing: #c00000; --judgment: #b86a00; --na: #707070;
    --card-bg: #f7f8fa;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#12151a; --fg:#e8e8e8; --muted:#9aa0a6; --border:#333;
      --header-bg:#16324f; --header-fg:#eef4ff; --card-bg:#1b1f26; }}
  }}
  :root[data-theme="dark"] {{ --bg:#12151a; --fg:#e8e8e8; --muted:#9aa0a6; --border:#333;
    --header-bg:#16324f; --header-fg:#eef4ff; --card-bg:#1b1f26; }}
  :root[data-theme="light"] {{ --bg:#ffffff; --fg:#1a1a1a; --muted:#666; --border:#ddd;
    --header-bg:#1f3a5f; --header-fg:#ffffff; --card-bg:#f7f8fa; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg); font-family: "Segoe UI", Arial, sans-serif; line-height:1.5; }}
  header.page {{ background:var(--header-bg); color:var(--header-fg); padding:2rem 1.5rem; }}
  header.page h1 {{ margin:0 0 .25rem 0; font-size:1.5rem; }}
  header.page p {{ margin:0; opacity:.85; font-size:.9rem; }}
  .wrap {{ max-width: 980px; margin: 0 auto; padding: 1.5rem; }}
  .client-card, .summary-card {{ background:var(--card-bg); border:1px solid var(--border); border-radius:8px; padding:1rem 1.25rem; margin-bottom:1.5rem; }}
  .client-card table {{ width:100%; border-collapse:collapse; }}
  .client-card td {{ padding:.25rem .5rem; vertical-align:top; }}
  .client-card td:first-child {{ color:var(--muted); width:220px; }}
  .summary-pills {{ display:flex; gap:.75rem; flex-wrap:wrap; margin-top:.5rem; }}
  .pill {{ border-radius:999px; padding:.25rem .75rem; font-size:.85rem; font-weight:600; }}
  .pill.filled {{ background:rgba(26,122,60,.15); color:var(--filled); }}
  .pill.missing {{ background:rgba(192,0,0,.15); color:var(--missing); }}
  .pill.judgment {{ background:rgba(184,106,0,.15); color:var(--judgment); }}
  .pill.na {{ background:rgba(112,112,112,.15); color:var(--na); }}
  .omitted-warning {{ border:1px solid var(--missing); background:rgba(192,0,0,.08); border-radius:8px; padding:.75rem 1rem; margin-bottom:1.5rem; color:var(--missing); font-size:.9rem; }}
  nav.toc {{ columns:3; column-gap:1rem; font-size:.85rem; margin-bottom:2rem; }}
  nav.toc a {{ color:var(--fg); text-decoration:none; display:block; padding:.15rem 0; border-bottom:1px dotted transparent; }}
  nav.toc a:hover {{ border-bottom-color:var(--muted); }}
  section.clause {{ border:1px solid var(--border); border-radius:8px; padding:1.25rem 1.5rem; margin-bottom:1.25rem; scroll-margin-top:1rem; }}
  section.clause h2 {{ margin:0 0 .5rem 0; font-size:1.05rem; }}
  .badge {{ display:inline-block; font-weight:700; font-size:.8rem; padding:.15rem .6rem; border-radius:4px; margin-bottom:.5rem; }}
  .status-missing .badge {{ color:#fff; background:var(--missing); }}
  .status-judgment .badge {{ color:#fff; background:var(--judgment); }}
  .status-na .badge {{ color:#fff; background:var(--na); }}
  .answer {{ white-space:pre-wrap; }}
  table.data {{ width:100%; border-collapse:collapse; margin-top:.75rem; font-size:.9rem; overflow-x:auto; display:block; }}
  table.data th, table.data td {{ border:1px solid var(--border); padding:.4rem .6rem; text-align:left; }}
  table.data th {{ background:var(--card-bg); }}
  .note {{ color:var(--muted); font-size:.85rem; margin-top:.6rem; font-style:italic; }}
  footer {{ text-align:center; color:var(--muted); font-size:.8rem; padding:2rem 1rem; }}
</style>
</head>
<body>
<header class="page">
  <h1>Tax Audit Workpaper &mdash; Form {form_type}-3CD</h1>
  <p>Draft prepared {gen_date} &middot; for CA review before filing &middot; not a final report</p>
</header>
<div class="wrap">
  <div class="client-card">
    <table>{client_rows}</table>
  </div>
  <div class="summary-card">
    <strong>{n_clauses} clauses drafted</strong>
    <div class="summary-pills">
      <span class="pill filled">{n_filled} filled</span>
      <span class="pill judgment">{n_judgment} judgment calls</span>
      <span class="pill missing">{n_missing} missing data</span>
      <span class="pill na">{n_na} not applicable</span>
    </div>
  </div>
  {omitted_html}
  <nav class="toc">{toc_html}</nav>
  {clauses_html}
</div>
<footer>Generated by tax-audit-workpaper skill &middot; verify every flagged item before filing</footer>
</body>
</html>
"""


def esc(v):
    return htmlmod.escape(str(v)) if v is not None else ""


def render_html(data, out_path):
    client = data.get("client", {})
    form_type = data.get("form_type", "3CB")
    clauses = data.get("clauses", [])

    client_rows = "".join(
        f"<tr><td>{esc(k.replace('_',' ').title())}</td><td>{esc(v)}</td></tr>"
        for k, v in client.items()
    )

    counts = {"filled": 0, "missing": 0, "judgment": 0, "not_applicable": 0}
    for c in clauses:
        counts[c.get("status", "filled")] = counts.get(c.get("status", "filled"), 0) + 1

    expected = set(CANONICAL_CLAUSES)
    present = set(c["number"] for c in clauses)
    omitted = sorted(expected - present, key=lambda x: CANONICAL_CLAUSES.index(x))
    omitted_html = ""
    if omitted:
        omitted_html = (
            f'<div class="omitted-warning">&#9888; {len(omitted)} standard Form 3CD clause(s) do not '
            f'appear in this draft at all (not even as N/A): {esc(", ".join(omitted))}. '
            f'Confirm whether these were deliberately skipped or missed.</div>'
        )

    toc_html = "".join(
        f'<a href="#clause-{esc(c["number"])}">Clause {esc(c["number"])} &mdash; {esc(c.get("title",""))}</a>'
        for c in clauses
    )

    clause_blocks = []
    for c in clauses:
        status = c.get("status", "filled")
        meta = STATUS_META.get(status, STATUS_META["filled"])
        badge = f'<div class="badge">{esc(meta["label"])}</div>' if meta["label"] else ""
        answer_html = f'<div class="answer">{esc(c.get("answer",""))}</div>' if c.get("answer") else ""

        table_html = ""
        rows = c.get("table")
        if rows:
            if isinstance(rows[0], dict):
                headers = list(rows[0].keys())
                thead = "".join(f"<th>{esc(h)}</th>" for h in headers)
                trs = "".join(
                    "<tr>" + "".join(f"<td>{esc(row.get(h))}</td>" for h in headers) + "</tr>"
                    for row in rows
                )
            else:
                thead = ""
                trs = "".join(
                    "<tr>" + "".join(f"<td>{esc(v)}</td>" for v in row) + "</tr>"
                    for row in rows
                )
            table_html = f'<table class="data"><thead><tr>{thead}</tr></thead><tbody>{trs}</tbody></table>'

        note_html = f'<div class="note">Note: {esc(c.get("notes"))}</div>' if c.get("notes") else ""

        clause_blocks.append(
            f'<section class="clause {meta["css_class"]}" id="clause-{esc(c["number"])}">'
            f'<h2>Clause {esc(c["number"])} &mdash; {esc(c.get("title",""))}</h2>'
            f'{badge}{answer_html}{table_html}{note_html}'
            f'</section>'
        )

    html_out = HTML_TEMPLATE.format(
        client_name=esc(client.get("name", "Client")),
        form_type=esc(form_type),
        gen_date=datetime.now().strftime("%d-%b-%Y"),
        client_rows=client_rows,
        n_clauses=len(clauses),
        n_filled=counts.get("filled", 0),
        n_judgment=counts.get("judgment", 0),
        n_missing=counts.get("missing", 0),
        n_na=counts.get("not_applicable", 0),
        omitted_html=omitted_html,
        toc_html=toc_html,
        clauses_html="\n".join(clause_blocks),
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 render_output.py <input_workpaper.json> <output_dir>", file=sys.stderr)
        sys.exit(1)

    in_path, out_dir = sys.argv[1], sys.argv[2]
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(out_dir, exist_ok=True)
    slug = slugify(data.get("client", {}).get("name", "client"))
    docx_path = os.path.join(out_dir, f"{slug}_tax_audit_workpaper.docx")
    html_path = os.path.join(out_dir, f"{slug}_tax_audit_workpaper.html")

    render_docx(data, docx_path)
    render_html(data, html_path)

    print(f"Written: {docx_path}")
    print(f"Written: {html_path}")


if __name__ == "__main__":
    main()
