---
name: tax-audit-workpaper
description: This skill should be used when the user asks to "prepare a tax audit workpaper", "draft Form 3CD", "draft Form 3CA" or "Form 3CB", "generate the tax audit report data", "map these documents to tax audit clauses", or hands over a client's trial balance, financial statements, AIS/TIS, Form 16, GST returns, or similar source documents for an Income-tax Act 1961 Section 44AB tax audit. Produces a clause-by-clause draft workpaper (Word + HTML) for a Chartered Accountant's review — it does not file, sign, or replace the CA's professional judgment.
version: 0.1.0
---

# Tax Audit Workpaper (Form 3CA/3CB-3CD)

## What this skill does and does not do

This skill turns a client's raw accounting/tax documents into a clause-by-clause draft workpaper covering every
applicable clause of Form 3CD (plus the 3CA or 3CB cover), for **Assessment Year 2026-27 (FY 2025-26)** under the
**Income-tax Act, 1961**, Section 44AB. It is meant to be run by CA-firm staff who don't necessarily know the
Income Tax Act in depth, so the reviewing CA spends time on judgment calls instead of first-pass data entry.

It does **not** file anything, generate the e-filing JSON, or replace the CA's sign-off. Every output document
opens with "for CA review before filing" and status-flags every clause so the reviewer knows where to look first.
The workflow ends with a Word document and an HTML file that get manually reviewed, corrected, and then re-keyed
into the firm's actual tax audit software — this skill's output is a workpaper, not a filing.

**Never fabricate a factual figure that isn't in the source documents.** If a number, date, or fact simply isn't
there, mark that clause `missing` and say what's needed — don't guess a plausible-looking figure. Interpretation
and classification judgment calls (is this expense disallowable? does an exception apply?) are different — make a
best-guess call on those and flag them `judgment`, per the workflow below.

## Step 1 — Determine the form and gather documents

Read `references/clauses-cover-and-applicability.md` first. It covers:
- The Form 3CA vs Form 3CB decision (accounts audited under another law, e.g. Companies Act → 3CA; not otherwise
  audited, e.g. proprietorship/partnership → 3CB).
- Whether Section 44AB audit applies at all (turnover/receipts thresholds, presumptive-scheme opt-out triggers).
- How to fill Part A, clauses 1 through 8a (name, PAN, status, previous year, assessment year, which limb of 44AB
  applies, special tax regime election).

Typical source documents, in whatever mix of formats the client provides: trial balance, audited financial
statements with notes/schedules, fixed asset register, AIS/TIS export from the income tax portal, Form 16 (for
salary TDS cross-checks), GST returns (GSTR-3B/9), bank statements, loan/deposit registers, related-party
transaction listings, TDS return summaries, prior-year tax audit report (for comparatives and carried-forward
figures), and a basic client profile/KYC note if the firm keeps one.

**Reading each document:**
- `.pdf` files (including AIS/TIS/Form 16 downloads and scanned documents) — use the Read tool directly, it
  handles PDFs and images natively.
- `.xlsx`/`.xls` and `.docx` files — Read can't parse these; run `python3 scripts/extract_text.py <file>` and
  read its output instead.
- `.csv`/`.txt` — Read directly, or `extract_text.py` works too.

## Step 2 — Map documents to clauses using the reference guides

Four reference files cover all 44 (well — the current form has some clauses added/deleted, see below) clauses in
statutory order. Read the ones covering the clauses you're working on; each explains the statutory basis, which
source document normally answers it, a step-by-step extraction procedure, common mistakes, and the exact
official-schema field name it maps to (useful for staff who also need to key data into ITD-schema-based software):

- `references/clauses-cover-and-applicability.md` — clauses 1–8a and form applicability
- `references/clauses-9-to-17.md` — books of account, presumptive income, method of accounting/ICDS, stock
  valuation, capital asset conversion, 43CA/50C property transfers
- `references/clauses-18-to-26.md` — depreciation, deductions, disallowances under sections 40/40A/43B. **This is
  the most judgment-heavy, highest error-risk block** — read it carefully, especially the section 43B(h) MSME rule
  (no return-due-date grace period, unlike other 43B items) and the section 36(1)(va) employee-PF-contribution
  rule (permanently disallowed if deposited even one day late — no exceptions).
- `references/clauses-27-to-35.md` — GST/CENVAT, deemed income, related party, transfer pricing/GAAR, loans and
  deposits under 269SS/269T/269ST, brought-forward losses, Chapter VI-A deductions, TDS/TCS compliance,
  quantitative details. **Note:** clauses 28 and 29 were deleted from the form by CBDT Notification 23/2025 —
  don't fill them, don't look for them.
- `references/clauses-36-to-44.md` — deemed dividend (including new clause 36B for buy-back transactions),
  obsolete cost/excise/service-tax audit clauses, accounting ratios, demand/refund, Form 61/61A/61B, CbCR, and
  clause 44 GST-expenditure breakup (confirmed **mandatory**, not deferred, for this AY — don't skip it assuming
  otherwise).

For every numeric threshold, rate, or due date (turnover limits, cash payment limits, TDS rates, 269SS/269T/269ST
amounts, due dates), treat `references/thresholds-ay2026-27.md` as authoritative over anything stated inline in
the clause-guide files — it's the single file the CA will manually refresh each Finance Act cycle.

If a reference file doesn't fully resolve how to treat something (an unusual transaction type, an unclear
interaction between two provisions), reason it through directly — the reference files distill the most common
scenarios but a real client's facts won't always match one exactly.

## Step 3 — Build the workpaper JSON

Assemble one JSON object per `references/workpaper_schema.md`, with a `client` block (Part A cover facts) and a
`clauses` array covering every applicable clause in form order. For each clause, set:
- `status: "filled"` for a confident, sourced answer,
- `status: "missing"` when a factual figure genuinely isn't in the documents (never invent one — say what's
  missing and where it should come from),
- `status: "judgment"` when the facts are present but the tax treatment needs interpretation or CA sign-off (give
  your best-guess answer, explain the call in `notes`),
- `status: "not_applicable"` only when the documents affirmatively support N/A — not as a default for "didn't
  check."

Emit an explicit entry (even if `not_applicable`) for every canonical clause that could apply to this client's
entity type and form — the renderer flags any standard clause that's silently absent, since that looks identical
to an overlooked one. Use tables (`table` field) for anything naturally tabular: depreciation schedule, 43B items,
loans/deposits, TDS compliance, quantitative details, related-party transactions.

Clause 21 is the one clause reported as separate lettered entries (`21(a)` through `21(i)`) — every other
multi-part clause (9, 11, 13, 20, 26, 31, 34, etc.) stays one entry per whole number with its sub-items folded
into that entry's `answer`/`table`/`notes`. See `references/workpaper_schema.md` for the full convention.

Save the JSON to a working file (e.g. in the client's working folder), then run:

```
python3 scripts/render_output.py <workpaper.json> <output_dir>
```

This produces `<client>_tax_audit_workpaper.docx` and `<client>_tax_audit_workpaper.html` — both laid out
clause-by-clause with color-coded status badges (red = missing, amber = judgment call, grey = N/A) and a review
summary dashboard. Both files automatically end with a preparer credit line (name/phone/URL, set as constants at
the top of `render_output.py`) — nothing to add for this in the workpaper JSON. The script is deterministic; it
does no tax reasoning of its own, so get Step 2/3 right before running it.

## Step 4 — Hand off

Present both output files to the user with a short summary: how many clauses were filled outright vs. flagged for
missing data vs. flagged for CA judgment, and which specific clauses need the CA's attention first. Remind them
these are drafts for CA review — the actual filing still happens through their tax audit software using their own
UDIN and digital signature.

## Testing this skill

`assets/demo-client/` contains a complete synthetic client (a fictional private limited company, mixed PDF/Excel
source documents) with about 20 deliberately embedded issues spanning most of the judgment-heavy clauses — cash
payment disallowances, an MSME payment overdue, a missed TDS deduction, a section 269SS cash-loan violation, a
late employee PF deposit, related-party payments, and several clauses that should correctly resolve to N/A. Run
the full workflow against it to sanity-check behavior; `assets/demo-client/_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md`
lists what a correct run should catch (that file is for the developer/CA checking the output, never feed it to
the skill as a source document).

## Additional resources

- `references/schema/` — the official ITD e-filing JSON schemas (`schema_3CA.json`, `schema_3CB.json`) and
  flattened field-structure dumps (`3CA_structure.txt`, `3CB_structure.txt`), useful if staff need to cross-check
  an exact field name in the firm's own tax audit software.
- `references/workpaper_schema.md` — full spec of the JSON `render_output.py` expects.
- `scripts/extract_text.py` — dumps Excel/Word content to text for reading.
- `scripts/render_output.py` — renders the final docx + HTML from the workpaper JSON.

## Keeping this skill current

This skill hard-codes AY 2026-27 figures and form structure. Before next year's filing season, refresh
`references/thresholds-ay2026-27.md` against that year's Finance Act, and check whether CBDT has amended Form
3CD's clause structure again (it has changed twice in the last two years — see the clause 28/29/36B notes above).
From FY 2026-27 onward, tax audits move to the new Income-tax Act 2025 framework (Form No. 26, replacing
3CA/3CB/3CD) — this skill will need a structural rebuild, not just a figures refresh, once that year arrives.
