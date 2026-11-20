#!/usr/bin/env python3
"""
Turn client source documents into plain text Claude can read and cite.

Single file (prints to stdout):
    python3 extract_text.py <file.xlsx|.xls|.xlsm|.docx|.csv|.txt|.pdf>

Whole client folder (recommended first step of every engagement):
    python3 extract_text.py --all <client_folder> [--out <dir>]

--all writes one .txt per document into <dir> (default: <client_folder>/_extracted)
and an INVENTORY.md listing every file with a document ref (D1, D2, ...), type,
size, sheets/pages and a first-line preview. Use those refs in the workpaper's
`sources` so every figure is traceable.

Notes
- PDFs: Claude's Read tool reads PDFs (including scanned ones) directly and is
  preferred for layout-heavy or scanned pages. This script's PDF text (via
  pdftotext or pypdf, if available) is a searchable backup; if a PDF yields no
  text it is probably scanned — read it with the Read tool instead.
- Excel: every sheet is dumped with row numbers ("R12:") so answers can cite
  "trial_balance.xlsx, sheet X, row 12". Formulas are shown as cached values.
- Files whose names start with "_" (e.g. answer keys) are skipped in --all mode.
"""
import os
import shutil
import subprocess
import sys

SUPPORTED = (".xlsx", ".xlsm", ".xls", ".docx", ".csv", ".txt", ".pdf")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def dump_xlsx(path):
    from openpyxl import load_workbook
    out = []
    wb = load_workbook(path, data_only=True, read_only=True)
    for ws in wb.worksheets:
        out.append(f"\n===== SHEET: {ws.title} =====")
        for idx, row in enumerate(ws.iter_rows(values_only=True), 1):
            if all(v is None for v in row):
                continue
            out.append(f"R{idx}: " + " | ".join("" if v is None else str(v) for v in row))
    return "\n".join(out), f"{len(wb.worksheets)} sheet(s): " + ", ".join(ws.title for ws in wb.worksheets)


def dump_xls(path):
    try:
        import xlrd
    except ImportError:
        return None, "legacy .xls needs xlrd (not installed) — ask the client for .xlsx, or convert with LibreOffice"
    out = []
    book = xlrd.open_workbook(path)
    for sh in book.sheets():
        out.append(f"\n===== SHEET: {sh.name} =====")
        for r in range(sh.nrows):
            vals = sh.row_values(r)
            if any(str(v).strip() for v in vals):
                out.append(f"R{r + 1}: " + " | ".join(str(v) for v in vals))
    return "\n".join(out), f"{book.nsheets} sheet(s)"


def dump_docx(path):
    from docx import Document
    doc = Document(path)
    out, ntab = [], 0
    for el in doc.element.body:
        tag = el.tag.split("}")[-1]
        if tag == "p":
            text = "".join(t.text or "" for t in el.findall(f".//{W}t"))
            if text.strip():
                out.append(text)
        elif tag == "tbl":
            ntab += 1
            out.append(f"--- TABLE {ntab} ---")
            for tr in el.findall(f"{W}tr"):
                out.append(" | ".join("".join(t.text or "" for t in tc.findall(f".//{W}t")) for tc in tr.findall(f"{W}tc")))
            out.append(f"--- END TABLE {ntab} ---")
    return "\n".join(out), f"{ntab} table(s)"


def dump_pdf(path):
    if shutil.which("pdftotext"):
        res = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        text = res.stdout
    else:
        try:
            from pypdf import PdfReader
        except ImportError:
            return None, "no PDF text tool available — read this PDF with the Read tool"
        text = "\n\f".join((p.extract_text() or "") for p in PdfReader(path).pages)
    pages = text.count("\f") + 1 if text else 0
    if len(text.strip()) < 40:
        return text, f"{pages} page(s) — little/no text layer: probably SCANNED, read with the Read tool"
    return text, f"{pages} page(s)"


def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        return dump_xlsx(path)
    if ext == ".xls":
        return dump_xls(path)
    if ext == ".docx":
        return dump_docx(path)
    if ext == ".pdf":
        return dump_pdf(path)
    if ext in (".csv", ".txt"):
        with open(path, encoding="utf-8", errors="replace") as f:
            t = f.read()
        return t, f"{t.count(chr(10)) + 1} line(s)"
    return None, f"unsupported type '{ext}' — read with the Read tool if it is an image, or ask for another format"


def run_all(folder, out_dir):
    out_dir = out_dir or os.path.join(folder, "_extracted")
    os.makedirs(out_dir, exist_ok=True)
    files = sorted(
        os.path.join(root, f)
        for root, dirs, fs in os.walk(folder)
        if not os.path.abspath(root).startswith(os.path.abspath(out_dir))
        for f in fs if not f.startswith((".", "_", "~$"))
    )
    rows = []
    for n, path in enumerate(files, 1):
        ref = f"D{n}"
        rel = os.path.relpath(path, folder)
        try:
            text, info = extract(path)
        except Exception as e:  # keep going: one bad file must not stop the inventory
            text, info = None, f"could not read: {e}"
        preview = ""
        if text:
            txt_name = f"{ref}_{os.path.splitext(os.path.basename(path))[0]}.txt"
            with open(os.path.join(out_dir, txt_name), "w", encoding="utf-8") as f:
                f.write(f"[{ref}] {rel}\n{info}\n{'=' * 60}\n{text}")
            preview = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")[:90]
        else:
            txt_name = "—"
        rows.append((ref, rel, os.path.splitext(path)[1].lower(), os.path.getsize(path), info, txt_name, preview))

    lines = ["# Document inventory", "", f"Folder: `{folder}`", "",
             "| Ref | File | Type | Size (KB) | Contents | Extracted text | First line |",
             "|---|---|---|---|---|---|---|"]
    for ref, rel, ext, size, info, txt, prev in rows:
        lines.append(f"| {ref} | {rel} | {ext} | {size / 1024:.0f} | {info} | {txt} | {prev.replace('|', '/')} |")
    lines += ["", "Use these refs (D1, D2, ...) in the workpaper's `engagement.documents` and in every clause's `sources`."]
    inv = os.path.join(out_dir, "INVENTORY.md")
    with open(inv, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nWritten: {inv} and {sum(1 for r in rows if r[5] != '—')} text file(s) in {out_dir}")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--all":
        if len(args) < 2:
            print(__doc__, file=sys.stderr)
            sys.exit(1)
        out = args[args.index("--out") + 1] if "--out" in args else None
        run_all(args[1], out)
        return
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    text, info = extract(args[0])
    if text is None:
        print(info, file=sys.stderr)
        sys.exit(1)
    print(f"[{info}]")
    print(text)


if __name__ == "__main__":
    main()
