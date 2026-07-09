# Workpaper JSON schema (input to `scripts/render_output.py`)

Build one JSON object per client and save it, then run:

```
python3 scripts/render_output.py <workpaper.json> <output_dir>
```

This produces `<slug>_tax_audit_workpaper.docx` and `<slug>_tax_audit_workpaper.html` in `<output_dir>`. The
script only lays the data out — it does not compute, judge, or validate tax positions. All of that must already
be decided before this JSON is built.

## Top-level shape

```json
{
  "form_type": "3CA",
  "client": {
    "name": "...",
    "pan": "...",
    "status": "...",
    "previous_year": "01-Apr-2025 to 31-Mar-2026",
    "assessment_year": "2026-27",
    "...any other flat key/value worth showing on the cover page...": "..."
  },
  "clauses": [
    { "number": "8a", "title": "...", "answer": "...", "table": [...], "status": "filled", "notes": "..." }
  ]
}
```

- `form_type`: `"3CA"` or `"3CB"` — decide this first, per `references/clauses-cover-and-applicability.md`, before building anything else.
- `client`: a flat object of label → value. Keys are title-cased automatically for display (`previous_year` → "Previous Year"). Include whatever cover-page facts clauses 1–7 need.
- `clauses`: an ordered array, one entry per Form 3CD clause that applies to this client. Order matters — it drives both the Word document and the HTML table of contents, so emit them in the standard Form 3CD sequence (1, 2, 3 … 44). **Clause 21 is the one clause split into separate lettered entries** — emit `21(a)` through `21(i)` as distinct array entries, matching `references/clauses-18-to-26.md`. Every other multi-part clause (9, 11, 13, 20, 26, 31, 34, etc.) stays a **single** entry per whole number, with its internal sub-items (e.g. 11(a)/(b)/(c)) folded into that one entry's `answer`/`table`/`notes` — don't split those into separate array entries or the completeness checker will show false-positive omission warnings.

## Clause entry fields

| Field    | Required | Notes |
|----------|----------|-------|
| `number` | yes | Exact clause label as it appears on the form, e.g. `"21(b)"`, `"29A"`, `"8a"`. Must match the labels used in `references/clauses-*.md` so the completeness checker in the renderer recognizes it. |
| `title`  | yes | Short clause heading, e.g. `"Amounts inadmissible under section 40(a)"`. |
| `status` | yes | One of `filled`, `missing`, `judgment`, `not_applicable`. See below. |
| `answer` | no | Free-text drafted answer. Omit or leave empty if the clause is purely tabular. |
| `table`  | no | Either a list of objects with identical keys (keys become column headers, in order), or a list of lists (no header row). Use for anything naturally tabular — clause 18 depreciation, clause 26 43B items, clause 31 loans/deposits, clause 34 TDS compliance, clause 35 quantitative details, etc. |
| `notes`  | no | Short explanation, source citation, or the specific reason something is flagged. Always fill this in when `status` is `missing` or `judgment` — an unexplained flag is not useful to the reviewing CA. |

## Status values — pick correctly, this drives the whole review workflow

- **`filled`** — a confident, fully-sourced answer. No badge shown.
- **`missing`** — a *factual* figure or document is absent from what the client provided. Never invent a number to avoid this status; use it instead. `notes` should say exactly what's missing and from where it would normally come (e.g. "PF payment challans not provided — cannot confirm actual remittance date").
- **`judgment`** — the facts are present, but the correct tax treatment requires interpretation, a borderline call, or something only the CA should sign off on (e.g. reasonableness of related-party pricing, whether a Rule 6DD exception applies, GAAR applicability). Give your best-guess `answer`/`table` AND explain the judgment call in `notes`.
- **`not_applicable`** — actively confirmed as not relevant to this client (e.g. clause 30A when there are no international transactions). Don't use this as a default for "didn't check" — only use it when the source documents or client profile affirmatively support N/A. If genuinely unchecked, use `missing` instead.

## Completeness checking

The renderer carries its own canonical list of standard Form 3CD clause numbers (see `CANONICAL_CLAUSES` in
`scripts/render_output.py` — note clauses 28 and 29 were deleted from the form by CBDT Notification 23/2025 and are
correctly absent from that list, while a new clause 36B — buy-back-of-shares deemed dividend under section
2(22)(f) — was inserted by the same notification and is included). Any canonical clause missing entirely from your `clauses` array — not even
present as `not_applicable` — triggers a visible warning banner in both outputs. Before finalizing the JSON, make
sure every applicable clause for the client's entity type and Form (3CA vs 3CB) is represented, even if only to
mark it `not_applicable`. Silently omitting a clause because it seemed irrelevant looks identical to forgetting it
— always emit an explicit `not_applicable` entry instead of leaving it out.

## Example minimal entry

```json
{
  "number": "21(d)",
  "title": "Disallowance under section 40A(3) — cash payments exceeding prescribed limit",
  "status": "judgment",
  "table": [
    {"Date": "12-Aug-2025", "Payee": "Shree Balaji Packaging", "Amount": "55,000", "Mode": "Cash"}
  ],
  "notes": "Single-day cash payment to one party exceeds Rs.10,000; no Rule 6DD exception identified from available records. CA to confirm disallowance and check for any exception not evident from the bank/cash book alone."
}
```
