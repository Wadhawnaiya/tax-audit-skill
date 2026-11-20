# Training guide — Claude Code for Chartered Accountants: automating the tax audit first pass

A ready-to-run session plan built around the `tax-audit-workpaper` skill. It focuses on what is specific to
**Claude Code** — project folders, CLAUDE.md, skills as slash commands, subagents and hooks — using a real CA
workflow as the running example.

**Duration:** 3 hours (core) + 1 hour hands-on lab. **Audience:** CAs, audit managers, article assistants.
**Prerequisites:** a laptop with Claude Code (desktop app or terminal) signed in, Python 3.10+, and this kit.

---

## Before the session (trainer checklist)

1. Install Python and the two libraries the skill uses:
   ```
   pip install python-docx openpyxl
   ```
   (On Windows use `py -m pip install python-docx openpyxl`.) LibreOffice is optional — only for PDF previews.
2. Unzip `tax-audit-skill-complete.zip` to a folder such as `Documents/tax-audit-skill`.
3. Open that folder in Claude Code (desktop app: open/select the folder for a new session; terminal: `cd` into it
   and run `claude`).
4. Type `/` and check that `tax-audit-workpaper` appears in the list. If it does not, see Troubleshooting.
5. Do one full dry run on the demo client yourself (about 15–25 minutes) and keep the output open to compare.
6. Keep `demo-output/` and the answer key ready, but hidden from participants until Module 6.

---

## Module 1 — Why Claude Code for CA work (15 min)

Talking points:
- Chat answers questions; **Claude Code works inside a folder** — it reads Excel/PDF files, runs scripts, writes
  Word/Excel files and keeps a task list. That is what an audit first pass needs.
- Three properties CAs care about: it works on files on your machine; it runs deterministic scripts for the
  layout (the AI does the judgment, Python does the formatting); every step is visible and reviewable.
- What it is not: it does not file returns, sign reports or replace professional judgment. The CA's UDIN and DSC
  stay with the CA.

Demo (2 min): open the folder, ask "What is in this folder and what is it for?" — Claude reads CLAUDE.md and the
skill and explains the workspace.

## Module 2 — The workspace: folders and CLAUDE.md (20 min)

Walk through the kit:

```
tax-audit-skill/
├── CLAUDE.md                 ← firm rules Claude reads every session (memory)
├── clients/                  ← one folder per client (git-ignored)
├── demo-output/              ← reference run on the demo client
├── .claude/
│   ├── settings.json         ← hook: auto-validate every workpaper Claude writes
│   ├── hooks/                ← the hook script
│   ├── agents/               ← tax-audit-reviewer subagent
│   └── skills/
│       └── tax-audit-workpaper/   ← the skill (SKILL.md + references + scripts + demo client)
└── TRAINING-GUIDE.md
```

Teach:
- **CLAUDE.md is standing instructions.** Open it, read the conventions (Indian number format, never estimate a
  figure, penalties flagged not computed, confidentiality). Exercise: add one firm rule, e.g. "Always list
  related parties in alphabetical order", and show Claude following it.
- `/memory` (or editing CLAUDE.md directly) — personal vs project instructions.
- Folder discipline: originals untouched, `_work/` for working files, `output/` for deliverables.

## Module 3 — Skills: packaging a workflow (30 min)

Open `.claude/skills/tax-audit-workpaper/SKILL.md` on screen. Explain the anatomy:
- **Frontmatter** — `name` becomes the slash command; `description` tells Claude when to use it automatically;
  `metadata` holds the version. (Claude Code also accepts extras such as `argument-hint`; they are left out here so
  the same zip uploads cleanly to the Claude app.) Text after the command arrives in the body as `$ARGUMENTS`.
- **Body** — the workflow: scope → inventory → reconcile → draft → self-review → validate → render.
- **References** — loaded only when needed (the clause guides are ~280 KB; Claude reads the one it needs).
- **Scripts** — deterministic Python for extraction, validation, rendering.

Where skills live in Claude Code:
| Location | Who gets it |
|---|---|
| `<project>/.claude/skills/<name>/` | Everyone who opens this project folder |
| `~/.claude/skills/<name>/` (your home folder) | You, in every project |

Two ways to start it: type `/tax-audit-workpaper clients/<name>`, or just ask in plain English ("prepare the tax
audit workpaper for the documents in clients/sharma-traders") — the description triggers it.

Using the skill in the Claude app (chat) instead: upload `tax-audit-workpaper-skill.zip` in the Skills section
of Settings, and make sure code execution is enabled. Don't unzip it first.

## Module 4 — Live run on the demo client (40 min)

Prompt (copy-paste):

```
/tax-audit-workpaper .claude/skills/tax-audit-workpaper/assets/demo-client
Work in clients/demo/_work and put outputs in clients/demo/output.
```

Narrate as it runs:
1. The **task list** appears — this is how you follow long work.
2. **Inventory** — `INVENTORY.md` with refs D1–D9. Point out that the answer-key file is skipped (leading `_`).
3. **Reconciliations** — the turning point. Show how the 40(a)(ia) findings come from comparing P&L ledgers with
   the TDS return summary, not from any single file.
4. **Drafting** — Claude opens the clause guides for 18–26 first (highest risk).
5. **Hook fires** when the workpaper JSON is written — if there is an error (e.g. someone adds clause 28), Claude
   is forced to fix it.
6. **Render** — Word, HTML and Excel files appear in `output/`.

While it runs, ask the room: "Which documents would you cross-check for clause 26?" and compare with what Claude
does.

## Module 5 — Reading the output like a reviewer (30 min)

Open the three files.

**HTML** — the fastest review screen. Click *judgment calls*, then *with tax impact*. Search "Rajesh".
**Word** — the CA attention list (sorted by priority and amount), the computation impact summary, the
reconciliations table, then clause by clause with source citations and client queries; Appendix A is the client
request list.
**Excel review register** — the working paper for sign-off: reviewer comment, sign-off dropdown, progress %, an
impact sheet with live formulas, and a client query tracker with status.

Discussion points from the demo client:
- 43B(h) Om Fabrics Rs. 6.5 lakh — why it appears in clauses 22 and 26 but is disallowed once (Notification
  23/2025).
- Employee PF Rs. 42,000 — why there is no grace period (Checkmate Services).
- Interest Rs. 5 lakh on a Rs. 3.5 lakh loan for 207 days ≈ 252% a year — what does a reviewer do with that?
- Club subscription and voluntary CSR — why the skill marks them judgment instead of disallowing automatically.

## Module 6 — Subagents: an independent reviewer (20 min)

Explain: a **subagent** is a separate Claude with its own instructions and a fresh context. It did not write the
draft, so it does not "mark its own homework".

Show `.claude/agents/tax-audit-reviewer.md`, then run:

```
Use the tax-audit-reviewer subagent to review clients/demo/_work/<client>_workpaper.json
against the documents in .claude/skills/tax-audit-workpaper/assets/demo-client.
```

Then score the run against the answer key:

```
Now open .claude/skills/tax-audit-workpaper/assets/demo-client/_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md
and score the workpaper using its Part C scoring sheet. List what was missed.
```

Use `/agents` to show how to create and edit subagents.

## Module 7 — Hooks: guardrails that always run (15 min)

Open `.claude/settings.json`. Explain: a **hook** runs a command automatically on an event — here, after every
file write, any `*workpaper*.json` is validated. Errors (deleted clause, unexplained flag, filled clause with no
answer) are sent back to Claude, which must fix them.

Live test: ask Claude to "add clause 28 to the demo workpaper". The hook blocks it and Claude explains why.

Use `/hooks` to view configured hooks. Message: hooks turn firm policy into something that can't be skipped.

## Module 8 — Making it yours (15 min)

- **Your details on every output:** add a `preparer` block to the workpaper JSON, or change `DEFAULT_PREPARER`
  in `scripts/wp_common.py`.
- **Next year:** refresh `references/thresholds-ay2026-27.md` using its update checklist. From tax year 2026-27
  the audit moves to **Form No. 26** under the Income-tax Act 2025 — the skill says so and stops; the next
  version needs a rebuild (see `references/form-26-transition.md`).
- **Your firm's checklist:** add your own red flags to `references/review-checklist.md`.
- **Improving the skill with Claude:** "Read the skill and suggest three improvements based on today's run" —
  then review the diff before accepting.

## Hands-on lab (60 min)

Teams of 2–3. Each team:
1. Copies the demo client to `clients/team-N/` and **changes three facts** (e.g. pays Om Fabrics on 25-Mar-2026,
   adds a Rs. 25,000 cash payment, removes the Q2 rent TDS problem).
2. Runs the skill, then the reviewer subagent.
3. Checks whether the workpaper reflects their changes correctly, and presents one thing Claude got right that
   surprised them and one thing it got wrong.

Scoring: Part C of the answer key (66 points; a good run scores 50+).

---

## Prompt cheat sheet

| Goal | Prompt |
|---|---|
| Full draft | `/tax-audit-workpaper clients/<name>` |
| One issue only | `Using the tax audit skill, check only 43B(h) and clause 22 for clients/<name>.` |
| Client request letter | `Turn Appendix A of the workpaper into an email to the client, grouped by document.` |
| Explain to a junior | `Explain clause 21(b) for this client as if to a first-year article.` |
| Second opinion | `Use the tax-audit-reviewer subagent on clients/<name>/_work/<file>.json.` |
| Revise after client reply | `The client sent PF challans in clients/<name>/new/. Update clause 20 and re-render.` |

## Professional-responsibility talking points (keep these in every session)

- The output is a draft workpaper. The CA reviews every flagged item and signs under their own UDIN.
- Client data stays on the machine and inside the project folder; don't paste PAN/bank details into web tools.
- The skill never estimates a missing figure — teach participants to treat any untraceable number as a defect.
- Keep the review register as evidence of review.

## Troubleshooting

| Problem | Fix |
|---|---|
| `/tax-audit-workpaper` not in the list | Check the folder is `.claude/skills/tax-audit-workpaper/SKILL.md` inside the folder you opened (hidden `.claude` folder). Restart the session. |
| `No module named docx` / `openpyxl` | `pip install python-docx openpyxl` (Windows: `py -m pip install ...`). |
| `python3` not found on Windows | Claude will use `python` or `py`; the hook already falls back to `python`. |
| Hook doesn't fire | Open `/hooks`; make sure the project's `.claude/settings.json` is loaded and that the file name contains `workpaper` and ends in `.json`. |
| Scanned PDFs give no text | Expected — Claude reads them with its built-in PDF/image reading. |
