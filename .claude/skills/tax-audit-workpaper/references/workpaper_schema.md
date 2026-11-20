# Workpaper JSON schema v2.0 (input to the scripts)

```
python3 scripts/validate_workpaper.py <workpaper.json>          # quality gate — fix every ERROR
python3 scripts/render_output.py <workpaper.json> <output_dir>  # docx + html + xlsx review register
```

The scripts only check and lay out data. They never compute or judge tax positions. Version 1 files (no
`engagement`, `reconciliations`, `sources`, `impact`) still render; the validator will warn about what's missing.

## Top level

```json
{
  "schema_version": "2.0",
  "form_type": "3CA",
  "client": { "name": "...", "pan": "...", "status": "...", "previous_year": "01-Apr-2025 to 31-Mar-2026",
              "assessment_year": "2026-27", "...any other cover facts...": "..." },
  "engagement": {
    "prepared_by": "...", "reviewer": "", "audit_report_due_date": "...",
    "documents": [ {"ref": "D1", "file": "trial_balance.xlsx", "description": "Trial balance FY 2025-26"} ]
  },
  "preparer": { "name": "...", "phone": "...", "url": "..." },
  "reconciliations": [ { "item": "...", "source_a": "...", "amount_a": 0, "source_b": "...", "amount_b": 0,
                         "difference": 0, "status": "matched|explained|unexplained", "explanation": "..." } ],
  "clauses": [ { ...clause entry... } ]
}
```

- `form_type` — `"3CA"` or `"3CB"`; decide first (`clauses-cover-and-applicability.md`).
- `client` — flat label → value. Keys display with acronyms kept (`pan` → PAN, `gstin` → GSTIN).
- `engagement.documents` — use the refs from `extract_text.py --all` (INVENTORY.md). Sources cite these refs.
- `preparer` — optional; overrides the default credit line printed on every output.
- `reconciliations` — see `reconciliations.md`. Shown as a table in all three outputs.

## Clause entry

| Field | Required | Notes |
|---|---|---|
| `number` | yes | Exact label: `"8a"`, `"21(b)"`, `"29A"`, `"36B"`. Only clause 21 is split by letter; every other multi-part clause (9, 11, 13, 20, 22, 26, 31, 34 …) is ONE entry with sub-items inside it. Never 28 or 29. |
| `title` | yes | Short heading. |
| `status` | yes | `filled` / `judgment` / `missing` / `not_applicable` (below). |
| `answer` | — | Text as it will be typed into the utility. Use `\n` for sub-items like (a), (b). |
| `table` | — | List of objects with identical keys (keys = headers) or list of lists. |
| `notes` | if judgment/missing | The fact, the rule, the conclusion, what would change it. |
| `sources` | strongly expected | List like `"D9 R43"`, `"D4: contingent liabilities note"`. |
| `impact` | — | One object or a list: `{"amount": 55000, "direction": "add"|"deduct", "basis": "s.40A(3)", "description": "...", "double_count_of": "26"}`. Add `double_count_of` when the same amount is already counted in another clause. |
| `priority` | for judgment/missing | `high` / `medium` / `low` — orders the CA attention list. |
| `client_query` | for missing | Exactly what to ask the client for. Collected into Appendix A and the Client Queries sheet. |

## Status values — this drives the whole review

- **`filled`** — confident, fully sourced. No badge.
- **`judgment`** — facts known, treatment needs the CA (best-guess answer + reasoning in notes).
- **`missing`** — a factual figure or document is absent. Never invent a number to avoid this status.
- **`not_applicable`** — affirmatively supported by the documents (say by what). Not a default for "didn't check".

A clause can be `missing` and still carry a confirmed `impact` (e.g. one late PF month known, the other eleven
not yet checked).

## What the renderer produces

| File | Contents |
|---|---|
| `<slug>_tax_audit_workpaper.docx` | Client & engagement, review summary, CA attention list, computation impact summary, reconciliations, clause-by-clause (with sources, impact, client query), Appendix A client queries, Appendix B documents. |
| `<slug>_tax_audit_workpaper.html` | Same content; filter buttons (judgment / missing / impact), search box, print layout, dark mode. |
| `<slug>_review_register.xlsx` | Review Register (reviewer comment + sign-off dropdown + progress %), Impact Summary (live formulas), Reconciliations, Client Queries tracker, Documents. |

## Example entry

```json
{
  "number": "21(d)",
  "title": "Disallowance u/s 40A(3)/40A(3A) — cash payments",
  "status": "filled",
  "table": [{"Date": "12-Aug-2025", "Payee": "Shree Balaji Packaging", "Amount": "55,000", "Mode": "Cash"}],
  "impact": {"amount": 55000, "direction": "add", "basis": "s.40A(3)", "description": "Cash payment"},
  "notes": "Single payment to one party in a day above Rs. 10,000; no Rule 6DD exception in the records.",
  "sources": ["D2 R7", "D9 R65"],
  "client_query": "Full cash book for FY 2025-26."
}
```
