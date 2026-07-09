# tax-audit-skill

A [Claude Code](https://claude.com/claude-code) skill that drafts Indian Income-tax Act, 1961 tax audit workpapers
(Form 3CA/3CB-3CD, Section 44AB) from a client's raw source documents — trial balance, financial statements,
AIS/TIS, Form 16, GST returns, bank statements, and similar records, in whatever mix of PDF/Excel/Word formats
they arrive in.

**Who this is for:** Chartered Accountant firms where junior staff — who may not have deep Income Tax Act
knowledge — do the first-pass document review, and the CA reviews and signs off before filing. This skill
automates that first pass: it doesn't file anything, generate e-filing JSON, or replace the CA's professional
judgment and UDIN-backed signature. Every output document is explicitly labeled "for CA review before filing."

## Installation

This is a standard [Agent Skill](https://www.anthropic.com/news/skills) — the same `SKILL.md` format works in
both Claude Desktop / claude.ai and Claude Code. Pick whichever you use.

### Option A — Claude Desktop or claude.ai (upload the zip)

1. Download **[`tax-audit-workpaper-skill.zip`](tax-audit-workpaper-skill.zip)** from this repo (or grab it from
   the [Releases](../../releases) page if one has been published).
2. In the Claude app, go to **Settings → Capabilities → Skills** (wording may vary slightly by app version —
   look for a "Skills" section under Settings, sometimes called "Capabilities").
3. Click **Upload skill** (or the **+** button in that section) and select `tax-audit-workpaper-skill.zip` as-is —
   do not unzip it first, and do not re-zip its contents (the zip must contain a single top-level
   `tax-audit-workpaper/` folder with `SKILL.md` inside it, which is exactly how the download is structured).
4. Make sure **Code execution** is enabled for your account/conversation — this skill runs a bundled Python
   script (`scripts/render_output.py`) to produce the final Word/HTML files, so Claude needs the ability to
   execute it. If you don't see a code-execution toggle, check Anthropic's current Skills documentation, since
   this capability and its exact setting name have been evolving.
5. Start a new chat, attach or paste in the client's source documents, and ask Claude to prepare the tax audit
   workpaper. Claude will recognize the skill from its description and use it automatically.

### Option B — Claude Code (copy into a project)

1. Clone this repo, or just download it.
2. Copy the `.claude/skills/tax-audit-workpaper/` folder into the `.claude/skills/` directory of whichever
   project/working folder you run Claude Code from (create `.claude/skills/` if it doesn't exist yet). Note
   `.claude` is a dot-folder — enable "show hidden files" in your file browser if you want to see it directly,
   or just use `cp -r`/drag-and-drop, which works without needing to see it.
3. Open that folder in Claude Code as usual and ask it to prepare a tax audit workpaper from a client's documents.

## What it produces

Given a folder of client documents, the skill drafts a clause-by-clause workpaper covering every applicable Form
3CD clause and outputs two files:

- A **Word document** (`.docx`) laid out to make copying answers into your tax audit software fast
- A **polished HTML file** with the same content, color-coded by review status, for a quick on-screen read

Every clause is tagged with one of four statuses so you know exactly where to spend your review time:

| Status | Meaning |
|---|---|
| Filled | Confident, fully-sourced answer |
| **Judgment call** | Facts are known, but the tax treatment needs your interpretation or sign-off |
| **Missing data** | A factual figure isn't in the documents provided — flagged, never invented |
| N/A | Actively confirmed as not applicable to this client |

The skill is built to **never fabricate a factual figure** it can't source from the documents — it will mark a
clause as missing data rather than guess a plausible-looking number. Judgment calls (is this expense disallowable?
does an exception apply?) get a best-guess answer with the reasoning flagged for your review.

## Current scope

Built for **Assessment Year 2026-27 / FY 2025-26**, under the Income-tax Act, 1961, Section 44AB, Forms
3CA/3CB-3CD — this is the current framework for this filing season. (The new Income-tax Act 2025 and its Form
No. 26 only take over from FY 2026-27 / AY 2027-28 onward; this skill will need updating, not just a figures
refresh, once that transition arrives.)

Numeric thresholds (TDS rates and limits, presumptive-scheme limits, cash-payment limits, due dates, etc.) are
hard-coded to AY 2026-27 figures in `references/thresholds-ay2026-27.md` rather than looked up live on every run —
refresh that file yourself each Finance Act cycle. See its "Next Year's Update Checklist" section for what to
re-check first.

## Repo layout

```
.claude/skills/tax-audit-workpaper/
├── SKILL.md                       Entry point — the workflow Claude follows when the skill runs
├── references/
│   ├── clauses-cover-and-applicability.md   Clauses 1-8a, Form 3CA vs 3CB, 44AB applicability
│   ├── clauses-9-to-17.md                   Books of account, method of accounting/ICDS, stock valuation
│   ├── clauses-18-to-26.md                  Depreciation & disallowances (40/40A/43B) — the highest-stakes block
│   ├── clauses-27-to-35.md                  GST/CENVAT, related party, TP/GAAR, loans, TDS/TCS
│   ├── clauses-36-to-44.md                  Deemed dividend, ratios, CbCR, GST expenditure breakup
│   ├── thresholds-ay2026-27.md              Authoritative numeric thresholds/rates/due dates
│   ├── workpaper_schema.md                  JSON schema the render script expects
│   └── schema/                              Official ITD e-filing JSON schemas (source of truth for field names)
├── scripts/
│   ├── extract_text.py            Dumps Excel/Word content to text (PDFs are read directly)
│   └── render_output.py           Renders the workpaper JSON into the final docx + HTML
└── assets/
    └── demo-client/                A synthetic test client with ~20 deliberately embedded issues
```

## How to use it

Once installed (either option above):

1. Hand Claude a client's source documents — trial balance, financials, AIS/TIS, Form 16, GST returns, bank
   statements, whatever you have — and ask it to prepare the tax audit workpaper for that client.
2. Claude reads the documents, consults the reference files to work out how each clause should be answered,
   builds a structured JSON, and runs `scripts/render_output.py` to produce the Word and HTML output.
3. Review both outputs — pay attention to anything flagged **judgment call** or **missing data** first — then
   re-key the confirmed answers into your tax audit software and file as usual, under your own UDIN.

### Try it on the demo client first

`assets/demo-client/` contains a complete fictional company ("Bright Horizon Textiles Private Limited") with
mixed PDF/Excel source documents and about 20 deliberately embedded issues — a cash payment disallowance, an
overdue MSME creditor, a missed TDS deduction, a Section 269SS cash-loan violation, a late employee PF deposit,
related-party payments, and more. Run the skill against it to see how it behaves before trusting it with a real
client. `assets/demo-client/_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md` lists what a correct run should catch — that file
is for your own validation only, never feed it to the skill as a source document.

## Keeping this current

- Refresh `references/thresholds-ay2026-27.md` after each year's Finance Act (Budget, typically February).
- Check whether CBDT has amended Form 3CD's clause structure again — it changed twice in the ~18 months before
  this skill was built (two clauses deleted, one added), so don't assume it's stable year to year.
- Plan for a structural rebuild once tax audits move to the new Income-tax Act 2025 / Form No. 26 framework
  (FY 2026-27 / AY 2027-28 onward).
