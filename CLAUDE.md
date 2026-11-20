# Tax audit workspace — instructions for Claude

This folder is a CA firm's tax audit workspace. Claude Code reads this file at the start of every session.

## How work is organised
- Each client gets a folder: `clients/<client-name>/`. Raw documents go straight in that folder.
- Claude's working files go in `clients/<client-name>/_work/` (extracted text, workpaper JSON).
- Final outputs go in `clients/<client-name>/output/`.
- Never edit or delete the client's original documents.

## How to prepare a tax audit
- Use the **tax-audit-workpaper** skill (`/tax-audit-workpaper clients/<client-name>`). Follow its steps in order;
  do not skip the reconciliation and self-review steps.
- Name the workpaper `clients/<client-name>/_work/<client>_workpaper.json` — a hook validates any file named
  `*workpaper*.json` every time it is written, and blocks on errors.
- When the draft is rendered, ask the **tax-audit-reviewer** subagent to review it before handing it to the CA.

## Firm conventions
- Amounts in Indian format (12,34,567); dates as DD-MMM-YYYY; "Rs." not "INR".
- Every figure must cite its document. If a fact is not in the documents, mark it missing and draft the client
  query — never estimate it.
- Penalties (271B, 271D, 271H…) are flagged as exposures, never computed.
- Preparer details on the outputs come from the `preparer` block in the workpaper JSON (default: the firm's
  details in `scripts/wp_common.py`).

## Confidentiality
- Client documents contain PANs, bank details and salaries. Do not paste them into web searches, external tools
  or anything outside this folder. Web search is fine for law and due-date checks only.
- Do not commit `clients/` to git or share it; it is excluded by `.gitignore`.

## Training mode
- `.claude/skills/tax-audit-workpaper/assets/demo-client/` is a synthetic company for practice.
- Its `_ANSWER_KEY_DO_NOT_FEED_TO_SKILL.md` is for the trainer. Do not open it during a practice run unless the
  user explicitly asks to score a finished run.
