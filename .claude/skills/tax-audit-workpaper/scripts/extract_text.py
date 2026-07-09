#!/usr/bin/env python3
"""
Dumps the readable content of a client source document to stdout as plain text.

Claude's Read tool already handles PDFs and images natively (including scanned
documents, via vision) - use Read directly for those, don't run this script on them.

This script exists for the formats Read can't parse on its own: Excel workbooks
(.xlsx/.xls) and Word documents (.docx). It prints every sheet/table/paragraph so
the content can be read like any other text output.

Usage:
    python3 extract_text.py <path/to/file.xlsx|.xls|.docx|.csv|.txt>
"""
import sys
import os


def dump_xlsx(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    for ws in wb.worksheets:
        print(f"\n===== SHEET: {ws.title} =====")
        for row in ws.iter_rows(values_only=True):
            if all(v is None for v in row):
                continue
            print(" | ".join("" if v is None else str(v) for v in row))


def dump_docx(path):
    from docx import Document
    doc = Document(path)
    for element in doc.element.body:
        tag = element.tag.split("}")[-1]
        if tag == "p":
            texts = element.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
            text = "".join(t.text or "" for t in texts)
            if text.strip():
                print(text)
        elif tag == "tbl":
            print("--- TABLE ---")
            for tr in element.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr"):
                cells = tr.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
                row_texts = []
                for tc in cells:
                    texts = tc.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t")
                    row_texts.append("".join(t.text or "" for t in texts))
                print(" | ".join(row_texts))
            print("--- END TABLE ---")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_text.py <file>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        dump_xlsx(path)
    elif ext == ".docx":
        dump_docx(path)
    elif ext in (".csv", ".txt"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
    else:
        print(f"Unsupported extension '{ext}'. For .pdf or image files, use the Read tool directly "
              f"instead of this script.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
