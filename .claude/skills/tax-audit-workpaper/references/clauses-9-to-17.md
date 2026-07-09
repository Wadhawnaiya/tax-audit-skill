# Form 3CD — Clauses 9 to 17 (AY 2026-27 / FY 2025-26)

Reference for drafting the Form 3CD tax-audit workpaper under section 44AB of the Income-tax Act, 1961. Each clause below states: the statutory basis, the exact JSON schema fields the filled value must map to (from `schema_3CB.json` / `3CB_structure.txt`), the source documents, a step-by-step extraction procedure, common junior-staff mistakes, and the missing-data protocol.

**Missing-data protocol (applies to every clause in this file):**
- Any **factual figure, date, name, or amount** not found in the source documents → write `[MISSING — CONFIRM WITH CLIENT]`. Never estimate, round, or infer a number that isn't in the records.
- Any **classification, characterization, or interpretive call** (e.g., "is this a change in nature of business or just a new product line," "is this method deviation material") → make the call, but flag it `[JUDGMENT CALL — CA TO CONFIRM]` so the signing CA reviews it before the report is finalized.

---

## Clause 9 — Firm / AOP: Partners/Members, Profit-Sharing Ratio, and Changes

**Applicability:** Only where assessee `Status` (Part A) is Firm, LLP, or AOP/BOI. Skip entirely (leave clause not applicable) for individuals, companies, HUF, trusts, etc.

**Statutory basis:** Clause 9(a) and 9(b) of Form 3CD — no separate charging section; this is a factual disclosure clause tied to the constitution of the assessee.

**Schema mapping:**
- 9(a) — current partners/members and profit-sharing ratio → `Form3cdFirmAopDetailNew.Form3cdFirmAopDetailPK[]` with `ChangeType = CURR_PROF_SHARE`, `FirmAopDesc` (partner/member name — max 100 chars), `FirmAopPerc` (profit share %, up to 99.99).
- 9(b) — changes during the year → `Form3cdChangeInPartners[]`: `DateOfChange`, `NameOfPartner`, `TypeOfChange` (`ADD`|`DEL`|`CHANGE`), `OldProfShareRatio`, `NewProfShareRatio`, `Remarks`. Leave the array empty if there was no change during the year — do not fabricate a "no change" entry.

**Source documents:** Original partnership deed / LLP agreement; any supplementary/reconstitution deeds executed during the year; minutes of partners'/members' meetings; Form 3CD and financial statements of the immediately preceding year (for opening comparatives); LLP Form 3/4 filed with MCA (for LLPs, evidences admission/retirement and ratio change effective dates).

**Extraction procedure:**
1. Pull the *original* deed plus every supplementary deed executed up to the end of the previous year — the current ratio is the cumulative effect of all deeds, not just the latest one.
2. List every partner/member as of the year-end (31 March or dissolution date) with their closing profit-sharing ratio, for 9(a). Ratios must foot to 100% (or to a stated balance held by the firm itself, if any) — if they don't, flag `[JUDGMENT CALL — CA TO CONFIRM]` and re-check for a missed deed.
3. Scan deed execution dates and minute-book entries falling between the start and end of the current previous year. For each: identify whether it is an admission (`ADD`), retirement/death (`DEL`), or a pure ratio reshuffle among existing partners (`CHANGE`), capture the `DateOfChange`, `OldProfShareRatio` and `NewProfShareRatio` for the partner(s) affected, and a one-line `Remarks` (e.g., "Admitted as partner vide deed dated ...", "Retired vide deed dated ...").
4. Cross-check total ratios before and after each change event — they must each foot to 100%.
5. For LLPs, also verify against MCA LLP Form 3/4 filings for the same period; a mismatch between the deed and the MCA filing is common and should be flagged `[JUDGMENT CALL — CA TO CONFIRM]`.

**Common junior-staff mistakes:**
- Reporting only the latest deed's ratios without checking for an intra-year change that a supplementary deed superseded again.
- Missing a partner who retired mid-year and was already dropped from the current partner list — 9(b) still requires reporting that retirement even though they're absent from the closing list in 9(a).
- Confusing capital-sharing ratio with profit-sharing ratio (deeds sometimes specify both; only profit-sharing ratio is required here).
- Forgetting minority/negative or unequal special ratios (e.g., a partner entitled only to a fixed remuneration and no profit share — report as 0% or as per deed wording, not omitted).

---

## Clause 10 — Nature of Business or Profession; Change During the Year

**Statutory basis:** Clause 10(a) and 10(b) of Form 3CD.

**Schema mapping:**
- 10(a) — current nature of business → `F3cdFirmAopDtlNatOfBusiness.Form3cdFirmAopDetailPK[]` with `ChangeType = CURR_NATURE_BUSNS`, `Sector` (2-digit ITD sector code), `FirmAopDesc` (specific ITD sub-code:description, e.g. `16002:Accounting, book-keeping and auditing profession`). Multiple entries allowed if the assessee has more than one distinct line of business.
- 10(b) — change in nature of business during the year → `F3cdFirmAopDtlChangeInNature.Form3cdFirmAopDetailPK[]` with `ChangeType = CHNG_NATURE_BUSNS`, `FirmAopBuss` (`Added`|`Discontinued`), `Sector`, `FirmAopDesc`. Leave empty if no change.

**ITD Sector classification (23 sectors, used as the first-level dropdown in the utility):**
`01` Agriculture, Animal Husbandry & Forestry · `02` Fish Farming · `03` Mining and Quarrying · `04` Manufacturing · `05` Electricity, Gas and Water · `06` Construction · `07` Real Estate and Renting Services · `08` Renting of Machinery · `09` Wholesale and Retail Trade · `10` Hotels, Restaurants and Hospitality Services · `11` Transport and Logistics Services · `12` Post and Telecommunication Services · `13` Financial Intermediation Services · `14` Computer and Related Services · `15` Research and Development · `16` Professions · `17` Education Services · `18` Health Care Services · `19` Social and Community Work · `20` Culture and Sport · `21` Other Services · `22` Extra Territorial Organisations and Bodies · `23` Co-operative Society Activities.

Within each sector, a detailed sub-code applies (~370 total codes). Frequently used sub-codes for practicing-CA clients:
- `00001` Share of Income from Firm only (for a partner-assessee whose only income is a share from a firm).
- `09005` General commission agents, commodity brokers and auctioneers; `09021`–`09028` various retail/wholesale trade categories.
- `14001` Software development; `14002` Other software consultancy.
- `16001` Legal profession; `16002` Accounting, book-keeping and auditing profession; `16003` Tax consultancy; `16004` Architectural profession; `16005` Engineering and technical consultancy; `16013` Business and management consultancy; `16019` Other professional services n.e.c.; `16019_1` Medical Profession.
- `18001`–`18018` various healthcare categories (hospitals, clinics, dental, ayurveda, diagnostic labs, etc.).
- `06002` Civil contractors (building of complete constructions or parts); `07002`–`07005` real estate operating/development/renting.
- `11008` Freight transport by road (relevant for section 44AE goods-carriage clients).

**Source documents:** GST registration certificate (nature of business/HSN-SAC codes), MSME/Udyam registration, previous year's Form 3CD (for continuity), MOA/partnership deed object clause, management representation, first page of financial statements/notes (often state "principal business activity").

**Extraction procedure:**
1. Identify the actual, operative business — not just what the deed/MOA permits. Multiple permitted objects in the deed don't all need reporting; only what was actually carried on during the year.
2. Match the activity description to the closest ITD sub-code. If genuinely no close match exists among the ~370 codes, this is itself a judgment call — pick the nearest "n.e.c." (not elsewhere classified) code within the correct sector and flag `[JUDGMENT CALL — CA TO CONFIRM]`.
3. Compare this year's classification against the **prior year's Form 3CD** clause 10(a) entry. If the code/sector differs from last year, determine why: (a) genuine change in business (report under 10(b)), or (b) just a more precise re-classification of the same activity (no 10(b) entry needed, but note the reason internally).
4. For 10(b): scan for any new revenue stream started mid-year (new GST HSN/SAC added, new bank current account for a new line, new segment in financial statements) → report as `Added`; and any activity ceased (asset sold off, segment discontinued, licence surrendered) → report as `Discontinued`. Capture the sector + sub-code for the added/discontinued activity.
5. If the entity is a pure investment/holding company or a partner drawing only firm-share income, use `00001`.

**Common junior-staff mistakes:**
- Picking the sub-code that matches the entity's *name* rather than its actual income-generating activity (e.g., classifying a trading company that also does minor job-work purely as "manufacturing" because its name says "Industries").
- Not flagging 10(b) when a business is added/discontinued mid-year but continues to appear combined in one P&L line — the addition/discontinuation is a factual event independent of how the P&L is presented.
- Reporting a temporary suspension of business (e.g., COVID-style closure with intent to resume) as "Discontinued" — a genuine discontinuation is a permanent cessation; a temporary halt is not a 10(b) event. Treat this classification as `[JUDGMENT CALL — CA TO CONFIRM]`.

---

## Clause 11 — Books of Account

**Statutory basis:** Section 44AA (books of account prescribed to be maintained) and Rule 6F (for specified professionals). Clause 11(a)/(b)/(c) of Form 3CD.

**Schema mapping:** All three sub-clauses live under the two `BooksOfAccType` values inside `Form3cdBooksOfAccLst[]` / `Form3cdBooksOfAccLstAddress[]` (both keyed by `Form3cdBooksOfAccLstPK`):
- 11(a) — books prescribed under s.44AA → `Form3cdBooksOfAccLst[]` with `BooksOfAccType = SEC44AA`, `BooksDetail` (name of the prescribed book, max 100 chars). One entry per prescribed book (cash book, journal, ledger, etc., or the specific books under Rule 6F for specified professions).
- 11(b) — books of account actually maintained, with address → `Form3cdBooksOfAccLstAddress[]` with `BooksOfAccType = BOAM` ("Books Of Account Maintained"), `BooksDetail`, and `AddressDetail` (AddrDetail1/2, City, StateCode, CountryCode, PinCode). **One entry per (book, location) combination** — if the same book is kept at more than one address (e.g., head office books vs. branch books), create a separate array entry for each location so the `Form3cdBooksOfAccLstAddress` output correctly reflects multi-location record-keeping.
- 11(c) — books examined by the auditor → `Form3cdBooksOfAccLst[]` with `BooksOfAccType = LBEX` ("List of Books EXamined"), `BooksDetail`. This list should normally equal or be a documented subset of 11(b); it must never include a book not listed as maintained.

**Section 44AA / Rule 6F applicability — who must maintain *specified* books:**
- **Specified professions** (legal, medical, engineering, architectural, accountancy, technical consultancy, interior decoration, authorised representative, film artist, company secretary, and — per later CBDT notification — information technology professionals) with gross receipts exceeding ₹1,50,000 in any of the three preceding years (or, for a new profession, likely to exceed ₹1,50,000 in the current year) must maintain the specific books prescribed under Rule 6F: cash book, journal (if mercantile), ledger, carbon copies of bills/receipts above ₹25, original bills/receipts for expenditure above ₹50, and for medical professionals additionally a daily case register (Form 3C) and inventory of drugs/consumables.
- **Specified professions below the Rule 6F threshold**, and **all other businesses/professions** — s.44AA(2) requires only that "such books of account and other documents as may enable the Assessing Officer to compute total income" be kept, if income exceeds ₹2,50,000 or turnover/gross receipts exceed ₹25,00,000 in any of the three preceding years (revised monetary limits for individuals/HUF: income > ₹2,50,000 or turnover > ₹25,00,000; for other assessees, income > ₹1,20,000 or turnover > ₹10,00,000 — apply the limits current for the assessment year and flag the specific figures used as a `[JUDGMENT CALL — CA TO CONFIRM]` if there is any doubt about which limb applies). There is no *prescribed format* here — 11(a) in that case is reported as "no books prescribed under section 44AA(1); books maintained as per section 44AA(2)."
- If the assessee is a company or covered by presumptive taxation without opting out, note interaction with 44AA is still separately assessed (44AA applies regardless of the presumptive election on the same facts).

**Source documents:** Nature of business/profession (from clause 10, and turnover/receipts from the trial balance) to determine 44AA applicability; client's books/records index or accounting software module list (Tally/Zoho/QuickBooks company list); registered office and branch addresses (from PAN/GST registration, MOA, or client confirmation); engagement letter / audit program listing books actually inspected during fieldwork.

**Extraction procedure:**
1. Determine 44AA applicability class using clause 10's nature-of-business classification plus gross receipts/turnover/income from the trial balance — specified profession above ₹1,50,000 receipts → Rule 6F books listed individually in 11(a); otherwise → general s.44AA(2) statement.
2. Build 11(b) from the actual accounting records: typically Cash Book, Bank Book, Purchase Register, Sales Register, Journal, General Ledger, Stock Register (if maintained), Fixed Asset Register. List exactly what the client maintains — do not assume a standard list; if the client's software maintains a consolidated general ledger without discrete cash/bank books, describe it as such.
3. For each book in 11(b), determine the physical/digital location where it is kept (registered office, branch, accountant's office, cloud server/registered office of accounting service provider) and populate `AddressDetail` per location. If the client maintains one consolidated set of books at a single address, all `BooksDetail` entries share that one address.
4. Build 11(c) from the audit team's actual working papers/fieldwork index — this must reflect what was *actually examined*, not a copy-paste of 11(b). If a book listed in 11(b) was not examined (e.g., a dormant subsidiary ledger), it should be excluded from 11(c) with a note.
5. Reconcile: every book in 11(a) (if prescribed) should generally appear in 11(b) as maintained; if a prescribed book is not maintained, that is itself a reportable observation elsewhere in the audit (para 3/Annexure of Form 3CB) — flag `[JUDGMENT CALL — CA TO CONFIRM]`.

**Common junior-staff mistakes:**
- Listing generic "books of account" as a single 11(b) entry instead of the actual granular list (cash book, ledger, etc.) — the schema expects one `BooksDetail` entry per book.
- Forgetting the address entirely, or using the registered office address by default when books are actually held at the tax consultant's/accountant's office — always confirm physical location with the client, don't assume.
- Copying 11(b) verbatim into 11(c) without actually cross-checking against the audit fieldwork papers.
- Missing Rule 6F-specific books (case register, stock of drugs) for medical professionals, or carbon-copy/bill retention requirements for other specified professionals — these are separate from the generic cash book/ledger/journal.
- Applying Rule 6F books to a profession not in the specified list (e.g., treating a general trading business as a "specified profession").

---

## Clause 12 — Presumptive Income Included in the P&L

**Statutory basis:** Sections 44AD (eligible business, resident individuals/HUF/firms other than LLP), 44ADA (specified professionals), 44AE (owning ≤10 goods carriages), 44B (shipping business of non-residents), 44BB (non-resident providing services/facilities for oil exploration), 44BBA (non-resident operating aircraft), 44BBB (foreign company doing turnkey civil-construction of a power project), and the First Schedule (insurance business — general/life). Clause 12 of Form 3CD.

**Schema mapping:** `Form3cdProfGainsPresum[]` — one entry per presumptive section applicable: `SectionNo` (enum: `44AD`, `44ADA`, `44AE`, `44AF` [legacy, retail trade, largely obsolete post-44AD], `44B`, `44BB`, `44BBA`, `44BBB`, `44BBC`, `44BBD`, `CHAPXIIG`, `FIRSTSCH`, `OTHER`), `OtherSection` (free text, only if `SectionNo = OTHER`), `Amount` (the presumptive profit/gains amount actually credited to/included in the P&L, integer).

**Note on scope:** Clause 12 only asks whether the P&L *includes* profits assessable on a presumptive basis — this arises typically when an assessee is otherwise subject to tax audit under s.44AB (e.g., turnover exceeds the presumptive threshold, or the assessee has other non-presumptive business requiring audit) but *also* has one segment/vertical genuinely eligible for and opted under a presumptive section. It is not asking whether the assessee is under presumptive taxation overall — a pure 44AD/44ADA case usually would not need a tax audit at all unless profit is declared below the presumptive rate and total income exceeds the basic exemption limit, or turnover exceeds the presumptive ceiling.

**Source documents:** Trial balance / P&L segment-wise breakup; computation of total income (ITR computation sheet) showing the presumptive income workings; goods-carriage registration certificates and ownership schedule (for 44AE — count of vehicles and months held); professional receipts breakup (for 44ADA); tonnage/freight receipts details (for 44B, shipping); prior year ITR/tax audit report for continuity of the presumptive election (44AD/44ADA carry a 5-year lock-in on exit if opted out early).

**Extraction procedure:**
1. Identify if the assessee runs more than one distinct business/professional activity, and whether any one of them independently qualifies for and has been reported on a presumptive basis in the income computation.
2. For 44AD: confirm eligible business (not commission/brokerage/agency business, not a business referred in 44AE, and turnover/gross receipts ≤ ₹2 crore [or ≤ ₹3 crore where cash receipts ≤5% of total receipts, current enhanced threshold] ) and that presumptive profit (≥8%/6% of turnover per receipt mode) is what's actually picked up in the computation.
3. For 44ADA: confirm it is a specified profession under s.44AA(1) with gross receipts ≤ ₹50 lakh (or ≤ ₹75 lakh with the enhanced cash-receipt condition), and presumptive income = 50% of gross receipts (or higher, if higher income is actually declared/credited).
4. For 44AE: pull the goods-carriage register — number of vehicles, whether heavy goods vehicle or other, and number of months held during the year; compute presumptive income per vehicle per the prescribed per-ton/per-vehicle rate and tie to the amount actually credited to the P&L.
5. For non-resident presumptive sections (44B, 44BB, 44BBA, 44BBB) — verify residential status and nature of receipts (freight, service fees for oil exploration, aircraft operation, turnkey power-project construction respectively) match the section; these are rare for a typical Indian SME/practicing-CA client base but must be checked if the assessee has such a foreign-company/non-resident engagement.
6. For insurance business (First Schedule) — applies only to insurers; use `FIRSTSCH`.
7. Populate `Amount` with the exact presumptive profit figure as it appears credited in the P&L/included in the computation — not the gross turnover of that segment.
8. If no presumptive income is included anywhere in the P&L, leave `Form3cdProfGainsPresum` empty — do not force an entry.

**Common junior-staff mistakes:**
- Reporting the gross turnover of the presumptive segment instead of the presumptive *profit* amount in `Amount`.
- Missing a small secondary activity (e.g., a manufacturer who also owns 3 trucks given on hire, reportable under 44AE) because attention is only on the main audited business.
- Applying 44AD to a commission/agency business or to a business already covered under 44AE (both are excluded from 44AD eligibility).
- Not checking the 5-year re-entry lock-out for a client who opted out of 44AD/44ADA in an earlier year and is now trying to opt back in early — this affects whether the presumptive claim is even valid, not just how it's disclosed. Flag as `[JUDGMENT CALL — CA TO CONFIRM]`.

---

## Clause 13 — Method of Accounting and ICDS Adjustments

**Statutory basis:** Section 145(1) (method of accounting — cash or mercantile only), section 145(2) (ICDS notified by CBDT), section 145(3) (AO's power to reject books/best judgment if ICDS not followed). Clause 13(a)–(f) of Form 3CD.

**Schema mapping:**
- 13(a) — method of accounting → `Form3cdChngMethAccDtl.Detail` (enum `01` = Cash system, `02` = Mercantile system).
- 13(b)/(c) — change in method from preceding year, and effect → `Form3cdChngMethAccVal.Form3cdChngMethAccValPK[]` (max 1 item) with `AccType = CHANGE_ACC`, `Particulars` (description of the change), `IncreaseProfits`, `DecreaseProfits`.
- 13(d) — whether ICDS adjustment required → implied by whether any `Form3cdChngMethAccValChange` entries exist (with `AccType = DEVIATION_VAL`); if none, 13(d) is answered "No".
- 13(e) — ICDS-wise accounting policy disclosures → `Form3cdDisclVal.Form3cdDisclValPK[]`, one entry per ICDS with `AccType = DEVIATION_VALUE`, `Icds` (enum `ICDSI` … `ICDSX`), `Disclosure` (free text, up to 2000 chars) — **this is mandatory for all 10 ICDS regardless of whether there's an adjustment**; every ICDS needs at least a "no adjustment, policy is consistent with ICDS" style disclosure, or a substantive one if it deviates.
- 13(f) — net profit/loss effect of ICDS adjustments, ICDS-wise → `Form3cdChngMethAccValChange.Form3cdChngMethAccValChangePK[]`: `AccType = DEVIATION_VAL`, `Icds` (enum `ICDSI`…`ICDSX`), `IncreaseProfits`, `DecreaseProfits`, `NetEffect`; plus `Form3cdChngMethAccValTotal[]` for the aggregate `TotalIncProfit`, `TotalDecProfits`, `TotalNetProfit` across all ICDS.

**The 10 ICDS (for populating 13(e) disclosure text):**
| ICDS | Title | Typical disclosure if no deviation |
|---|---|---|
| ICDS I | Accounting Policies | "Accrual basis and going concern followed; no change in accounting policy affecting current year's income; material accounting policies disclosed in financial statements." |
| ICDS II | Valuation of Inventories | "Inventories valued at lower of cost (FIFO/weighted average, as applicable) and net realisable value, consistent with ICDS II." |
| ICDS III | Construction Contracts | "Percentage of completion method applied for construction contracts, where applicable." (State "Not applicable" if assessee has no construction contracts.) |
| ICDS IV | Revenue Recognition | "Revenue from sale of goods recognised on transfer of significant risks/rewards; service revenue on percentage completion/straight-line as applicable, consistent with ICDS IV." |
| ICDS V | Tangible Fixed Assets | "Fixed assets recognised and valued per ICDS V; no deviation." |
| ICDS VI | Effects of Changes in Foreign Exchange Rates | "Foreign currency transactions/monetary items translated as per ICDS VI; no deviation." (Or "Not applicable" if no foreign-currency exposure.) |
| ICDS VII | Government Grants | "Government grants recognised per ICDS VII." (Or "Not applicable" if none received.) |
| ICDS VIII | Securities | "Securities held as stock-in-trade valued at lower of actual cost or NRV, category-wise, per ICDS VIII." (Or "Not applicable" for non-trading assessees.) |
| ICDS IX | Borrowing Costs | "Borrowing costs directly attributable to acquisition/construction of qualifying assets capitalised per ICDS IX; other borrowing costs expensed." |
| ICDS X | Provisions, Contingent Liabilities and Contingent Assets | "Provisions recognised only where a present obligation exists and a reliable estimate can be made, per ICDS X; contingent liabilities disclosed, not provided; contingent assets not recognised." |

**Source documents:** Financial statement "Significant Accounting Policies" note; trial balance; prior year Form 3CD (for 13(a)/(b) comparative — was mercantile followed last year too?); fixed asset schedule and borrowing cost workings (ICDS IX capitalization); inventory valuation note (ICDS II — cross-check against clause 14); revenue recognition note / long-term contract schedules (ICDS III/IV); contingent liability note and provisions schedule (ICDS X); foreign exchange gain/loss ledger (ICDS VI).

**Extraction procedure:**
1. **13(a):** Read the financial statements' basis-of-preparation note. Virtually all corporate/LLP/firm clients with statutory audit use mercantile (accrual). A cash-basis client is rare — usually a very small proprietary professional practice. Confirm from the trial balance behavior (are expenses/income booked on payment/receipt, or on accrual with payables/receivables balances?).
2. **13(b)/(c):** Compare this year's stated method against last year's Form 3CD clause 13(a). If unchanged, mark "No" for 13(b) and leave 13(c)/`Form3cdChngMethAccVal` empty. If changed (e.g., cash → mercantile), describe the change in `Particulars` and compute its P&L effect: identify income/expense items that would have been recognised in a different year under the old vs. new method, and quantify the double-count or omission for the current year in `IncreaseProfits`/`DecreaseProfits`.
3. **13(d)–(f) — practical approach for SME clients:** Most SME/professional clients that already prepare financial statements under (Ind)AS on accrual/mercantial basis have **minimal to nil ICDS adjustments**, because ICDS is substantially aligned to AS for most day-to-day items. Do not assume zero, though — specifically check these four areas, which are where real-world ICDS-vs-books gaps most commonly arise:
   - **ICDS II (inventory):** ICDS mandates FIFO/weighted-average only (no LIFO) and requires including certain costs (e.g., excludes borrowing cost typically, but check treatment of by-products/scrap and standard costing conventions). Compare the financial statement's stated inventory valuation policy against ICDS II — a LIFO-basis client, or a standard-cost basis not adequately adjusted to actual cost, needs an adjustment.
   - **ICDS III/IV (construction contracts / revenue recognition):** If the client is a real-estate developer, civil contractor, or provides long-duration services and books revenue only on invoice/completion instead of percentage-of-completion, or defers income beyond what ICDS IV permits (e.g., excessive prudence-based deferral of revenue where ICDS doesn't allow anticipated-loss-only recognition the same way AS does), an adjustment is likely. Post-Ind AS 115 (or AS 9 replacement), compare the accounting-standard revenue figure against the ICDS-required figure — timing differences (especially around advances, retention money, service contract percentage completion) are the most common ICDS IV adjustment.
   - **ICDS IX (borrowing costs):** ICDS IX requires capitalization of borrowing cost on qualifying assets on a formula basis (including specific and general borrowings) that is stricter/more mechanical than AS 16 / Ind AS 23 in places (e.g., no "cessation during extended interruption" concept, specific formula for general borrowings). If books expense some borrowing cost that ICDS IX would require to be capitalized (or vice versa), that's an adjustment — check the borrowing cost/interest expense note against the capital-WIP schedule.
   - **ICDS X (provisions/contingencies):** ICDS X has a stricter recognition threshold for provisions than Ind AS 37/AS 29 in some respects (e.g., disallows discounting to present value, and has specific rules on "reasonable certainty" for reimbursements). A common gap: books carry a provision for a probable-but-not-virtually-certain contingency (e.g., a warranty or litigation provision) that ICDS X would still recognise similarly, OR a discounted provision (present-valued) that ICDS X requires to be stated at undiscounted amount — the discounting differential is an adjustment. Also check marked-to-market/unrealised losses on derivative contracts not otherwise allowable, which ICDS X-adjacent rules under section 36(1)(xviii) may restrict.
   - Also scan ICDS VI (unrealised forex gain/loss on monetary items — should be recognised, unlike sometimes-deferred treatment) and ICDS VIII (securities held as stock-in-trade valued scrip-wise, not by category in aggregate, for lower-of-cost-or-NRV) if the client has forex exposure or trades in securities.
4. For each item identified as a genuine ICDS deviation, quantify its P&L effect as `IncreaseProfits` or `DecreaseProfits` under the relevant `Icds` code, and total them in `Form3cdChngMethAccValTotal`. If, after the above checks, no adjustment is found for a given ICDS, still write the "no deviation" disclosure text for 13(e) — but do not create a `Form3cdChngMethAccValChange` entry for it (that array is only for ICDS with an actual quantified adjustment).
5. Tie the total net ICDS effect (`TotalNetProfit`) into the overall computation of total income reconciliation, cross-referencing clause 44AB Part A profit figure to the ITR computation.

**Common junior-staff mistakes:**
- Treating "no ICDS adjustment" as the default without actually checking inventory/revenue/borrowing-cost/provision notes — leads to under-reporting genuine adjustments (ICDS II, IX, X in particular are the most frequently missed).
- Confusing an ICDS adjustment (a *reporting/computation-only* adjustment made in the tax computation, not in the books) with a books restatement — the books are not changed; only the Form 3CD/computation reflects the ICDS-compliant figure.
- Skipping the 13(e) disclosure narrative for ICDS with no deviation — all 10 need a disclosure line, not just the ones with adjustments.
- Reporting a genuine change in accounting policy (e.g., depreciation method change) under ICDS adjustment (13(d)/(f)) instead of as a policy change elsewhere, or vice versa — a change in method of accounting (cash↔mercantile) is 13(b)/(c); an ICDS-vs-books valuation gap under a *consistent* method is 13(d)/(e)/(f). Keep these separate.

---

## Clause 14 — Valuation of Closing Stock and Section 145A Compliance

**Statutory basis:** Section 145A (inclusive method of valuation — stock must include the amount of any tax, duty, cess, or fee (e.g., GST, customs duty) actually paid or incurred to bring the goods to the location and condition as on the valuation date, unless it is anyway credited/debited through a corresponding adjustment such that there is no net profit impact — commonly implemented via "exclusive method in books + notional adjustment in computation" or "inclusive method in books directly"). Clause 14(a)/(b) of Form 3CD.

**Schema mapping:**
- 14(a) — method of valuation → `MethodValCS.ChangeType` (enum: `1` = At Cost, `2` = At Market Rate, `3` = Lower of Cost or Market Rate) plus `DeviationDesc[]` for narrative description of the method actually followed (e.g., "FIFO, cost or NRV whichever is lower, item-wise").
- 14(b) — deviation from s.145A and its effect → `Form3cdChngMethAccVal.Form3cdChngMethAccValPK[]` (same structure as clause 13, differentiated by) `AccType = DEVIATION_SEC145A`, `Particulars` (nature of the deviation), `IncreaseProfits`, `DecreaseProfits`.

**Source documents:** Financial statement "Significant Accounting Policies" — inventory valuation note; trial balance closing stock figure; GST returns (GSTR-3B/GSTR-9, specifically input tax credit claimed on closing stock items) and purchase invoices (to identify GST/duty component not credited to P&L or already excluded from the inventory cost); excise/customs records if applicable (rare post-GST, relevant mainly for a few excisable goods or customs duty on imported stock); stock summary/inventory valuation report from the accounting software.

**Extraction procedure:**
1. Read the inventory valuation policy note in the financial statements — identify the base (cost / market / lower of cost-or-NRV) and the cost formula (FIFO / weighted average / specific identification) used. Map to 14(a) accordingly (`ChangeType` = 1, 2, or 3, with method description in `DeviationDesc`).
2. Determine whether GST input tax credit is being availed on stock purchases (almost always yes for a registered dealer). Under GST, ITC-eligible tax is normally *excluded* from purchase cost (net/exclusive method) in the books — that is standard and compliant practice, because s.145A only requires inclusion of taxes that are **not otherwise recoverable/creditable**; recoverable GST correctly excluded from both purchase cost and closing stock cost is not a s.145A violation as long as it is applied consistently to opening stock, purchases, and closing stock (this is the "no net P&L impact" safe harbour built into s.145A explanation).
3. The actual check: verify that whatever method is used for taxes/duties (inclusive or exclusive), it is applied **consistently to opening stock, purchases, sales AND closing stock** — a mismatch (e.g., non-creditable duty excluded from closing stock valuation but included in purchase cost, or vice versa) is the deviation being tested, not merely "is GST excluded."
4. Specifically check for non-creditable taxes/cess (e.g., unclaimed GST due to blocked credit u/s 17(5), any customs duty component not fully recovered, cess not available as credit) — these must be included in stock valuation at cost. If the client's inventory valuation excludes such non-creditable levies, that is a genuine s.145A deviation.
5. If a deviation is found, compute its effect: the differential tax/duty amount embedded in the closing stock (and correspondingly in opening stock, purchases) that changes the reported profit if valued per s.145A, and populate `IncreaseProfits`/`DecreaseProfits` in `Form3cdChngMethAccVal` (with `AccType = DEVIATION_SEC145A`). Note the offsetting nature — since s.145A requires inclusive treatment of both opening and closing stock, purchases and sales, a well-applied exclusive method consistently followed usually nets to nil or near-nil impact on profit; only inconsistent application creates a real effect.
6. If no deviation, state so and leave the increase/decrease fields blank/zero.

**Common junior-staff mistakes:**
- Assuming any GST-exclusive stock valuation (the near-universal SME practice) is automatically a s.145A violation — it is not, as long as it's applied consistently across opening stock/purchases/sales/closing stock and only creditable GST is excluded.
- Missing blocked/non-creditable GST credit (s.17(5) items — e.g., motor vehicles, certain construction materials, employee-related expenses treated as inventory in unusual cases) that should have been included in cost.
- Not checking opening stock treatment for consistency — a deviation analysis that looks only at closing stock without comparing to how opening stock (=prior year's closing stock) was valued will misstate the profit effect.
- Confusing 14(a)'s "method of valuation" (cost/market/lower of the two, and cost formula) with the inventory *category* (raw material/WIP/finished goods can each have different bases) — describe each category's basis in `DeviationDesc` if they differ.

---

## Clause 15 — Conversion of Capital Asset (Land/Building) into Stock-in-Trade

**Statutory basis:** Section 45(2) — where a capital asset is converted into (or treated as) stock-in-trade, capital gains arise in the year of *conversion* but are chargeable to tax only in the year the converted asset is actually *sold*; fair market value (FMV) of the asset on the date of conversion is deemed to be the full value of consideration for computing the capital gain. Clause 15 of Form 3CD is limited to land or building (or rights therein) so converted.

**Schema mapping:** `Form3cdCapAsstSit[]` — one entry per asset converted: `DescCapAsst` (description of the capital asset), `DateOfAcq` (original date of acquisition of the capital asset), `CostOfAcq` (original cost of acquisition), `AmtConvSit` (amount — i.e., FMV — at which the asset was converted into stock-in-trade). All four fields are mandatory when an entry exists.

**Scope note:** This clause covers land/building (or any right therein) only — conversion of other capital assets (e.g., machinery, shares) into stock-in-trade is not reportable under clause 15 (though it may still have s.45(2) tax consequences reportable elsewhere in the computation, just not in this specific Form 3CD clause).

**Source documents:** Fixed asset register / capital asset schedule (for the asset's original classification as "capital asset" e.g. investment property, freehold land held as fixed asset); board minutes or partner resolution authorising the conversion/re-purposing of the asset for a real-estate development or trading business; valuation report (registered valuer's FMV certificate as on the conversion date); capital gains computation working papers in the ITR; opening/closing inventory schedule (does the converted asset now appear as opening stock-in-trade of a project?); title deed showing original acquisition cost and date.

**Extraction procedure:**
1. This is a rare event — first confirm applicability by checking the fixed asset register/investment schedule for any land or building that was reclassified out of "Fixed Assets"/"Investment Property"/"Capital Assets" into "Inventory"/"Stock-in-Trade"/"Work-in-Progress — real estate" during the year. A reclassification journal entry in the trial balance (debit inventory, credit fixed assets) is the tell-tale sign.
2. Also check for a land/building that a firm/company always intended as a fixed asset but has now started developing/selling in parcels (common with real estate/construction entities holding legacy land banks) — this is a classic s.45(2) trigger even without a formal board resolution.
3. Once identified, pull: (a) `DescCapAsst` — full description (survey number, address, plot size) sufficient to identify the specific land/building; (b) `DateOfAcq` — from the original purchase deed/fixed asset register; (c) `CostOfAcq` — original cost of acquisition (plus capitalized improvement costs, if any, as per the capital gains cost-of-acquisition rules); (d) `AmtConvSit` — FMV as on the date of conversion, which should be supported by a registered valuer's report or, at minimum, a documented basis (e.g., stamp duty ready-reckoner rate on the conversion date, or a comparable sales-based valuation).
4. Verify the capital gains computation in the ITR reflects this conversion — capital gains (`AmtConvSit` − indexed `CostOfAcq`) should be computed for the year of conversion but the tax liability deferred to the year of actual sale of the resulting stock (per s.45(2)); flag if the computation team hasn't captured this deferred treatment.
5. If the FMV as on the date of conversion is not independently supported by a valuation report, flag it `[MISSING — CONFIRM WITH CLIENT]` rather than using book value or stamp-duty value as a substitute without confirmation — FMV determination is a factual/valuation matter, not something to infer.

**Common junior-staff mistakes:**
- Missing the conversion entirely because it's buried in a routine-looking reclassification journal entry rather than flagged by the client.
- Reporting the transaction only in the year of actual sale (when cash/profit is realized) instead of in the year of conversion, which is when clause 15 disclosure and the s.45(2) capital gain computation (though not the tax payment) are triggered.
- Using book value (historical cost) instead of FMV on the conversion date for `AmtConvSit`.
- Applying clause 15 to non-land/building capital assets (e.g., machinery converted to trading stock) — that's outside this clause's scope even though s.45(2) may still apply for the substantive tax computation.

---

## Clause 16 — Amounts Not Credited to the Profit and Loss Account

**Statutory basis:** No single charging section; clause 16 is a disclosure sweep across five categories: (a) items covered by section 28 (profits and gains of business/profession, including specific inclusions like compensation on termination/modification of business contracts/agencies under s.28(ii)-(va)) not routed through the P&L; (b) proforma credits, drawbacks, or refunds of customs/excise duty or sales tax/VAT/GST, to the extent admitted as due by the concerned authority; (c) escalation claims accepted during the year; (d) any other item of income; (e) capital receipts.

**Schema mapping:**
- General bucket → `Form3cdAmtNotCredit[]`, each entry with `Form3cdAmtNotCreditPk`: `TableType` (enum `ITEMS_SEC28` | `PRFRMA_CRDTS` | `ESCL_CLMS_PY` | `ANY_OTH_INCM` | `CAP_RECEIPT`), `TypeOfAmt` (the amount, integer), `Description` (nature of the item, max 100 chars). One entry per item, tagged to the applicable category.
- Sub-detail for category (b) specifically → `Form3cdDrawbackRefundetc[]`: `Description` (enum `01` Proforma credits, `02` Drawbacks, `03` Refunds of Duty of Customs, `04` Refunds of Duty of Excise, `05` Refunds of Service Tax, `06` Refunds of Sales Tax, `07` Refunds of Value Added Tax, `08` Refund of Goods & Services Tax, `09` Others), `DescriptionOthers` (if `09`), `Amount`.

**Source documents:** Bank statements for the full year (look for credits not traced to any P&L income head); "Other Income"/"Other Comprehensive Income" schedule in the financial statements; GST portal refund-order status (RFD-06 orders) and customs/excise refund/drawback sanction orders; correspondence/orders from customers on price-escalation claims (especially for contractors/EPC/construction clients); any settlement, arbitration award, or compensation received for termination of an agency/distributorship/business contract; capital receipts ledger (e.g., government subsidy for capital purposes, insurance claim for a capital asset) that were credited direct to a reserve/capital account rather than the P&L; balance sheet "Other Advances"/"Claims Receivable" accounts that moved during the year.

**Extraction procedure:**
1. Obtain the full-year bank statement(s) and reconcile every credit entry above a reasonable materiality threshold against the P&L. For any credit not traceable to a P&L income line, trace it instead to a balance sheet account (e.g., "Advance received," "Capital Reserve," "Claims Receivable written back") — determine its nature.
2. For each such untraced credit, classify: is it a s.28 item (e.g., compensation for termination of an agency, non-compete fee received in the course of business, or other business income specifically brought within s.28)? → `ITEMS_SEC28`. Is it a customs/excise/GST refund, drawback, or proforma credit admitted as due by the authority (check the actual sanction/refund order date and amount — "admitted as due" typically means the authority has approved/sanctioned it, even if not yet received in cash) → `PRFRMA_CRDTS`, cross-populate `Form3cdDrawbackRefundetc` with the specific duty type. Is it a price-escalation claim under a contract that the counterparty formally accepted during the year (common for construction/EPC/works-contract clients) → `ESCL_CLMS_PY`. Any other income item not otherwise categorized → `ANY_OTH_INCM`. A receipt that is capital in nature (not chargeable as revenue, e.g., capital subsidy, sale proceeds credited directly to a capital reserve without passing through P&L) → `CAP_RECEIPT`.
3. Cross-check the GST portal / GSTN refund status and any customs/excise authority correspondence for refunds *sanctioned* during the year but not yet credited to the P&L (accrual is triggered by admission of the claim as due by the authority, not by actual receipt) — this is the most commonly missed category because such refunds often sit in a receivable account and never hit the P&L until cash is received (which may itself be a compliance gap that clause 16 exists to surface).
4. For escalation claims, check contractor/EPC client correspondence — an escalation claim merely raised/invoiced by the assessee but not yet accepted by the counterparty is NOT reportable; only claims *accepted* during the year qualify.
5. For every item found, record the `Description`/nature and the `TypeOfAmt`/`Amount`. If an amount is referenced in correspondence but the exact figure isn't in the bank statement or ledger (e.g., a refund order sanctioned but amount unclear from available documents), mark `[MISSING — CONFIRM WITH CLIENT]` rather than estimating from the claim amount.
6. If, after this review, no untraced credits or admitted claims are found, `Form3cdAmtNotCredit` and `Form3cdDrawbackRefundetc` remain empty — do not force placeholder entries.

**Common junior-staff mistakes:**
- Only scanning the P&L "Other Income" note and missing items that never reached the P&L at all (the entire point of clause 16) — always start from bank statements and balance sheet movements, not the P&L.
- Treating a GST refund merely *claimed/filed* (RFD-01 filed) as reportable — only refunds *admitted as due* (i.e., sanctioned by the authority, RFD-06/refund order issued) qualify.
- Missing capital receipts credited directly to reserves (e.g., a capital subsidy taken straight to a "Capital Reserve" account) because the review only checks revenue-account movements.
- Reporting an escalation claim merely invoiced/raised by the assessee, without confirmation of counterparty acceptance during the year.
- Double-counting an item that is actually already reflected in the P&L under a differently-labelled income head — verify true non-inclusion, not just that the account name doesn't match expectations.

---

## Clause 17 — Land/Building Transferred Below Stamp Duty Value (Sections 43CA / 50C)

**Statutory basis:** Section 50C (capital asset — land or building or both, held as investment/fixed asset) and section 43CA (stock-in-trade — land or building or both held as inventory, e.g., by real estate developers). Both provide that where the consideration received/accrued on transfer is less than the value adopted or assessed (or assessable) by a stamp valuation authority, the stamp duty value is deemed to be the full value of consideration for computing income — subject to the tolerance band (currently 10% variance safe harbour between actual consideration and stamp duty value; if within 10%, no addition) and, where applicable, the additional condition regarding sale agreement date vs. registration date (stamp value on agreement date if part consideration was received via banking channel on/before the agreement). Clause 17 of Form 3CD.

**Schema mapping:** `Form3cdLandBuildProperty[]` — one entry per property transferred: `Details` (property description), `AddressDetail` (AddrDetail1/2, City, StateCode, CountryCode, PinCode), `ConsiderAmt` (consideration received/accrued as per the sale deed/books), `Valueadoptedassessed` (`Y`/`N` — whether stamp duty value was in fact adopted/assessed/assessable, i.e., is there a discrepancy to report), `AssessedAmt` (the value adopted/assessed/assessable by the stamp valuation authority). All fields mandatory when an entry exists.

**Source documents:** Sale deed / conveyance deed (registered, with the sub-registrar's stamp duty valuation endorsed on it, or the challan for stamp duty paid); books of account (sale consideration recorded, and for stock-in-trade, the item removed from inventory); fixed asset register (for capital asset disposals, to identify land/building sold during the year and its sale proceeds); prior sale agreement (if any, to check the agreement-date vs. registration-date stamp value rule); state stamp duty ready-reckoner / circle rate notification (if the deed itself doesn't state the stamp value, cross-check against the applicable circle rate for that locality as of the transfer date).

**Extraction procedure:**
1. Identify every transfer of land or building (or rights therein) during the year — both (a) capital assets (check fixed asset register/investment schedule disposals) for s.50C, and (b) stock-in-trade (check inventory/completed-project sales register) for s.43CA, e.g. real estate developer's flat/unit sales.
2. For each transfer, pull the actual sale consideration recorded in the books/sale deed (`ConsiderAmt`) and the stamp duty value adopted/assessed by the registering authority at the time of registration (usually stated on the deed itself, or obtainable from the sub-registrar's office/e-stamping portal) (`AssessedAmt`).
3. Compare: if `AssessedAmt` > `ConsiderAmt`, check the tolerance band — if the excess of `AssessedAmt` over `ConsiderAmt` is within 10% of `ConsiderAmt` (current statutory safe harbour under both s.43CA and s.50C), there is technically still a clause 17 disclosure event only if `AssessedAmt` ≠ `ConsiderAmt` at all (form-wise the clause calls for disclosure whenever stamp value differs and was adopted/assessable), but the tax addition itself would be nil within the tolerance band — note this distinction and still populate the entry with the actual figures; flag the tolerance-band conclusion `[JUDGMENT CALL — CA TO CONFIRM]` since it affects the computation (not the disclosure).
4. If there was a registered agreement to sell prior to the registered conveyance, and part of the consideration was received via banking channel on or before the date of that agreement, use the stamp duty value as on the *agreement* date instead of the registration date — verify banking-channel receipt evidence (cheque/NEFT/RTGS, not cash) before applying this exception; if unverified, flag `[JUDGMENT CALL — CA TO CONFIRM]`.
5. Populate `Valueadoptedassessed = Y` if the stamp authority's value was in fact adopted/assessed/is assessable and differs from consideration (i.e., there is something to report); `N` only if there genuinely was no stamp valuation event to report for that property (in which case there's usually no reason to create the entry at all — this flag is primarily for internal completeness, not a meaningful "no" case in a populated entry).
6. Fill `AddressDetail` from the sale deed's schedule-of-property description.
7. If the stamp duty value is not stated on the deed and not otherwise available at the time of preparing the workpaper, mark `AssessedAmt` `[MISSING — CONFIRM WITH CLIENT]` rather than substituting an estimated circle-rate figure without verification — the circle rate can be used only as a cross-check pointer for follow-up, not as the reported figure itself.

**Common junior-staff mistakes:**
- Checking only capital-asset (fixed asset) disposals and missing stock-in-trade sales (43CA) — real estate developers and builders very commonly trigger this clause on flat/unit sales, not just on sale of a factory building.
- Applying the 10% tolerance band incorrectly — it is a safe harbour against the *addition to income*, but the clause disclosure itself (reporting `ConsiderAmt` vs `AssessedAmt`) is still generally expected whenever the two figures differ, so don't suppress the entry just because the variance falls inside the safe harbour.
- Missing the agreement-date exception (s.43CA/50C proviso) when part consideration was received in advance via banking channels before a registered agreement — leads to using the wrong (higher, later) stamp value.
- Forgetting rights in land/building (e.g., transfer of leasehold rights, TDR/FSI, development rights) which also fall within the scope of "land or building or any right therein."
- Using an internet/estimated circle-rate value instead of the actual value stated on the registered deed/challan when the two might differ (always prefer the value actually adopted by the registering/stamp authority for that specific transaction).

---

### Cross-clause consistency checks (apply after drafting 9–17)
- Clause 9(a) partner list should tie to clause 8 (status) and to the firm's PAN/deed on file — status must be Firm/LLP/AOP for clause 9 to apply at all.
- Clause 10's nature-of-business classification should be consistent with the presumptive section claimed in clause 12 (e.g., a 44AE claim implies a transport business, which should also surface in clause 10's sector `11` classification).
- Clause 11's books-maintained list (11b) should be internally consistent with what's described as the basis of accounting in clause 13(a) (e.g., if cash book and bank book only are maintained, method of accounting is more likely cash basis — investigate any mismatch).
- Clause 13(e)/(f) ICDS II disclosure should tie to clause 14's stock valuation method — the same closing stock figure and valuation basis should be reflected consistently across both clauses.
- Clause 15 (conversion of capital asset to stock) and clause 17 (transfer of land/building below stamp value) both draw on the same fixed-asset-register review — do this review once and populate both clauses from the same pass to avoid missing a transaction in one while catching it in the other.
- Clause 16 capital receipts (e) should be cross-checked against clause 15's conversion FMV and any capital gains computation, to ensure the same receipt isn't reported as both a clause 16 capital receipt and separately mis-stated elsewhere.
