#!/usr/bin/env python3
"""
Deterministic renderer for the tax-audit-workpaper skill (v1.0).

    python3 render_output.py <workpaper.json> <output_dir>

Produces three files in <output_dir>:
  <slug>_tax_audit_workpaper.docx   clause-by-clause workpaper (copy answers into tax audit software)
  <slug>_tax_audit_workpaper.html   same content, colour-coded, filterable, printable
  <slug>_review_register.xlsx       CA review register: sign-off columns, impact summary,
                                    reconciliations, client query tracker, document index

The script only lays data out. It does not compute or judge tax positions —
that happens upstream when the JSON is built (see references/workpaper_schema.md).
It runs validate_workpaper.py first and prints the warnings; it refuses to render
only on hard errors (pass --force to render anyway).
"""
import html as htmlmod
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wp_common import (  # noqa: E402
    CANONICAL_CLAUSES, DEFAULT_PREPARER, SKILL_VERSION, clause_sort_key,
    fmt_inr, impacts_of, slugify, to_number,
)
from validate_workpaper import validate  # noqa: E402

STATUS_META = {
    "filled":         {"label": "",                                "short": "Filled",   "rgb": None,       "css": "status-filled",   "xl": "E2EFDA"},
    "judgment":       {"label": "[JUDGMENT CALL — CA TO CONFIRM]", "short": "Judgment", "rgb": "B86A00",   "css": "status-judgment", "xl": "FFE699"},
    "missing":        {"label": "[MISSING — CONFIRM WITH CLIENT]", "short": "Missing",  "rgb": "C00000",   "css": "status-missing",  "xl": "F8CBAD"},
    "not_applicable": {"label": "[N/A]",                           "short": "N/A",      "rgb": "707070",   "css": "status-na",       "xl": "EDEDED"},
}
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2, None: 3}


# ---------------------------------------------------------------------------
# Derived data shared by all three outputs
# ---------------------------------------------------------------------------

def prepare(data):
    clauses = data.get("clauses", [])
    counts = {k: 0 for k in STATUS_META}
    for c in clauses:
        counts[c.get("status", "filled")] = counts.get(c.get("status", "filled"), 0) + 1
    present = {str(c.get("number")) for c in clauses}
    omitted = [n for n in CANONICAL_CLAUSES if n not in present]

    impacts = []
    for c in clauses:
        for imp in impacts_of(c):
            amt = to_number(imp.get("amount")) or 0.0
            impacts.append({
                "clause": c.get("number"),
                "title": c.get("title", ""),
                "status": c.get("status", "filled"),
                "basis": imp.get("basis", ""),
                "description": imp.get("description", ""),
                "direction": imp.get("direction", "add"),
                "amount": amt,
                "signed": amt if imp.get("direction", "add") == "add" else -amt,
                "double_count_of": imp.get("double_count_of"),
            })
    net = sum(i["signed"] for i in impacts if not i["double_count_of"])
    confirmed = sum(i["signed"] for i in impacts if not i["double_count_of"] and i["status"] == "filled")

    attention = [c for c in clauses if c.get("status") in ("judgment", "missing")]
    attention.sort(key=lambda c: (
        PRIORITY_RANK.get(c.get("priority"), 3),
        -sum(to_number(i.get("amount")) or 0 for i in impacts_of(c)),
        clause_sort_key(c.get("number")),
    ))
    queries = [c for c in clauses if c.get("client_query")]
    preparer = dict(DEFAULT_PREPARER)
    preparer.update({k: v for k, v in (data.get("preparer") or {}).items() if v})
    return {
        "clauses": clauses, "counts": counts, "omitted": omitted, "impacts": impacts,
        "net_impact": net, "confirmed_impact": confirmed, "attention": attention,
        "queries": queries, "preparer": preparer,
        "recons": data.get("reconciliations") or [],
        "docs": (data.get("engagement") or {}).get("documents") or [],
        "engagement": data.get("engagement") or {},
        "gen_date": datetime.now().strftime("%d-%b-%Y"),
    }


ACRONYMS = {"pan": "PAN", "cin": "CIN", "gstin": "GSTIN", "tan": "TAN", "udin": "UDIN", "frn": "FRN", "llpin": "LLPIN", "ay": "AY", "itr": "ITR"}


def label(key):
    """client/engagement key -> display label, keeping acronyms upper-case."""
    return " ".join(ACRONYMS.get(w.lower(), w.capitalize()) for w in str(key).split("_"))


def first_sentence(text, limit=170):
    """First sentence of a note, capped at `limit` characters on a word boundary."""
    t = " ".join(str(text or "").split())
    m = re.search(r"(?<!Rs)(?<!No)(?<!\bs)(?<!u/s)\.\s+(?=[A-Z(])", t)
    if m and m.start() < limit:
        return t[: m.start() + 1]
    return t if len(t) <= limit else t[: t.rfind(" ", 0, limit)] + " …"


def table_rows(rows):
    """Normalise a clause table into (headers or None, list of row lists)."""
    if not rows:
        return None, []
    if isinstance(rows[0], dict):
        headers = list(rows[0].keys())
        return headers, [["" if r.get(h) is None else str(r.get(h)) for h in headers] for r in rows]
    return None, [["" if v is None else str(v) for v in r] for r in rows]


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------

def render_docx(data, d, out_path):
    from docx import Document
    from docx.enum.section import WD_ORIENT  # noqa: F401
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    def shade(cell, hex_color):
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hex_color)
        cell._tc.get_or_add_tcPr().append(shd)

    def add_table(headers, rows, widths=None, header_fill="D9E1F2"):
        ncols = len(headers) if headers else (len(rows[0]) if rows else 1)
        t = doc.add_table(rows=0, cols=ncols)
        t.style = "Table Grid"
        if headers:
            cells = t.add_row().cells
            for i, h in enumerate(headers):
                cells[i].text = str(h)
                for p in cells[i].paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.size = Pt(9)
                shade(cells[i], header_fill)
        for row in rows:
            cells = t.add_row().cells
            for i in range(ncols):
                cells[i].text = str(row[i]) if i < len(row) else ""
                for p in cells[i].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9)
        if widths:
            t.autofit = False
            grid = t._tbl.tblGrid
            for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
                if i < len(widths):
                    gc.set(qn("w:w"), str(int(widths[i] * 567)))
            for row in t.rows:
                for i, w in enumerate(widths):
                    if i < len(row.cells):
                        row.cells[i].width = Cm(w)
        doc.add_paragraph()
        return t

    doc = Document()
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2)
        s.top_margin = s.bottom_margin = Cm(1.8)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)

    client = data.get("client", {})
    form = data.get("form_type", "3CB")

    # Header / footer on every page
    sec = doc.sections[0]
    hp = sec.header.paragraphs[0]
    hp.text = f"{client.get('name', 'Client')} — Form {form}-3CD workpaper — AY {client.get('assessment_year', '')} — DRAFT FOR CA REVIEW"
    hp.runs[0].font.size = Pt(8)
    hp.runs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    fp = sec.footer.paragraphs[0]
    fp.text = f"Prepared by {d['preparer']['name']} | {d['preparer']['phone']} | {d['preparer']['url']}"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.runs[0].font.size = Pt(8)
    fp.runs[0].font.color.rgb = RGBColor(0x70, 0x70, 0x70)

    title = doc.add_heading(f"Tax Audit Workpaper — Form {form}-3CD", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph(f"Draft prepared {d['gen_date']} — for CA review before filing. Not a final report.")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.runs[0].italic = True

    doc.add_heading("Client details", level=1)
    add_table(None, [[label(k), "" if v is None else str(v)] for k, v in client.items()],
              widths=[5, 12])

    eng = d["engagement"]
    if eng:
        meta = [[label(k), str(v)] for k, v in eng.items() if k != "documents" and v]
        if meta:
            doc.add_heading("Engagement", level=1)
            add_table(None, meta, widths=[5, 12])

    # Review summary
    doc.add_heading("Review summary", level=1)
    c = d["counts"]
    p = doc.add_paragraph()
    p.add_run(f"{len(d['clauses'])} clauses drafted — {c['filled']} filled, {c['judgment']} judgment calls, "
              f"{c['missing']} missing data, {c['not_applicable']} not applicable.").bold = True
    if d["omitted"]:
        w = doc.add_paragraph()
        r = w.add_run(f"⚠ {len(d['omitted'])} standard Form 3CD clause(s) do not appear at all (not even as N/A): "
                      f"{', '.join(d['omitted'])}. Confirm whether these were deliberately skipped or missed.")
        r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    if d["attention"]:
        doc.add_heading("CA attention list (highest priority first)", level=2)
        rows = []
        for cl in d["attention"]:
            amt = sum(to_number(i.get("amount")) or 0 for i in impacts_of(cl))
            rows.append([cl["number"], cl.get("title", ""), STATUS_META[cl["status"]]["short"],
                         (cl.get("priority") or "").title(), fmt_inr(amt) if amt else "—",
                         first_sentence(cl.get("notes"))])
        add_table(["Clause", "Title", "Status", "Priority", "Impact (Rs.)", "Why it needs you"], rows,
                  widths=[1.3, 4.2, 1.7, 1.5, 2.1, 6.2])

    if d["impacts"]:
        doc.add_heading("Computation impact summary (draft)", level=2)
        rows = []
        for i in d["impacts"]:
            sign = "+" if i["direction"] == "add" else "−"
            rows.append([i["clause"], i["basis"], i["description"], STATUS_META[i["status"]]["short"],
                         f"{sign} {fmt_inr(i['amount'])}" + (" (shown elsewhere — not added again)" if i["double_count_of"] else "")])
        rows.append(["", "", "Net effect on total income (all items, excluding duplicates)", "", fmt_inr(d["net_impact"])])
        rows.append(["", "", "of which already 'filled' (no CA judgment pending)", "", fmt_inr(d["confirmed_impact"])])
        add_table(["Clause", "Section", "Item", "Status", "Amount (Rs.)"], rows, widths=[1.4, 2.4, 8, 1.8, 3.4])
        n = doc.add_paragraph("These are the adjustments the draft identifies for the income computation. They are "
                              "not a tax computation; judgment items may change after CA review.")
        n.runs[0].italic = True
        n.runs[0].font.size = Pt(9)

    if d["recons"]:
        doc.add_heading("Cross-document reconciliations", level=2)
        rows = [[r.get("item", ""), f"{r.get('source_a', '')}: {fmt_inr(r.get('amount_a'))}",
                 f"{r.get('source_b', '')}: {fmt_inr(r.get('amount_b'))}",
                 fmt_inr(r.get("difference")) if r.get("difference") not in (None, "") else "",
                 (r.get("status") or "").title(), r.get("explanation", "")] for r in d["recons"]]
        add_table(["Check", "Source A", "Source B", "Difference", "Result", "Explanation"], rows,
                  widths=[3, 3, 3, 2.1, 2.2, 3.7])

    doc.add_page_break()
    doc.add_heading("Clause-by-clause workpaper", level=1)
    for cl in d["clauses"]:
        st = cl.get("status", "filled")
        meta = STATUS_META.get(st, STATUS_META["filled"])
        doc.add_heading(f"Clause {cl['number']} — {cl.get('title', '')}", level=2)
        if meta["label"]:
            fpara = doc.add_paragraph()
            run = fpara.add_run(meta["label"])
            run.bold = True
            run.font.color.rgb = RGBColor.from_string(meta["rgb"])
            if cl.get("priority"):
                pr = fpara.add_run(f"   Priority: {cl['priority'].title()}")
                pr.font.size = Pt(9)
        if cl.get("answer"):
            for para in str(cl["answer"]).split("\n"):
                doc.add_paragraph(para)
        headers, rows = table_rows(cl.get("table"))
        if rows:
            add_table(headers, rows)
        for imp in impacts_of(cl):
            ip = doc.add_paragraph()
            sign = "Add back" if imp.get("direction", "add") == "add" else "Deduct"
            r = ip.add_run(f"Computation impact: {sign} Rs. {fmt_inr(imp.get('amount'))} — {imp.get('basis', '')}"
                           + (f" ({imp.get('description')})" if imp.get("description") else ""))
            r.bold = True
            r.font.size = Pt(9.5)
        if cl.get("notes"):
            np_ = doc.add_paragraph()
            nr = np_.add_run(f"Note: {cl['notes']}")
            nr.italic = True
            nr.font.size = Pt(9.5)
        if cl.get("sources"):
            sp = doc.add_paragraph()
            sr = sp.add_run("Source: " + "; ".join(str(s) for s in cl["sources"]))
            sr.font.size = Pt(8.5)
            sr.font.color.rgb = RGBColor(0x50, 0x50, 0x50)
        if cl.get("client_query"):
            qp = doc.add_paragraph()
            qr = qp.add_run(f"Client query: {cl['client_query']}")
            qr.font.size = Pt(9)
            qr.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    if d["queries"]:
        doc.add_page_break()
        doc.add_heading("Appendix A — Information required from the client", level=1)
        doc.add_paragraph("Please provide the following so we can complete the tax audit:")
        rows = [[str(k + 1), q["number"], q["client_query"]] for k, q in enumerate(d["queries"])]
        add_table(["#", "Clause", "Information / document required"], rows, widths=[0.8, 1.6, 14.6])

    if d["docs"]:
        doc.add_heading("Appendix B — Source documents relied on", level=1)
        rows = [[x.get("ref", ""), x.get("file", ""), x.get("description", "")] for x in d["docs"]]
        add_table(["Ref", "File", "Description"], rows, widths=[1.2, 5.5, 10.3])

    doc.add_paragraph()
    credit = doc.add_paragraph()
    credit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = credit.add_run(f"Workpaper prepared by {d['preparer']['name']}  |  {d['preparer']['phone']}  |  "
                        f"{d['preparer']['url']}  ·  tax-audit-workpaper skill v{SKILL_VERSION}")
    cr.italic = True
    cr.font.size = Pt(9)
    cr.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    doc.save(out_path)


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5f6368;--border:#dadce0;--hdr:#1f3a5f;--hdrfg:#fff;--card:#f7f8fa;
--filled:#1a7a3c;--missing:#c00000;--judgment:#a35d00;--na:#6b6b6b}
@media (prefers-color-scheme:dark){:root{--bg:#12151a;--fg:#e8e8e8;--muted:#9aa0a6;--border:#333;--hdr:#16324f;--card:#1b1f26}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:"Segoe UI",Arial,sans-serif;line-height:1.5}
header.page{background:var(--hdr);color:var(--hdrfg);padding:1.75rem 1.5rem}header.page h1{margin:0 0 .25rem;font-size:1.45rem}
header.page p{margin:0;opacity:.85;font-size:.9rem}.wrap{max-width:1040px;margin:0 auto;padding:1.5rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.25rem;margin-bottom:1.25rem}
.card h3{margin:.1rem 0 .6rem;font-size:1rem}.kv td{padding:.2rem .5rem;vertical-align:top}.kv td:first-child{color:var(--muted);width:210px}
.pills{display:flex;gap:.6rem;flex-wrap:wrap}.pill{border-radius:999px;padding:.25rem .8rem;font-size:.85rem;font-weight:600;border:0;cursor:pointer;font-family:inherit}
.pill.all{background:rgba(31,58,95,.12);color:var(--fg)}.pill.filled{background:rgba(26,122,60,.15);color:var(--filled)}
.pill.missing{background:rgba(192,0,0,.13);color:var(--missing)}.pill.judgment{background:rgba(184,106,0,.16);color:var(--judgment)}
.pill.na{background:rgba(112,112,112,.15);color:var(--na)}.pill.impact{background:rgba(70,40,160,.13);color:#5b3fc4}
.pill[aria-pressed=true]{outline:2px solid currentColor}
.warn{border:1px solid var(--missing);background:rgba(192,0,0,.07);border-radius:8px;padding:.75rem 1rem;margin-bottom:1.25rem;color:var(--missing);font-size:.9rem}
input.search{width:100%;padding:.5rem .75rem;border:1px solid var(--border);border-radius:6px;background:var(--bg);color:var(--fg);font-size:.95rem;margin:.75rem 0}
nav.toc{columns:3;column-gap:1rem;font-size:.82rem;margin-bottom:1.5rem}nav.toc a{color:var(--fg);text-decoration:none;display:block;padding:.1rem 0}
nav.toc a .dot{display:inline-block;width:.55rem;height:.55rem;border-radius:50%;margin-right:.35rem;background:var(--filled)}
nav.toc a.status-missing .dot{background:var(--missing)}nav.toc a.status-judgment .dot{background:var(--judgment)}nav.toc a.status-na .dot{background:var(--na)}
section.clause{border:1px solid var(--border);border-left:5px solid var(--filled);border-radius:8px;padding:1.1rem 1.4rem;margin-bottom:1rem;scroll-margin-top:1rem}
section.status-missing{border-left-color:var(--missing)}section.status-judgment{border-left-color:var(--judgment)}section.status-na{border-left-color:var(--na)}
section.clause h2{margin:0 0 .45rem;font-size:1.02rem}.badge{display:inline-block;font-weight:700;font-size:.76rem;padding:.12rem .55rem;border-radius:4px;margin:0 .4rem .45rem 0;color:#fff}
.status-missing .badge.st{background:var(--missing)}.status-judgment .badge.st{background:var(--judgment)}.status-na .badge.st{background:var(--na)}
.badge.pr{background:#444}.answer{white-space:pre-wrap}
table.data{width:100%;border-collapse:collapse;margin-top:.6rem;font-size:.86rem;display:block;overflow-x:auto}
table.data th,table.data td{border:1px solid var(--border);padding:.35rem .55rem;text-align:left;vertical-align:top}table.data th{background:var(--card)}
td.num{text-align:right;white-space:nowrap}.impact{margin-top:.6rem;font-weight:600;color:#5b3fc4;font-size:.9rem}
.note{color:var(--muted);font-size:.86rem;margin-top:.55rem;font-style:italic}.src{color:var(--muted);font-size:.78rem;margin-top:.4rem}
.query{color:var(--missing);font-size:.85rem;margin-top:.4rem}
footer{text-align:center;color:var(--muted);font-size:.8rem;padding:2rem 1rem}
@media print{.pills,input.search,nav.toc{display:none}section.clause{break-inside:avoid}header.page{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""

JS = """
const secs=[...document.querySelectorAll('section.clause')];let mode='all';
function apply(){const q=(document.getElementById('q').value||'').toLowerCase();
 secs.forEach(s=>{const okMode=mode==='all'||(mode==='impact'?s.dataset.impact==='1':s.dataset.status===mode);
 const okQ=!q||s.textContent.toLowerCase().includes(q);s.style.display=okMode&&okQ?'':'none';});}
document.querySelectorAll('button.pill').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;
 document.querySelectorAll('button.pill').forEach(x=>x.setAttribute('aria-pressed',x===b));apply();}));
document.getElementById('q').addEventListener('input',apply);
"""


def esc(v):
    return htmlmod.escape("" if v is None else str(v))


def html_table(headers, rows, num_cols=()):
    thead = "<thead><tr>" + "".join(f"<th>{esc(h)}</th>" for h in headers) + "</tr></thead>" if headers else ""
    body = "".join("<tr>" + "".join(
        f'<td class="num">{esc(v)}</td>' if i in num_cols else f"<td>{esc(v)}</td>" for i, v in enumerate(r)) + "</tr>"
        for r in rows)
    return f'<table class="data">{thead}<tbody>{body}</tbody></table>'


def render_html(data, d, out_path):
    client = data.get("client", {})
    form = data.get("form_type", "3CB")
    c = d["counts"]
    parts = []
    kv = "".join(f"<tr><td>{esc(label(k))}</td><td>{esc(v)}</td></tr>" for k, v in client.items())
    parts.append(f'<div class="card"><h3>Client</h3><table class="kv">{kv}</table></div>')

    imp_pill = f'<button class="pill impact" data-mode="impact" aria-pressed="false">{len({i["clause"] for i in d["impacts"]})} with tax impact</button>' if d["impacts"] else ""
    parts.append(
        '<div class="card"><h3>Review summary</h3><div class="pills">'
        f'<button class="pill all" data-mode="all" aria-pressed="true">All {len(d["clauses"])}</button>'
        f'<button class="pill judgment" data-mode="judgment" aria-pressed="false">{c["judgment"]} judgment calls</button>'
        f'<button class="pill missing" data-mode="missing" aria-pressed="false">{c["missing"]} missing data</button>'
        f'<button class="pill filled" data-mode="filled" aria-pressed="false">{c["filled"]} filled</button>'
        f'<button class="pill na" data-mode="not_applicable" aria-pressed="false">{c["not_applicable"]} N/A</button>'
        f'{imp_pill}</div></div>')
    if d["omitted"]:
        parts.append(f'<div class="warn">&#9888; {len(d["omitted"])} standard Form 3CD clause(s) do not appear in this '
                     f'draft at all (not even as N/A): {esc(", ".join(d["omitted"]))}. Confirm whether these were '
                     f'deliberately skipped or missed.</div>')

    if d["attention"]:
        rows = []
        for cl in d["attention"]:
            amt = sum(to_number(i.get("amount")) or 0 for i in impacts_of(cl))
            rows.append([cl["number"], cl.get("title", ""), STATUS_META[cl["status"]]["short"],
                         (cl.get("priority") or "").title(), fmt_inr(amt) if amt else "—"])
        parts.append('<div class="card"><h3>CA attention list — start here</h3>'
                     + html_table(["Clause", "Title", "Status", "Priority", "Impact (Rs.)"], rows, num_cols=(4,)) + "</div>")
    if d["impacts"]:
        rows = [[i["clause"], i["basis"], i["description"], STATUS_META[i["status"]]["short"],
                 ("+ " if i["direction"] == "add" else "− ") + fmt_inr(i["amount"]) + (" (dup.)" if i["double_count_of"] else "")]
                for i in d["impacts"]]
        rows.append(["", "", "Net effect on total income (excluding duplicates)", "", fmt_inr(d["net_impact"])])
        rows.append(["", "", "of which 'filled' (no judgment pending)", "", fmt_inr(d["confirmed_impact"])])
        parts.append('<div class="card"><h3>Computation impact summary (draft)</h3>'
                     + html_table(["Clause", "Section", "Item", "Status", "Amount (Rs.)"], rows, num_cols=(4,))
                     + '<div class="note">Adjustments identified for the income computation. Not a tax computation; '
                       'judgment items may change after CA review.</div></div>')
    if d["recons"]:
        rows = [[r.get("item", ""), f"{r.get('source_a', '')}: {fmt_inr(r.get('amount_a'))}",
                 f"{r.get('source_b', '')}: {fmt_inr(r.get('amount_b'))}",
                 fmt_inr(r.get("difference")) if r.get("difference") not in (None, "") else "",
                 (r.get("status") or "").title(), r.get("explanation", "")] for r in d["recons"]]
        parts.append('<div class="card"><h3>Cross-document reconciliations</h3>'
                     + html_table(["Check", "Source A", "Source B", "Diff.", "Result", "Explanation"], rows, num_cols=(3,)) + "</div>")

    parts.append('<input id="q" class="search" type="search" placeholder="Search clauses, parties, sections…">')
    toc = "".join(
        f'<a class="{STATUS_META.get(cl.get("status", "filled"), STATUS_META["filled"])["css"]}" href="#clause-{esc(cl["number"])}">'
        f'<span class="dot"></span>{esc(cl["number"])} &mdash; {esc(cl.get("title", ""))}</a>' for cl in d["clauses"])
    parts.append(f'<nav class="toc">{toc}</nav>')

    for cl in d["clauses"]:
        st = cl.get("status", "filled")
        meta = STATUS_META.get(st, STATUS_META["filled"])
        badges = f'<span class="badge st">{esc(meta["label"])}</span>' if meta["label"] else ""
        if cl.get("priority") and st in ("judgment", "missing"):
            badges += f'<span class="badge pr">{esc(cl["priority"].title())} priority</span>'
        body = f'<div class="answer">{esc(cl.get("answer"))}</div>' if cl.get("answer") else ""
        headers, rows = table_rows(cl.get("table"))
        if rows:
            body += html_table(headers, rows)
        for imp in impacts_of(cl):
            sign = "Add back" if imp.get("direction", "add") == "add" else "Deduct"
            body += (f'<div class="impact">Computation impact: {sign} Rs. {esc(fmt_inr(imp.get("amount")))} — '
                     f'{esc(imp.get("basis", ""))}{(" (" + esc(imp.get("description")) + ")") if imp.get("description") else ""}</div>')
        if cl.get("notes"):
            body += f'<div class="note">Note: {esc(cl["notes"])}</div>'
        if cl.get("sources"):
            body += f'<div class="src">Source: {esc("; ".join(str(s) for s in cl["sources"]))}</div>'
        if cl.get("client_query"):
            body += f'<div class="query">Client query: {esc(cl["client_query"])}</div>'
        parts.append(f'<section class="clause {meta["css"]}" id="clause-{esc(cl["number"])}" data-status="{esc(st)}" '
                     f'data-impact="{1 if impacts_of(cl) else 0}"><h2>Clause {esc(cl["number"])} &mdash; '
                     f'{esc(cl.get("title", ""))}</h2>{badges}{body}</section>')

    if d["queries"]:
        rows = [[k + 1, q["number"], q["client_query"]] for k, q in enumerate(d["queries"])]
        parts.append('<div class="card"><h3>Appendix A — Information required from the client</h3>'
                     + html_table(["#", "Clause", "Information / document required"], rows) + "</div>")
    if d["docs"]:
        rows = [[x.get("ref", ""), x.get("file", ""), x.get("description", "")] for x in d["docs"]]
        parts.append('<div class="card"><h3>Appendix B — Source documents relied on</h3>'
                     + html_table(["Ref", "File", "Description"], rows) + "</div>")

    p = d["preparer"]
    page = (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Tax Audit Workpaper - {esc(client.get("name", "Client"))}</title><style>{CSS}</style></head><body>'
        f'<header class="page"><h1>Tax Audit Workpaper &mdash; Form {esc(form)}-3CD</h1>'
        f'<p>{esc(client.get("name", ""))} &middot; AY {esc(client.get("assessment_year", ""))} &middot; '
        f'Draft prepared {d["gen_date"]} &middot; for CA review before filing &middot; not a final report</p></header>'
        f'<div class="wrap">{"".join(parts)}</div>'
        f'<footer>Generated by tax-audit-workpaper skill v{SKILL_VERSION} &middot; verify every flagged item before filing<br>'
        f'Workpaper prepared by {esc(p["name"])} &middot; {esc(p["phone"])} &middot; '
        f'<a href="{esc(p["url"])}" style="color:inherit">{esc(p["url"])}</a></footer>'
        f'<script>{JS}</script></body></html>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)


# ---------------------------------------------------------------------------
# XLSX review register
# ---------------------------------------------------------------------------

def render_xlsx(data, d, out_path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation

    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    hdr_fill = PatternFill("solid", fgColor="1F3A5F")
    hdr_font = Font(bold=True, color="FFFFFF")
    wrap = Alignment(wrap_text=True, vertical="top")
    client = data.get("client", {})

    def sheet(ws, title_text, headers, widths):
        ws["A1"] = title_text
        ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = f"{client.get('name', '')} · PAN {client.get('pan', '')} · AY {client.get('assessment_year', '')} · draft {d['gen_date']}"
        ws["A2"].font = Font(italic=True, color="606060")
        for i, h in enumerate(headers, 1):
            cell = ws.cell(row=4, column=i, value=h)
            cell.fill, cell.font, cell.alignment, cell.border = hdr_fill, hdr_font, wrap, border
            ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
        ws.freeze_panes = "A5"
        return 5

    # 1. Review register
    ws = wb.active
    ws.title = "Review Register"
    hdrs = ["Clause", "Title", "Status", "Priority", "Impact (Rs.)", "Draft answer (summary)", "Notes / basis",
            "Sources", "Preparer comment", "Reviewer comment", "Reviewer sign-off", "Review date"]
    r = sheet(ws, "Tax audit review register — Form " + data.get("form_type", "") + "-3CD", hdrs,
              [8, 34, 11, 9, 13, 55, 55, 34, 26, 30, 12, 12])
    first = r
    for cl in d["clauses"]:
        st = cl.get("status", "filled")
        amt = sum((to_number(i.get("amount")) or 0) * (1 if i.get("direction", "add") == "add" else -1)
                  for i in impacts_of(cl) if not i.get("double_count_of"))
        ans = str(cl.get("answer") or "")
        if not ans and cl.get("table"):
            ans = f"[table — {len(cl['table'])} row(s); see workpaper]"
        vals = [cl.get("number"), cl.get("title", ""), STATUS_META.get(st, STATUS_META["filled"])["short"],
                (cl.get("priority") or "").title(), amt if amt else None, ans[:1500], str(cl.get("notes") or "")[:1500],
                "; ".join(str(s) for s in cl.get("sources") or []), "", "", "", ""]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=i, value=v)
            cell.alignment, cell.border = wrap, border
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor=STATUS_META.get(st, STATUS_META["filled"])["xl"])
        ws.cell(row=r, column=5).number_format = '#,##,##0;[Red]-#,##,##0'
        r += 1
    last = r - 1
    dv = DataValidation(type="list", formula1='"Agreed,Amended,Query raised,Not reviewed"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"K{first}:K{last}")
    ws.auto_filter.ref = f"A4:{get_column_letter(len(hdrs))}{last}"
    r += 1
    ws.cell(row=r, column=1, value="Progress").font = Font(bold=True)
    ws.cell(row=r + 1, column=1, value="Clauses")
    ws.cell(row=r + 1, column=2, value=f"=COUNTA(A{first}:A{last})")
    ws.cell(row=r + 2, column=1, value="Signed off")
    ws.cell(row=r + 2, column=2, value=f'=COUNTIF(K{first}:K{last},"Agreed")+COUNTIF(K{first}:K{last},"Amended")')
    ws.cell(row=r + 3, column=1, value="% reviewed")
    ws.cell(row=r + 3, column=2, value=f"=IF(B{r + 1}=0,0,B{r + 2}/B{r + 1})")
    ws.cell(row=r + 3, column=2).number_format = "0%"

    # 2. Impact summary
    ws2 = wb.create_sheet("Impact Summary")
    r = sheet(ws2, "Computation impact summary (draft — not a tax computation)",
              ["Clause", "Section", "Item", "Status", "Add / Deduct", "Amount (Rs.)", "Signed amount", "Counted?"],
              [8, 16, 60, 11, 12, 15, 15, 30])
    first = r
    for i in d["impacts"]:
        vals = [i["clause"], i["basis"], i["description"], STATUS_META[i["status"]]["short"],
                "Add" if i["direction"] == "add" else "Deduct", i["amount"], None,
                "No — same amount shown in clause " + str(i["double_count_of"]) if i["double_count_of"] else "Yes"]
        for k, v in enumerate(vals, 1):
            cell = ws2.cell(row=r, column=k, value=v)
            cell.alignment, cell.border = wrap, border
        ws2.cell(row=r, column=7, value=f'=IF(H{r}="Yes",IF(E{r}="Add",F{r},-F{r}),0)')
        for col in (6, 7):
            ws2.cell(row=r, column=col).number_format = '#,##,##0;[Red]-#,##,##0'
        r += 1
    last = max(r - 1, first)
    ws2.cell(row=r + 1, column=3, value="Net effect on total income").font = Font(bold=True)
    ws2.cell(row=r + 1, column=7, value=f"=SUM(G{first}:G{last})").font = Font(bold=True)
    ws2.cell(row=r + 2, column=3, value="of which status = Filled")
    ws2.cell(row=r + 2, column=7, value=f'=SUMIFS(G{first}:G{last},D{first}:D{last},"Filled")')
    for rr in (r + 1, r + 2):
        ws2.cell(row=rr, column=7).number_format = '#,##,##0;[Red]-#,##,##0'

    # 3. Reconciliations
    ws3 = wb.create_sheet("Reconciliations")
    r = sheet(ws3, "Cross-document reconciliations",
              ["Check", "Source A", "Amount A", "Source B", "Amount B", "Difference", "Result", "Explanation"],
              [34, 28, 15, 28, 15, 15, 12, 60])
    for rec in d["recons"]:
        a, b = to_number(rec.get("amount_a")), to_number(rec.get("amount_b"))
        vals = [rec.get("item", ""), rec.get("source_a", ""), a, rec.get("source_b", ""), b, None,
                (rec.get("status") or "").title(), rec.get("explanation", "")]
        for k, v in enumerate(vals, 1):
            cell = ws3.cell(row=r, column=k, value=v)
            cell.alignment, cell.border = wrap, border
        if a is not None and b is not None:
            ws3.cell(row=r, column=6, value=f"=C{r}-E{r}")
        else:
            ws3.cell(row=r, column=6, value=to_number(rec.get("difference")))
        for col in (3, 5, 6):
            ws3.cell(row=r, column=col).number_format = '#,##,##0;[Red]-#,##,##0'
        if (rec.get("status") or "") == "unexplained":
            ws3.cell(row=r, column=7).fill = PatternFill("solid", fgColor="F8CBAD")
        r += 1

    # 4. Client queries
    ws4 = wb.create_sheet("Client Queries")
    r = sheet(ws4, "Information required from the client",
              ["#", "Clause", "Information / document required", "Status", "Date requested", "Date received", "Remarks"],
              [5, 9, 80, 12, 14, 14, 30])
    first = r
    for k, q in enumerate(d["queries"], 1):
        vals = [k, q["number"], q["client_query"], "Open", d["gen_date"], "", ""]
        for j, v in enumerate(vals, 1):
            cell = ws4.cell(row=r, column=j, value=v)
            cell.alignment, cell.border = wrap, border
        r += 1
    if d["queries"]:
        dv2 = DataValidation(type="list", formula1='"Open,Received,Closed,Not available"', allow_blank=True)
        ws4.add_data_validation(dv2)
        dv2.add(f"D{first}:D{r - 1}")

    # 5. Documents
    ws5 = wb.create_sheet("Documents")
    r = sheet(ws5, "Source documents relied on", ["Ref", "File", "Description"], [8, 40, 80])
    for x in d["docs"]:
        for j, v in enumerate([x.get("ref", ""), x.get("file", ""), x.get("description", "")], 1):
            cell = ws5.cell(row=r, column=j, value=v)
            cell.alignment, cell.border = wrap, border
        r += 1

    wb.save(out_path)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if len(args) != 2:
        print("Usage: python3 render_output.py <workpaper.json> <output_dir> [--force]", file=sys.stderr)
        sys.exit(1)
    in_path, out_dir = args
    with open(in_path, encoding="utf-8") as f:
        data = json.load(f)

    errors, warnings = validate(data)
    for w in warnings:
        print(f"WARNING {w}")
    if errors:
        for e in errors:
            print(f"ERROR   {e}", file=sys.stderr)
        if not force:
            print("Not rendered: fix the errors above (or pass --force).", file=sys.stderr)
            sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    d = prepare(data)
    slug = slugify(data.get("client", {}).get("name", "client"))
    outs = {
        "docx": os.path.join(out_dir, f"{slug}_tax_audit_workpaper.docx"),
        "html": os.path.join(out_dir, f"{slug}_tax_audit_workpaper.html"),
        "xlsx": os.path.join(out_dir, f"{slug}_review_register.xlsx"),
    }
    render_docx(data, d, outs["docx"])
    render_html(data, d, outs["html"])
    try:
        render_xlsx(data, d, outs["xlsx"])
    except ImportError:
        print("NOTE openpyxl not installed — review register (.xlsx) skipped.")
        outs.pop("xlsx")
    c = d["counts"]
    print(f"Summary: {len(d['clauses'])} clauses | filled {c['filled']} | judgment {c['judgment']} | "
          f"missing {c['missing']} | N/A {c['not_applicable']} | net impact Rs. {fmt_inr(d['net_impact'])}")
    for p in outs.values():
        print(f"Written: {p}")


if __name__ == "__main__":
    main()
