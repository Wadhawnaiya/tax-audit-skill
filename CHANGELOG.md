# Changelog

## v1.0.0 — 20-Nov-2026

### Law and accuracy fixes
- **Clause 22** rewritten for Notification 23/2025: it now has (i) MSMED s.23 interest, (ii) total payable to
  micro/small enterprises, (iii)(a) paid in time / (b) not paid in time and inadmissible. The old guidance said
  43B(h) belonged only in clause 26 — it is now disclosed in both, disallowed once.
- **Due dates** updated for CBDT Circular 7/2026: tax audit report 21-Oct-2026, ITR (audit cases) 21-Nov-2026;
  s.271B late-report exposure and Rule 6G(3) revised reports added.
- **194-I** threshold corrected to Rs. 50,000 per month or part of a month.
- **Clause 31** form letters A–L mapped to schema codes (CP, CR, PTNAPC …).
- **Club subscriptions** no longer treated as automatically disallowable (*United Glass*, SC 2012).
- New `references/form-26-transition.md`: the skill stops for tax year 2026-27+ (Form No. 26, Income-tax Act 2025).
- Demo client: file-extension and 194J-threshold errors corrected; answer key rewritten (Part A corrected, Part B
  with 20 hidden issues, Part C scoring sheet).

### Workflow
- SKILL.md rewritten as a six-step workflow with three overriding rules; mandatory reconciliation and self-review
  steps; hand-off includes impact and due-date position; narrower requests handled.
- New `references/reconciliations.md` (turnover, TDS ledger-vs-return for every section, GST, depreciation,
  loans, implied-rate test, TB integrity).
- New `references/review-checklist.md` (integrity checks, ten most common misses, red flags).

### Scripts
- `extract_text.py`: `--all` folder mode with `INVENTORY.md` and document refs (D1…), row-numbered Excel dumps,
  PDF text fallback with scanned-PDF detection, legacy .xls support, answer-key files skipped.
- New `validate_workpaper.py`: quality gate (statuses, notes, queries, sources, deleted clauses, order, coverage,
  impacts, reconciliations). Also used by the Claude Code hook.
- `render_output.py` v2: CA attention list, computation impact summary (with double-count control),
  reconciliations, source citations, client query appendix, document index, header/footer, acronym-aware labels,
  filterable/searchable/printable HTML, and a new **Excel review register** (sign-off dropdown, progress %,
  impact formulas, client query tracker). Refuses to render on validation errors unless `--force`.
- Schema v2.0 (`engagement`, `reconciliations`, `sources`, `impact`, `priority`, `client_query`, `preparer`);
  v1 files still render.

### Claude Code teaching kit
- `CLAUDE.md`, `tax-audit-reviewer` subagent, validation hook, `clients/` layout with `.gitignore`,
  `TRAINING-GUIDE.md`, and a full reference run in `demo-output/`.
