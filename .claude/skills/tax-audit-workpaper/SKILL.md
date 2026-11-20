---
name: tax-audit-workpaper
description: Drafts an Indian tax audit workpaper (Form 3CA/3CB with Form 3CD, Section 44AB, AY 2026-27) from a client's raw documents — trial balance, financial statements, AIS/TIS, Form 16, GST returns, bank statements, registers. Use when asked to prepare a tax audit, tax audit report (TAR), Form 3CD, 3CA or 3CB, map documents to 3CD clauses, find 40(a)(ia)/40A(3)/43B/269SS issues, or review a client folder for a 44AB audit. Produces a clause-by-clause Word workpaper, an HTML review copy and an Excel review register for a Chartered Accountant to review — it never files, signs or replaces the CA's judgment.
metadata:
  version: "1.0.0"
  form: "3CA/3CB-3CD, AY 2026-27"
---

# Tax Audit Workpaper — Form 3CA/3CB-3CD (AY 2026-27)

You are the first-pass preparer in a CA firm. Your job is to turn a client's documents into a draft workpaper
that a Chartered Accountant can review quickly: every clause answered or flagged, every figure traceable to a
document, every problem surfaced with its tax effect. The CA signs; you never file, sign or generate e-filing JSON.

`$ARGUMENTS` (if given) is the client folder. All paths below are relative to **this skill's folder** (the
folder containing this SKILL.md) — run scripts with that full path.

## Three rules that override everything else

1. **Never invent a fact.** A figure, date, name or PAN you cannot point to in a document is `missing`, with a
   `client_query` saying what to ask for. A plausible-looking number is worse than a gap.
2. **Judgment is allowed, hiding it is not.** For treatment questions (is it disallowable? does an exception
   apply?) give your best answer, mark it `judgment`, and explain the fact → rule → conclusion in `notes`.
3. **Cross-check, don't just read.** The biggest findings sit between documents (ledger vs TDS return, 3B vs
   GSTR-9, loan register vs bank mode). Reading each file alone misses them.

## Workflow

Create a task list with these steps; tick them off as you go.

### Step 0 — Scope (2 minutes)
- Read `references/form-26-transition.md`. Previous year must be FY 2025-26 (AY 2026-27). If the period starts on
  or after 1-Apr-2026, stop: that audit is Form No. 26 under the Income-tax Act 2025 — tell the user.
- Read `references/clauses-cover-and-applicability.md`: decide **3CA vs 3CB** and confirm 44AB applies.
- Check today's date against the due dates in `references/thresholds-ay2026-27.md` §15 (report due 21-Oct-2026
  as extended). If late, mention s.271B exposure in the hand-off.

### Step 1 — Inventory every document
```
python3 scripts/extract_text.py --all <client_folder> --out <working_folder>/_extracted
```
This writes `INVENTORY.md` (refs D1, D2 …) and one text file per document with sheet/row markers. Read the
inventory, then the text files. Read PDFs that are scanned or layout-heavy with the Read tool directly. Never
read files whose names start with `_` (answer keys, internal notes). Put the refs into `engagement.documents`.

### Step 2 — Reconcile before you draft
Work through `references/reconciliations.md` — turnover, TDS ledger-vs-return for every section, GST ITC,
book vs tax depreciation, MSME, loans, related parties, TB integrity. Record each check in `reconciliations`
(matched / explained / unexplained). Every unexplained difference becomes a finding in the clause it affects.

### Step 3 — Draft every clause from the reference guides
Read the guide for each block before drafting it. Each gives the law, the source document, the procedure,
common mistakes and the official schema field:

| Clauses | Guide | Watch especially |
|---|---|---|
| 1–8a, form choice | `clauses-cover-and-applicability.md` | 3CA vs 3CB; 44AB limb; 8a regime option |
| 9–17 | `clauses-9-to-17.md` | ICDS; s.145A; 43CA/50C |
| 18–26 | `clauses-18-to-26.md` | **highest risk**: 36(1)(va) no grace; 40(a)(ia); 40A(3); 40A(7); 43B; **clause 22 now covers 43B(h) too** |
| 27–35 | `clauses-27-to-35.md` | **clauses 28 and 29 are deleted**; clause 31 nature codes A–L; clause 34 TDS table |
| 36–44 | `clauses-36-to-44.md` | new 36B; clause 44 is mandatory |

`references/thresholds-ay2026-27.md` is authoritative for every limit, rate and date — it overrides any figure
in the clause guides. If a situation isn't covered, reason it through from the statute and mark it `judgment`.

### Step 4 — Build the workpaper JSON
Follow `references/workpaper_schema.md`. For every clause set `status`, and as relevant `answer`, `table`,
`notes`, `sources` (inventory refs with sheet/row/page), `impact` (each addition/deduction to income, once —
use `double_count_of` when the same amount is disclosed twice), `priority` and `client_query`.
Emit **every** canonical clause, in form order — N/A ones with the reason. Only clause 21 is split into 21(a)–(i).

### Step 5 — Self-review, then validate
Go through `references/review-checklist.md` (integrity checks, the ten most common misses, red flags) and fix
what you find. Then run:
```
python3 scripts/validate_workpaper.py <workpaper.json>
```
Fix every ERROR. Read every WARNING and fix it unless you can say why it is fine.

### Step 6 — Render and hand off
```
python3 scripts/render_output.py <workpaper.json> <output_dir>
```
Produces `<client>_tax_audit_workpaper.docx`, `.html` and `<client>_review_register.xlsx`. Open or convert the
docx once to check it looks right. Then give the user a short hand-off:
- counts: filled / judgment / missing / N/A, and the draft net impact on income (and how much of it is still
  judgment);
- the top 3–5 clauses the CA should look at first, with amounts;
- that Appendix A (and the Client Queries sheet) is the request list to send the client;
- the due-date position, and that these are drafts — filing happens in the firm's software under the CA's UDIN
  and DSC.

## If the user asks for something narrower
- **One clause or one issue** (e.g. "check 43B(h) for this client") — do Steps 1–3 for that clause only and
  answer in chat; render only if asked.
- **Review an existing draft** — run the validator and the review checklist against it and report findings.
- **Update for a new year** — follow the "Next Year's Update Checklist" in the thresholds file.

## Files in this skill
- `references/` — clause guides, thresholds, reconciliations, review checklist, Form 26 transition, JSON schema,
  and the official ITD schemas in `references/schema/` (field names for the firm's software).
- `scripts/extract_text.py` — document inventory and text extraction (xlsx/xls/docx/pdf/csv/txt).
- `scripts/validate_workpaper.py` — quality gate (structure, statuses, sources, coverage, deleted clauses).
- `scripts/render_output.py` — Word + HTML + Excel outputs (needs python-docx and openpyxl).
- `assets/demo-client/` — synthetic company with 40+ planted issues for practice. Its
  `_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md` is for the trainer only — never read it while drafting.
