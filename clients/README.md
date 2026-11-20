# clients/

Put each client's documents in its own folder here, for example:

```
clients/
  sharma-traders/
    trial_balance.xlsx
    financial_statements.pdf
    ais.pdf
    gstr9.xlsx
    ...
```

Then, in Claude Code:

```
/tax-audit-workpaper clients/sharma-traders
```

Claude will create `_work/` (extracted text + workpaper JSON) and `output/` (Word, HTML, Excel) inside the
client folder. This folder is git-ignored — client data never leaves your machine through the repo.
