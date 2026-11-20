# tax-audit-skill — v1.0

A Claude Code workspace and skill that drafts Indian tax audit workpapers (**Form 3CA/3CB-3CD, Section 44AB,
AY 2026-27**) from a client's raw documents — trial balance, financial statements, AIS/TIS, Form 16, GST returns,
bank statements and registers, in any mix of PDF, Excel and Word.

**Who it's for:** CA firms where article assistants do the first-pass review and the CA reviews and signs. The
skill does the first pass. It does not file anything, generate e-filing JSON, or replace the CA's judgment,
UDIN or digital signature.

## What's in this kit

| Item | What it is |
|---|---|
| `.claude/skills/tax-audit-workpaper/` | The skill (also packaged as `tax-audit-workpaper-skill.zip`) |
| `.claude/agents/tax-audit-reviewer.md` | Independent reviewer subagent |
| `.claude/settings.json` + `.claude/hooks/` | Hook that validates every workpaper Claude writes |
| `CLAUDE.md` | Firm rules Claude follows in this folder |
| `demo-output/` | Reference run on the demo client: workpaper JSON, Word, HTML, Excel review register |
| `TRAINING-GUIDE.md` | Session plan for teaching Claude Code to CAs, with exercises and a prompt cheat sheet |
| `clients/` | Where client folders go (git-ignored) |

## Install

**Requirements:** Claude Code, Python 3.10+, and `pip install python-docx openpyxl`.

**Option A — use the whole workspace (recommended for training):** unzip `tax-audit-skill-complete.zip`, open the
folder in Claude Code, type `/tax-audit-workpaper`.

**Option B — add only the skill to your own setup:** unzip `tax-audit-workpaper-skill.zip` into
`~/.claude/skills/` (all your projects) or `<your project>/.claude/skills/` (one project). You should end up with
`.../skills/tax-audit-workpaper/SKILL.md`.

**Option C — Claude app (chat):** upload `tax-audit-workpaper-skill.zip` as-is in the Skills section of
Settings, with code execution enabled.

## Use it

```
/tax-audit-workpaper clients/<client-folder>
```

or just ask: "Prepare the tax audit workpaper for the documents in clients/sharma-traders."

The skill works in six steps — scope, inventory, reconcile, draft, self-review + validate, render — and produces:

| Output | Use |
|---|---|
| `<client>_tax_audit_workpaper.docx` | CA attention list, computation impact summary, reconciliations, clause-by-clause answers with sources, client request list |
| `<client>_tax_audit_workpaper.html` | Fast on-screen review: filter by judgment / missing / tax impact, search, print |
| `<client>_review_register.xlsx` | Review working paper: reviewer comments, sign-off dropdown, progress %, impact sheet with formulas, client query tracker |

Every clause carries one of four statuses: **Filled**, **Judgment call**, **Missing data**, **N/A**. Missing
figures are never invented.

## Try it on the demo client

`.claude/skills/tax-audit-workpaper/assets/demo-client/` is a synthetic private limited company with 23 planted
issues and 20 more hidden in the data (TDS gaps between ledgers and returns, unfunded gratuity, a 252% implied
interest rate, a GSTR-9 keying error…). Compare your run with `demo-output/` and score it with the answer key's
Part C. The answer key is for the trainer — never feed it to the skill.

## Scope and currency

- Built for **AY 2026-27 / FY 2025-26** under the Income-tax Act, 1961. Law re-checked on 20-Nov-2026, including
  Notification 23/2025 (clauses 28/29 omitted, 36B inserted, clause 22 now covers 43B(h), clause 31 codes) and
  CBDT Circular 7/2026 (report due 21-Oct-2026, ITR 21-Nov-2026 for audit cases).
- From **tax year 2026-27** tax audits move to **Form No. 26** under the Income-tax Act, 2025 (s.63, Rule 47).
  The skill detects this and stops rather than guess; a Form 26 version is the next rebuild.
- Thresholds live in one file, `references/thresholds-ay2026-27.md`, with an update checklist.

See `CHANGELOG.md` for what changed from v0.1.
