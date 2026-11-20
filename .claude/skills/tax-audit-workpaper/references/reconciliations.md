# Mandatory cross-document reconciliations

Most tax audit findings are not in any single document — they appear when two documents that should agree don't.
Run every check below that the client's documents allow, record each one in the workpaper's `reconciliations`
array (even when it matches), and carry every unexplained difference into the clause it affects.

Record format: `item`, `source_a`, `amount_a`, `source_b`, `amount_b`, `difference`, `status`
(`matched` / `explained` / `unexplained`), `explanation`. Cite documents by their inventory ref (D1, D2 …).

## 1. Turnover and income

| Check | Source A | Source B | Feeds clause |
|---|---|---|---|
| Turnover | Financial statements / TB sales ledgers | GSTR-9 (or 12 × GSTR-3B), and AIS/TIS GST turnover if shown | 8, 40, 44AB applicability |
| Turnover vs 26AS/AIS receipts | Books (sales, professional receipts) | AIS TDS/TCS entries (194C/194J/194Q received) | 16, 40 |
| Other income | TB interest, dividend, rent, misc. | AIS interest/dividend/SFT | 16, 21(h), 36A |
| Export turnover | Books | Shipping bills / GSTR-1 zero-rated | 16 (export incentives) |

## 2. TDS — the richest source of findings

For every TDS section, compare **the P&L ledger total** with **the amount reported in the TDS returns**:

| P&L ledger | Section | Threshold FY 2025-26 (see thresholds file) |
|---|---|---|
| Salaries, directors' remuneration | 192 | slab |
| Interest to non-banks (incl. directors, relatives, unsecured loans) | 194A | Rs. 10,000 |
| Contract labour, job work, freight, advertisement, repairs by contractors | 194C | 30,000 / 1,00,000 |
| Commission, brokerage | 194H | 20,000 |
| Rent (building, plant, furniture) | 194-I | 50,000 per month |
| Professional, legal, audit, technical fees; director sitting fees | 194J | 50,000 (no threshold for director fees) |
| Purchases of goods (if buyer's prior-year turnover > Rs. 10 crore) | 194Q | 50 lakh per seller |
| Payments to partners (firms/LLPs) | 194T | 20,000 |

- A ledger with **no** matching return entry, a quarter that is **missing**, or a return amount **lower** than the
  ledger are each a potential s.40(a)(ia) disallowance (30%) in clause 21(b) and a clause 34 exception.
- Payee-wise thresholds mean an aggregate gap is not automatically a default. Disallow only what is confirmed;
  mark the rest `missing` with a request for party-wise ledgers, and state the maximum exposure in the notes.
- Compare Form 16 / 16A samples with the return totals — a sample larger than the whole return means the return
  data is incomplete.

## 3. GST

| Check | Source A | Source B | Feeds clause |
|---|---|---|---|
| ITC availed | GSTR-3B (12 months) | GSTR-9 / electronic credit ledger | 27(a) |
| Blocked credit reversed | GSTR-3B reversal | P&L ledger | 27(a), 21(a) |
| GST paid | GSTR-3B cash paid | Bank statement / statutory dues ledger | 26 (43B(a)) |
| Expenditure by supplier registration | Purchase/expense ledgers | GSTR-2B supplier GSTINs | 44 |

## 4. Fixed assets and depreciation

- Book depreciation (P&L) vs Income-tax depreciation (FAR / clause 18). A difference is normal — but check the
  accounting-policy note; if it claims they are "aligned" and they aren't, flag it.
- Sale proceeds in the FAR vs bank receipts; additions vs invoices (dates decide full vs half rate).
- Additions in the FAR vs capital creditors / CWIP movement.

## 5. Payables, loans and related parties

| Check | Source A | Source B | Feeds clause |
|---|---|---|---|
| MSME dues | FS MSME note | MSME ageing / TB | 22, 26 |
| Loans taken / repaid | Loan register | Bank statement (mode!) / TB | 31 |
| Related-party payments | AS-18 / Ind AS 24 note | Related-party register / P&L ledgers | 23 |
| Interest to lenders | P&L interest ledger | Loan balance × rate × period | 23, 21(b) |
| Statutory dues payable | TB | Challans after year end | 26 |

**Implied-rate test:** interest ÷ (average loan × days/365). An implied rate far above market means either the
loan register is incomplete or the payment is excessive (s.40A(2)(a)).

## 6. Accounts integrity

- TB debits = TB credits. If not, find out why before relying on it.
- TB P&L ledgers vs FS line items (revenue, cost of materials, employee cost, finance cost, other expenses, PBT).
- Tax expense / deferred tax: P&L movement vs balance-sheet movement.
- Inventory: FS vs TB vs stock register (quantities feed clause 35).

## How to record the outcome

- `matched` — amounts agree (state any rounding).
- `explained` — they differ for a reason you can show from the documents (write it).
- `unexplained` — they differ and the documents don't say why. Every `unexplained` item must also appear as a
  `client_query` on the clause it affects, and usually makes that clause `judgment` or `missing`.
