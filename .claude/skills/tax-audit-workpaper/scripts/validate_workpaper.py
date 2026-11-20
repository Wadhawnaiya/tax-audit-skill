#!/usr/bin/env python3
"""
Quality gate for a tax-audit workpaper JSON. Run it BEFORE render_output.py.

    python3 validate_workpaper.py <workpaper.json> [--strict]

Prints ERRORS (must fix) and WARNINGS (review). Exit code:
    0 = no errors (warnings allowed, unless --strict)
    1 = errors found (or warnings found with --strict)
    2 = file unreadable / not JSON

It checks structure and review hygiene only. It does NOT judge tax positions —
that is the preparer's and the CA's job.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wp_common import (  # noqa: E402
    CANONICAL_CLAUSES, DELETED_CLAUSES, PAN_RE, PRIORITIES, STATUSES,
    clause_sort_key, impacts_of, to_number,
)


def validate(data):
    errors, warnings = [], []
    E, W = errors.append, warnings.append

    if not isinstance(data, dict):
        return ["Top level must be a JSON object."], []

    form = data.get("form_type")
    if form not in ("3CA", "3CB"):
        E(f"form_type must be '3CA' or '3CB' (got {form!r}).")

    client = data.get("client") or {}
    if not isinstance(client, dict) or not client:
        E("client block is missing or empty.")
    else:
        for k in ("name", "pan", "assessment_year", "previous_year"):
            if not client.get(k):
                W(f"client.{k} is empty.")
        pan = str(client.get("pan", "")).strip().upper()
        if pan and not PAN_RE.match(pan):
            W(f"client.pan '{pan}' does not look like a valid PAN (AAAAA9999A).")
        ay = str(client.get("assessment_year", ""))
        if ay and ay not in ("2026-27", "AY 2026-27"):
            W(f"assessment_year is '{ay}'. This skill version is built for AY 2026-27 — "
              "for Tax Year 2026-27 onward the audit is in Form No. 26 (see references/form-26-transition.md).")

    docs = (data.get("engagement") or {}).get("documents") or []
    doc_refs = {str(d.get("ref")) for d in docs if isinstance(d, dict) and d.get("ref")}
    if not docs:
        W("engagement.documents is empty — list every source document with a ref (D1, D2...) so answers can cite them.")

    clauses = data.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        E("clauses must be a non-empty list.")
        return errors, warnings

    seen, last_idx = set(), -1
    for i, c in enumerate(clauses):
        tag = f"clauses[{i}]"
        if not isinstance(c, dict):
            E(f"{tag} is not an object.")
            continue
        num = str(c.get("number", "")).strip()
        tag = f"Clause {num or '?'}"
        if not num:
            E(f"clauses[{i}] has no number.")
            continue
        if num in seen:
            E(f"{tag} appears more than once.")
        seen.add(num)
        if num in DELETED_CLAUSES:
            E(f"{tag} was omitted from Form 3CD by Notification 23/2025 — remove it.")
        elif num not in CANONICAL_CLAUSES:
            W(f"{tag} is not a canonical clause label (expected e.g. '21(b)', '8a', '36B'). "
              "Sub-items of other clauses belong inside one entry.")
        idx = clause_sort_key(num)
        if idx < last_idx:
            W(f"{tag} is out of Form 3CD order.")
        last_idx = max(last_idx, idx)

        if not c.get("title"):
            E(f"{tag} has no title.")
        st = c.get("status")
        if st not in STATUSES:
            E(f"{tag} status {st!r} is not one of {', '.join(STATUSES)}.")
        notes = str(c.get("notes") or "").strip()
        if st in ("missing", "judgment") and not notes:
            E(f"{tag} is '{st}' but has no notes explaining why — an unexplained flag is useless to the CA.")
        if st == "missing" and not c.get("client_query"):
            W(f"{tag} is 'missing' but has no client_query (the request to send the client).")
        if st == "not_applicable" and not (notes or c.get("answer")):
            W(f"{tag} is N/A with no reason — say what supports N/A (e.g. 'client is a company').")
        if st == "filled" and not c.get("answer") and not c.get("table"):
            E(f"{tag} is 'filled' but has neither answer nor table.")
        if st in ("filled", "judgment") and not c.get("sources"):
            W(f"{tag} has no sources — every figure should be traceable to a document.")
        for s in c.get("sources") or []:
            m = re.match(r"\s*(D\d+)\b", str(s))
            ref = m.group(1) if m else None
            if doc_refs and ref and ref not in doc_refs:
                W(f"{tag} cites '{ref}', which is not in engagement.documents.")
        pr = c.get("priority")
        if pr is not None and pr not in PRIORITIES:
            W(f"{tag} priority {pr!r} should be one of {', '.join(PRIORITIES)}.")

        tbl = c.get("table")
        if tbl is not None:
            if not isinstance(tbl, list) or not tbl:
                W(f"{tag} table is empty or not a list.")
            elif isinstance(tbl[0], dict):
                keys = list(tbl[0].keys())
                for r, row in enumerate(tbl):
                    if not isinstance(row, dict) or list(row.keys()) != keys:
                        W(f"{tag} table row {r} has different columns from row 0.")
                        break

        for j, imp in enumerate(impacts_of(c)):
            amt = to_number(imp.get("amount"))
            if amt is None:
                E(f"{tag} impact[{j}] amount {imp.get('amount')!r} is not a number.")
            if imp.get("direction", "add") not in ("add", "deduct"):
                W(f"{tag} impact[{j}] direction should be 'add' or 'deduct'.")
            if not imp.get("basis"):
                W(f"{tag} impact[{j}] has no basis (section).")
        if st == "not_applicable" and impacts_of(c):
            W(f"{tag} is N/A but carries a computation impact.")

    omitted = [n for n in CANONICAL_CLAUSES if n not in seen]
    if omitted:
        W(f"{len(omitted)} canonical clause(s) absent (emit them as not_applicable if they don't apply): "
          + ", ".join(omitted))

    for k, r in enumerate(data.get("reconciliations") or []):
        st = r.get("status")
        if st not in ("matched", "explained", "unexplained"):
            W(f"reconciliations[{k}] ({r.get('item')}) status should be matched/explained/unexplained.")
        if st != "matched" and not r.get("explanation"):
            W(f"reconciliations[{k}] ({r.get('item')}) has a difference but no explanation.")
    if not data.get("reconciliations"):
        W("No reconciliations recorded — turnover, TDS, GST and AIS cross-checks are expected (see references/reconciliations.md).")

    return errors, warnings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    try:
        with open(args[0], encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read {args[0]}: {e}", file=sys.stderr)
        sys.exit(2)

    errors, warnings = validate(data)
    n = len(data.get("clauses") or [])
    print(f"Validated {args[0]}: {n} clauses, {len(errors)} error(s), {len(warnings)} warning(s).")
    for e in errors:
        print(f"  ERROR   {e}")
    for w in warnings:
        print(f"  WARNING {w}")
    if errors or (strict and warnings):
        sys.exit(1)
    print("OK — ready to render." if not warnings else "OK with warnings — review them, then render.")


if __name__ == "__main__":
    main()
