# Form 3CD — Clauses 27 to 35 (AY 2026-27 / FY 2025-26)

Domain reference for drafting Form 3CD workpapers. Scope: clauses 27, 28, 29, 29A, 29B, 30, 30A, 30B, 30C, 31, 32, 33, 34, 35.

**General rules that apply to every clause below:**
1. Never invent a rupee figure, name, PAN, date, or count that is not traceable to a source document. If a data point required by the schema is absent from what the client has provided, write `[MISSING — CONFIRM WITH CLIENT]` in that field/note and move on — do not estimate, round, or infer it.
2. Where the *data exists* but its tax characterisation requires judgment (e.g., is this a "loan" for 269SS or a trade advance outside its scope; is a share allotment covered by 56(2)(viib)), make the best-supported call from the evidence and tag it `[JUDGMENT CALL — CA TO CONFIRM]`. Do not silently pick an interpretation.
3. Field/group names below (`Form3cdXxx`) are the exact JSON keys in `references/schema/schema_3CB.json` / `3CB_structure.txt` — use them when mapping extracted data to the e-return schema. Enum values quoted are taken from the schema; if the live e-filing utility has diverged from this bundled schema at the time of the engagement, trust the utility and note the discrepancy.
4. **Schema vintage caveat**: several enums in the bundled schema are capped one year short of AY 2026-27 (e.g. `Form3cdIncExpPriorPlAcc.PriorYear` only goes up to `2024-25`). Where the correct value for FY 2025-26 work is not in an enum, do not force-fit it — flag `[SCHEMA GAP — VERIFY AGAINST LIVE UTILITY]` for the developer/CA rather than silently substituting the nearest enum value.

---

## Clause 27 — CENVAT/GST credit and prior period items

### 27(a) — CENVAT/GST input tax credit

**Statute**: Rule 6G / Form 3CD clause 27(a) — amount of Central Excise duty/service tax/GST input credit availed or utilised during the year and its treatment in the P&L account, plus treatment of any outstanding CENVAT/input credit balance in the accounts.

**Schema**: `Form3cdPl` (array — one row per tax head, e.g. GST/erstwhile Central Excise/Service Tax/VAT, since old and new indirect tax regimes can coexist in transition years): `OpeningBalAmount` + `OpeningBalTreatmentPl`, `CenvatAvailAmount` + `CenvatAvailTreatmentPl`, `CenvatUtilizedAmount` + `CenvatUtilizedTreatmentPl`, `BalanceAmount` + `BalanceTreatmentPl`. A legacy sibling group `Form3cdModvat` (`Amount`, `TreatmentOsModVat`) also exists in the schema — MODVAT is the pre-2000 name for CENVAT; for an FY 2025-26 audit this group is almost certainly unused. Prefer `Form3cdPl`; only populate `Form3cdModvat` if the live utility explicitly asks for it.

**Source documents**: GSTR-3B (month-wise ITC availed/utilised/reversed), GSTR-2B (ITC as reflected/eligible), annual return GSTR-9 (annual reconciliation of ITC), the GST ledger/electronic credit ledger, and the client's trial balance accounts for "GST Input Credit Recoverable" / "GST Payable" / "CENVAT credit receivable" (if any residual pre-GST balance survives).

**Procedure**:
1. Determine the accounting method used: **net method** (ITC never touches P&L — booked directly to a balance-sheet "GST recoverable" asset account, net of GST payable) vs **gross method** (rare; purchases/expenses booked GST-inclusive, with a corresponding P&L credit for ITC claimed). Most modern Tally/Zoho/QuickBooks-based SME books use the net method — in that case the correct clause 27(a) answer is that CENVAT/GST credit availed and utilised has **no P&L effect**; only report opening balance, credit availed, credit utilised, and closing balance as balance-sheet movements, with "Treatment in P&L" = "Not routed through P&L / credited to GST Recoverable account."
2. Separately identify any ITC **reversed** during the year (e.g., under Rule 42/43 for exempt supplies, blocked credit under Sec 17(5) wrongly claimed, credit note-driven reversals, or ITC reversed and expensed off because a vendor defaulted on GSTR-1/2B matching or payment beyond 180 days under Sec 16(2) second proviso). If a reversal was **debited to the P&L as an expense** (common when the client treats time-barred or ineligible ITC as a write-off), this is a distinct, more important disclosure than mechanical opening/closing balances — call it out explicitly with the ledger account and amount.
3. Reconcile the closing "GST Recoverable"/"Input Tax Credit" balance per books against the electronic credit ledger balance per the GST portal (or GSTR-9 Table 6/7/8) as of 31 March. A material unreconciled difference is a red flag — note it, do not silently accept the books figure.
4. If the entity still carries a pre-GST (pre-July 2017) CENVAT/VAT credit balance sitting idle in the books (common for legacy litigation), report the outstanding balance and its treatment separately.

**Common mistakes**: treating GST paid on purchases as a P&L expense when it should be capitalised as recoverable ITC (inflates expenses, needs adjustment); confusing IGST/CGST/SGST components when reconciling to GSTR-9; missing ITC reversed under Rule 86B or blocked credits under Sec 17(5) that were wrongly availed and later expensed.

**Fabrication rule**: the availed/utilised/reversed figures MUST tie to GSTR-3B/2B/9 or the GST ledger — never estimate from the P&L alone. If GST returns are not provided, flag `[MISSING — CONFIRM WITH CLIENT: GSTR-3B/2B/9 not provided]` rather than deriving ITC from bank/purchase data.

### 27(b) — Prior period income/expenditure

**Statute**: Form 3CD clause 27(b) — particulars of income or expenditure of a prior period credited or debited to the P&L account of the current year.

**Schema**: `Form3cdIncExpPriorPlAcc` (array): `Type` (pattern `Prior period Income|Prior period Expenditure|Expenditure Deb[ited]`), `Particulars`, `Amount`, `PriorYear` (enum of AYs, currently capped at `2024-25` in the bundled schema — see schema vintage caveat above; if the item relates to FY 2024-25/AY 2025-26, that value should be present, but if it relates to something even later that isn't in the enum, flag `[SCHEMA GAP]`).

**Source documents**: P&L account and its schedules/notes — search specifically for ledger heads or line-item labels containing "prior period," "earlier year," "PY adjustment," or notes-to-accounts disclosures under AS 5 / Ind AS 8 (prior period items / errors).

**Procedure**:
1. Scan the trial balance and P&L schedules for any account literally named "Prior Period Income/Expense," and also scan for out-of-place large one-off entries (e.g., a sudden write-back of an old provision, a late-received credit note against last year's purchase, an omitted invoice from FY 2024-25 booked in FY 2025-26) that are prior-period in substance even if not labelled as such.
2. For each item found, record nature, amount, and the year it actually pertains to.
3. Note that this is a *disclosure* clause, not an adjustment clause — it does not itself change the tax computation, but the tax computation should independently verify that expenses of an earlier year are not being claimed for the first time this year without justification (year of accrual/crystallisation matters under the mercantile system), and correspondingly that prior-period income is not being kept out of an earlier year's return.

**Common mistakes**: missing prior-period items buried inside a general "other income" or "miscellaneous expenses" head instead of a dedicated ledger; forgetting that a reversal of an earlier year's provision (write-back) is a prior-period *credit*, not current-year income, for this disclosure.

**Fabrication rule**: only report items that are actually visible in the P&L/ledger as prior-period in nature — do not reclassify current-year items as prior period on a hunch; if a large one-off entry looks prior-period but the client hasn't confirmed its origin, flag `[JUDGMENT CALL — CA TO CONFIRM: possible prior-period item, origin unverified]`.

---

## Clause 28 — Shares received without/inadequate consideration (Sec 56(2)(viia))

**IMPORTANT — clause omitted from Form 3CD w.e.f. AY 2025-26 onwards.** CBDT Notification No. 23/2025 dated 28 March 2025 (Income-tax (Eighth Amendment) Rules, 2025), effective for tax audit reports furnished/signed on or after 1 April 2025, **deleted clauses 28 and 29 from Form 3CD entirely**. For an FY 2025-26 (AY 2026-27) tax audit, clause 28 does not exist in the form — there is nothing to report and nothing to leave blank; it is simply not asked. Do not spend time investigating this.

**Historical context (for understanding old workpapers only)**: Sec 56(2)(viia) taxed a firm or a closely-held company (company in which the public are *not* substantially interested) that received shares of another closely-held company without consideration or for inadequate consideration, in the hands of the *recipient* firm/company as "income from other sources." This provision was itself omitted by the Finance Act, 2017 and subsumed into the broader Sec 56(2)(x) (any person, any property) effective AY 2018-19 — so even before the form-level deletion, clause 28 had been reporting a near-dead-letter provision for eight assessment years (transactions from AY 2018-19 onward fall under clause 29B / Sec 56(2)(x) instead, described below).

**Schema**: the field group `Form3cdSec562viia` (array: `NameOfPerson`, `PANOfPerson`, `AadhaarCardNo`, `NameOfCompany`, `CINissuedByMCA`, `NoOfShares`, `AmountConsideration`, `FairMarketShares`) and flag `Form3cdFlags.Form3cdSec562viiaFlag` (`Y|N|X`) still exist in the bundled JSON schema — likely retained for backward compatibility with older AY filings bundled into the same schema file. **Do not populate these for an AY 2026-27 report**; if the runtime tool must set the flag for schema-validity reasons, use `X` (not applicable) and confirm against the live e-filing utility, since the correct behaviour (omit the field vs. set X) depends on how ITD's current utility actually handles it.

---

## Clause 29 — Share premium exceeding FMV / angel tax (Sec 56(2)(viib))

**IMPORTANT — clause omitted from Form 3CD w.e.f. AY 2025-26 onwards**, by the same CBDT Notification No. 23/2025 dated 28 March 2025 referenced above. Separately and more fundamentally, the underlying substantive provision — Sec 56(2)(viib), the "angel tax" — was itself abolished by the Finance (No. 2) Act, 2024, with the amendment applying from **AY 2025-26 onwards**: consideration received for issue of shares by a closely-held company, in excess of fair market value, is **no longer chargeable to tax at all**, regardless of whether the investor is resident or non-resident. Both the form question and the underlying tax liability are gone for FY 2025-26. Treat as a non-issue — do not investigate share premium received during the year for angel-tax purposes.

**Historical context (for understanding old workpapers, or if a query relates to FY 2024-25 or earlier)**:
- Sec 56(2)(viib) taxed a closely-held company on share consideration received from a resident investor in excess of FMV, as income from other sources, subject to valuation under Rule 11UA.
- The Finance Act 2023 had extended this provision to consideration received from *non-resident* investors as well (previously only resident investors triggered it) — this extension operated for FY 2023-24 and FY 2024-25 before the whole provision was abolished from AY 2025-26.
- A DPIIT-registered "eligible startup" satisfying prescribed conditions (turnover < Rs 100 crore in any prior year, not older than 10 years, aggregate paid-up capital + premium post-issue ≤ Rs 25 crore excluding specified exempt investor classes) was exempt from Sec 56(2)(viib) via CBDT notification even before the general abolition.

**Schema**: `Form3cdSec562viib` (array: `NameOfPerson`, `PANOfPerson`, `AadhaarCardNo`, `NoOfShares`, `AmountConsideration`, `FairMarketShares`) and flag `Form3cdFlags.Form3cdSec562viibFlag` (`Y|N|X`) similarly remain in the bundled schema for legacy compatibility. **Do not populate for AY 2026-27**; use `X` only if the live utility structurally requires a value, and verify against the current utility rather than assuming.

---

## Clause 29A — Forfeited advance on transfer of capital asset (Sec 56(2)(ix))

**Statute**: Sec 56(2)(ix) — any sum of money received as an advance or otherwise in the course of negotiations for transfer of a capital asset, which is forfeited because the negotiations do not result in transfer, is chargeable as "income from other sources" in the hands of the recipient, in the year of forfeiture. (This is distinct from the pre-2014 position where such forfeitures reduced the cost of acquisition under Sec 51 — post Sec 56(2)(ix), forfeiture is taxed as income at the time of forfeiture *and* Sec 51 no longer allows a further cost reduction for amounts already taxed under 56(2)(ix).)

**Schema**: `Form3cdSec29IncOtherSourcesAb` (array: `NatureOfIncome`, `NatureAmount`), gated by flag `Form3cdFlags.IncomeCluaseixofsubsection2` (`Y|N`). Note this clause remains fully live and unaffected by the CBDT Notification 23/2025 changes (only clauses 28/29 were deleted; 29A and 29B keep their existing sub-clause letters).

**Source documents**: journal entries/other income ledger for "advance forfeited," "earnest money forfeited," "token money forfeited"; board resolutions or correspondence relating to aborted sale of property, plant, land, or other capital assets; the balance sheet (advances received against sale of assets, or "capital advance" liability accounts) to see if any such balance was written back to income during the year.

**Procedure**:
1. Ask specifically whether the assessee (a) attempted to sell any capital asset (land, building, plant, investments, goodwill, etc.) during the year or in a prior year, (b) received an advance/token/earnest money for that intended sale, and (c) the deal fell through with the advance retained.
2. If yes, confirm the amount forfeited and the year of forfeiture (income arises in the year the amount is *forfeited*, not the year it was originally received).
3. Confirm it has been credited to the P&L (as other income) or income has been separately offered in the computation of income even if not routed through P&L.

**Common mistakes**: confusing a forfeited advance on a *capital asset* (taxable under 56(2)(ix)) with a forfeited advance on *stock-in-trade*/trading goods (which is ordinary business income, not this clause); missing forfeitures embedded in "miscellaneous income" without a descriptive ledger name.

**Fabrication rule**: this clause is a genuine NIL for the overwhelming majority of SME clients in any given year (aborted capital-asset sales with retained advances are uncommon events) — default to NIL unless a specific forfeiture is evidenced in the books/other income schedule. Do not invent a scenario. Flag `[MISSING — CONFIRM WITH CLIENT]` only if there's a specific reason to suspect an unexplained credit (e.g., an unusually large "other income" entry with no clear description).

---

## Clause 29B — Receipt of money/property without or for inadequate consideration (Sec 56(2)(x))

**Statute**: Sec 56(2)(x) — where **any person** (not just firms/companies — individuals, HUFs, everyone) receives, without consideration or for inadequate consideration, (a) any sum of money exceeding Rs 50,000 in aggregate during the year, (b) any immovable property, or (c) any specified movable property (shares/securities, jewellery, archaeological collections, drawings, paintings, sculptures, any work of art, bullion, virtual digital assets), the whole or the shortfall is taxed as income from other sources, subject to specific thresholds per category:
- **Money**: aggregate sum received without consideration > Rs 50,000 → entire sum taxable.
- **Immovable property without consideration**: stamp duty value (SDV) > Rs 50,000 → entire SDV taxable.
- **Immovable property for inadequate consideration**: taxable only if (SDV − consideration) exceeds the *higher of* Rs 50,000 **or** 10% of the consideration (this 10%-or-Rs-50,000 safe harbour is frequently missed — do not apply a flat Rs 50,000 threshold to immovable property purchases).
- **Specified movable property without consideration**: aggregate FMV > Rs 50,000 → entire FMV taxable.
- **Specified movable property for inadequate consideration**: taxable if (FMV − consideration) exceeds Rs 50,000.
- Exclusions: property received from relatives (as defined), on marriage, under a will/inheritance, from a local authority/registered trust/fund under Sec 10(23C) or 12A/12AA/12AB, in contemplation of death, in certain business reorganisations, etc.

**Schema**: `Form3cdSec29IncOtherSourcesBb` (array: `NatureOfIncome`, `NatureAmount`), gated by flag `Form3cdFlags.IncomeCluasexofsubsection2` (`Y|N`).

**Source documents**: fixed asset register and capital account movements for any asset acquired at below-market value or gifted-in; share application/allotment records (bonus/rights issues at a discount to a closely-held company can occasionally trigger this for the allottee, though normal proportionate bonus/rights issues are excluded); gift deeds; capital account credits in partnership/proprietorship books for assets introduced by partners/proprietor without full consideration; loan waiver or debt-forgiveness entries (generally taxed elsewhere under Sec 41(1)/28(iv), not this clause, but worth cross-checking); related-party transaction registers for any asset transfer between group entities at less than FMV.

**Procedure**:
1. Scan for any gift, donation-in-kind, or asset received free/cheap during the year — check "capital reserve," "gifts received," "assets received," and unusual credits to reserves or capital accounts.
2. For any property (immovable or specified movable) purchased below its SDV/FMV, obtain or estimate the SDV/FMV and apply the correct threshold test above (note the different mechanics for immovable vs. movable property, and the 10%-or-Rs-50,000 rule for immovable property).
3. Check for the relative/exclusion carve-outs before concluding an item is taxable — a gift from a "relative" as statutorily defined (spouse, siblings of self/spouse, siblings of parents, lineal ascendant/descendant of self or spouse, spouse of any of the aforementioned) is excluded regardless of amount.
4. Confirm whether the amount identified has actually been offered to tax in the computation of income (this clause can surface items the client has not separately reported).

**Common mistakes**: applying the flat Rs 50,000 test to immovable property instead of the 10%-or-Rs-50,000 safe harbour; missing shares of a closely-held company received by an individual/firm/company for less than FMV under Rule 11UA (a frequent private-company related-party area); treating a genuine arm's-length discount/bargain purchase as taxable without checking whether real consideration was in fact adequate; overlooking that virtual digital assets (crypto/NFTs) received without consideration also fall within "property" for this clause.

**Fabrication rule**: this clause requires an actual identified receipt in the books or supporting documents — do not assume related-party asset transfers were at inadequate consideration without valuation evidence. If a related-party or unusual asset transfer is seen but no valuation (SDV/FMV) is available, flag `[MISSING — CONFIRM WITH CLIENT: valuation/SDV/FMV required to test 56(2)(x)]` rather than guessing whether the threshold was crossed.

---

## Clause 30 — Hundi borrowings (Sec 69D)

**Statute**: Sec 69D — any amount borrowed on a hundi (a traditional negotiable instrument used in indigenous/informal money-lending, mainly in western/northern India), or any amount due thereon (including interest) repaid, otherwise than through an account payee cheque drawn on a bank, is deemed to be the income of the borrower (for borrowings) or of the payer (for repayments not already taxed as the borrower's income in an earlier year) for that previous year.

**Applicability note**: this is essentially obsolete for standard modern SME/corporate accounting — hundi financing is a narrow, geographically and historically specific informal-credit instrument, not something that appears in normal GST-registered business books, bank-financed working capital, or NBFC/bank loan structures. **Default to NIL for virtually all clients** and do not spend audit time searching for hundi transactions unless the client operates in a traditional trading community/sector where hundi financing is still known to be used (e.g., certain commodity/bullion/grain trade circles), or there is an explicit ledger head or loan confirmation referencing "hundi."

**Schema**: `Form3cdSec69d` (array: `NameOfPerson`, `PANOfPerson`, `AadhaarCardNo`, `AddressDetail` (address block with state/country/pin codes), `AmountBarrowed`, `DateOfBarrow`, `AmountDueIntrst`, `AmountRepaid`, `DateOfRepayment`), gated by flag `Form3cdFlags.Section69D` (`Y|N`).

**Source documents**: unsecured loan ledgers and loan confirmation letters — a quick scan of lender names/instrument descriptions for "hundi" is sufficient; if none found, close this out as NIL.

**Fabrication rule**: answer `N` unless a hundi transaction is explicitly evidenced. Do not ask the client leading questions that waste time on a near-extinct instrument — a single confirmatory question ("any hundi borrowings this year?") to the client/finance team is enough diligence.

---

## Clause 30A — Primary transfer pricing adjustment (Sec 92CE(1))

**[APPLICABLE ONLY IF CLIENT HAS RELATED-PARTY CROSS-BORDER/SPECIFIED DOMESTIC TRANSACTIONS EXCEEDING TP THRESHOLDS — CONFIRM WITH CA]**. This clause only arises where a primary transfer pricing adjustment has been made to the transfer price of an international transaction or specified domestic transaction with an associated enterprise (AE), and the primary adjustment exceeds Rs 1 crore *and* the transaction relates to FY 2016-17 onwards (Sec 92CE was inserted w.e.f. AY 2018-19). **Default to NIL for typical domestic SME clients** — a client with no AE transactions, no Form 3CEB filing obligation, and no transfer pricing study has nothing to report here; do not investigate this clause unless the engagement file already shows the client has related-party cross-border dealings or a Form 3CEB requirement.

**Statute**: Sec 92CE(1) — a primary adjustment to transfer price arises where it (i) is made suo motu by the assessee in the return, (ii) is made by the AO and accepted by the assessee, (iii) is determined by an Advance Pricing Agreement (APA) under Sec 92CC, (iv) is made per Safe Harbour Rules under Sec 92CB, or (v) arises from resolution of a Mutual Agreement Procedure (MAP) under Sec 90/90A. If the primary adjustment exceeds Rs 1 crore, "excess money" (the difference between the arm's length price and the actual price, to the extent funds are still with the AE) must be repatriated to India within the prescribed time (generally 90 days from the due date of filing the return, or 90 days from the date of the APA/MAP/AO order, as applicable) — if not repatriated, interest is imputed as additional income at the prescribed rate (SBI one-year MCLR + 3%, for INR-denominated transactions; specified rate for foreign-currency-denominated transactions) on the un-repatriated excess money.

**Schema**: `Form3cdSec92CE` (array): `UnderSec92CE` (enum `01`–`05`, corresponding to the five circumstances (i)–(v) above), `PrimaryAdjAmt`, `ExcessRepatriatedAmt` (`Y|N` — whether the excess money required to be repatriated has actually been repatriated), `ImputedRepatriatedAmt` (`Y|N|D`), `ImputedInterestIncome`, `ExpectedDate` (repatriation due date). Gated by flag `Form3cdFlags.TransferPriceSection92CE` (`Y|N`).

**Source documents**: Form 3CEB (transfer pricing report, if filed), TP study/documentation, APA (if any), any AO/appellate order or MAP resolution making a TP adjustment, AE fund-flow/repatriation evidence (FIRC/bank remittance advices).

**Procedure (only if applicable)**: identify which of the five circumstances triggered the primary adjustment; quantify the adjustment amount and the excess money; confirm from bank/FIRC records whether repatriation actually occurred within the prescribed window; if not repatriated, compute imputed interest per Rule 10CB.

**Fabrication rule**: never mark this clause "Yes" without a specific TP adjustment event (an actual AO order, self-adjustment in the ITR, APA, or MAP resolution) in hand — this is not something to infer from general related-party transactions. For clients without a Form 3CEB filing history, mark `N`/leave the flag at NIL.

---

## Clause 30B — Interest limitation / thin capitalisation (Sec 94B)

**Applicability note**: this clause applies **only** to (a) an Indian company, or a permanent establishment of a foreign company in India, that (b) pays or incurs interest or similar expenditure exceeding **Rs 1 crore** in the year (c) to a non-resident associated enterprise, or to a lender where the debt itself is effectively guaranteed by an AE (implicit/back-to-back AE guarantee). It has no application to proprietorships, partnerships/LLPs, or any domestic-only-funded company. **Flag as NOT APPLICABLE for the typical domestic SME/proprietorship/partnership client** — do not investigate unless the client is a company with cross-border AE debt (e.g., an Indian subsidiary of a foreign parent that has extended an intercompany loan, or debt raised from a third party but guaranteed by the foreign parent).

**Statute**: Sec 94B(1) — where an Indian company/PE of a foreign company incurs interest/similar expenditure exceeding Rs 1 crore towards debt from/guaranteed by an AE, the interest deduction is capped, per Sec 94B(2), at the lower of (a) actual interest expenditure, or (b) 30% of EBITDA. The disallowed excess can be carried forward for set-off against income under "profits and gains of business or profession" to the extent of the 30%-of-EBITDA headroom in the next 8 assessment years. Banking/insurance companies and NBFCs are excluded.

**Schema**: `Form3cdIncurredExpenditure` (array): `NatureIncurredAmt` (interest/similar expenditure amount), `EBITDAAmt`, `Amt30PerEBITDA` (the 94B(2) computed disallowance), `Sec94BAssmntYearBfwd`/`Sec94BAmtBFwd` (brought-forward disallowed interest available from an earlier AY, enum capped at `2025-26`), `Sec94BAssmntYearCfwd`/`Sec94BAmtCFwd` (amount carried forward to a future AY, enum extends to `2026-27` — consistent with FY 2025-26 being the current year). Gated by flag `Form3cdFlags.IncurredExpenditure` (`Y|N`).

**Source documents (only if applicable)**: loan agreements with the foreign AE or AE-guaranteed lenders, interest computation schedules, EBITDA computation (from the audited P&L, adding back interest, depreciation, and amortisation to profit before tax), prior years' Form 3CD/computation of income for brought-forward disallowed interest.

**Fabrication rule**: do not compute an EBITDA/30% cap unless AE-linked interest exceeding Rs 1 crore is actually confirmed — this clause is a NIL/not-applicable default for the vast majority of engagements.

---

## Clause 30C — GAAR / impermissible avoidance arrangement (Sec 96)

**Statute**: Sec 96 defines an "impermissible avoidance arrangement" (IAA) as one whose main purpose is to obtain a tax benefit, and which additionally (a) creates rights/obligations not ordinarily created between parties dealing at arm's length, (b) results in misuse/abuse of the Act's provisions, (c) lacks commercial substance (per Sec 97) in whole or part, or (d) is entered into/carried out in a manner not ordinarily employed for bona fide purposes. Chapter X-A (Sec 95–102, GAAR) empowers the AO to disregard, recharacterise, or deny the tax benefit of such an arrangement, subject to Approving Panel clearance.

**Threshold below which GAAR does not apply**: Rule 10U(1)(a) of the Income-tax Rules excludes an arrangement from GAAR where the aggregate tax benefit to all parties, in the relevant assessment year, does **not exceed Rs 3 crore**. This is assessed year-by-year (per CBDT Circular 7/2017), not cumulatively across years. Rule 10U also carves out certain FII arrangements and grandfathers investments/income arising before 1 April 2017.

**Applicability note**: GAAR is essentially reserved for large, deliberately tax-structured arrangements (aggressive treaty shopping, artificial round-tripping, contrived business reorganisations designed mainly to shift income/reduce tax) — **it is never the correct default answer for a standard SME/professional/trading client**, and should never be marked "Yes" without an explicit, identifiable arrangement and a specific reason articulated by the CA. Flag NIL as the default for essentially all engagements under this skill's typical scope.

**Schema**: `Form3cdImpermissibleSec96` (array): `NatureImpermissible` (pattern `a|b|c|d|e` mapping to the four Sec 96(1) tainted-element tests above, plus `e` for "others"), a field carrying the **amount of tax benefit** for the year (note: this field is internally named `InterestExp94BAmt` in the schema — a naming artifact reused from the Sec 94B group; despite the name, in this group it represents the tax benefit amount for clause 30C, not an interest figure), and `Others` (free text). Gated by flag `Form3cdFlags.ImpermissibleSec96` (`Y|N`).

**Fabrication rule**: mark `N` unless there is a specific, CA-identified arrangement with a quantified tax benefit — never infer GAAR applicability from general aggressive tax planning or generic related-party structuring without an explicit basis.

---

## Clause 31 — Loans, deposits, specified sums (Sec 269SS/269T) and cash receipts/payments (Sec 269ST)

**Critical distinction** (a common area of confusion): Sec 269SS/269T apply narrowly to **loans, deposits, and "specified sums"** (advances relating to transfer of immovable property) — acceptance/repayment above Rs 20,000 otherwise than through prescribed banking channels. Sec 269ST is far broader: it applies to **any receipt of Rs 2,00,000 or more from a person**, in cash or otherwise than by account payee cheque/draft/ECS — including ordinary trade/business receipts, sale proceeds, gifts, or any other transaction, not just loans. A single large cash sale to one customer can trigger 269ST even though it has nothing to do with 269SS/269T. Always test both, separately.

**Schema field groups for clause 31** (each maps to a specific reporting sub-item):

| Sub-item | Schema group | Key fields | Covers |
|---|---|---|---|
| 31(a) | `Form3cdAmtSec269ssDetail` | `LenderName`, `LenderAddress`, `PanNoLender`, `AadhaarCardNo`, `AmtLoanDeposit`, `LoanDepSqrdPyFlag`, `MaxAmtOsAccPy`, `LoanDepChqDrftFlag`, `NatureAmtCdeType`, `LoanDepChqDrftType`, `PleaseSpfy` | Loans/deposits taken/accepted during the year exceeding Rs 20,000 (Sec 269SS) |
| 31(b) | `Form3cdSec269SSDtls` | `ReceiverName`, `ReceiverAddress`, `ReceiverPanNo`, `AadhaarCardNo`, `AmtAccepted`, `OsAccPy`, `NatureAmtCdeBType`, `LoanDepChqDrftType`, `PleaseSpfyB` | "Specified sum" (advance/other sum relating to transfer of immovable property, whether or not the transfer occurs) exceeding Rs 20,000 accepted during the year |
| 31(ba) | `Form3cdSec269ST31ba` | `NameOfPayer`, `AddressOfPayer`, `PANOfPayer`, `NatureOfTransaction`, `ReceiptAmount`, `ReceiptDate` | Cash receipts ≥ Rs 2,00,000 (269ST), received otherwise than by cheque/draft/ECS |
| 31(bb) | `Form3cdSec269ST31bb` | `NameOfPayer`, `AddressOfPayer`, `PANOfPayer`, `ReceiptAmount` | Receipts ≥ Rs 2,00,000 (269ST) received by cheque/draft that is *not* account payee |
| 31(bc) | `Form3cdSec269ST31bc` | `NameOfPayee`, `AddressOfPayee`, `PANOfPayee`, `NatureOfTransaction`, `PaymentAmount`, `PaymentDate` | Cash payments ≥ Rs 2,00,000 (269ST) made otherwise than by cheque/draft/ECS |
| 31(bd) | `Form3cdSec269ST31bd` | `NameOfPayee`, `AddressOfPayee`, `PANOfPayee`, `PaymentAmount` | Payments ≥ Rs 2,00,000 (269ST) made by cheque/draft that is *not* account payee |
| 31(c) | `Form3cdAmtSec269tDetail` | `PayeeName`, `PayeeAddress`, `PayeePanNo`, `AadhaarCardNo`, `AmtRepayment`, `MaxAmtOsAccPy`, `RepaymentChqDraftFlag`, `NatureAmtCdeCType`, `RepaymentChqDraftType`, `PleaseSpfyC` | Repayment of loan/deposit/specified advance exceeding Rs 20,000 (Sec 269T) |
| 31(d)/(e) | `Form3cdSec269TDtls`, `Form3cdSec269TNewDtls` | `DepositorName`, `DepositorAddress`, `DepositorPanNo`, `AadhaarCardNo`, `AmtDeposit` | Further breakdown of repayments received otherwise than by account payee cheque/draft (two parallel groups in the schema — verify against the live utility which of the two the current form uses for "otherwise than by account payee instrument" vs "by non-account-payee cheque/draft") |

**"Nature/mode" code field (`NatureAmtCdeType`/`NatureAmtCdeBType`/`NatureAmtCdeCType`) — read this carefully.** Effective for AY 2025-26 onward (per CBDT Notification No. 23/2025), clause 31 requires a specific code for *how* the loan/deposit/repayment moved, not just a Y/N "was it an account payee cheque" flag. The valid codes are:
- Prescribed banking modes: `C` (cheque), `BD` (bank draft), `E` (ECS), `CC` (credit card), `DC` (debit card), `NB` (net banking), `IMPS`, `NEFT`, `RTGS`, `UPI`, `BHIM`, `AOM` (any other mode).
- Cash / non-bank-instrument modes: `CP` (cash payment), `CR` (cash receipt), `PTNAPC` (payment through non-account-payee cheque), `RTNAPC` (receipt through non-account-payee cheque).
- Non-monetary settlement modes (the loophole this amendment specifically closes — loans "squared up" via book entries rather than cash/cheque were previously reported ambiguously): `TOA` (transfer of asset), `TOL` (transfer of liability), `COA` (conversion of asset), `COL` (conversion of liability), `JED` (journal entry — debit), `JEC` (journal entry — credit), `AOMD`/`AOMC` (any other mode — debit/credit).

**Form letters vs schema codes.** The notification's Note 1 labels the non-banking natures with letters; the e-filing schema uses the short codes above. Map them as: A cash paid = `CP`, B cash received = `CR`, C paid by non-account-payee cheque = `PTNAPC`, D received by non-account-payee cheque = `RTNAPC`, E transfer of asset = `TOA`, F transfer of liability = `TOL`, G conversion of asset = `COA`, H conversion of liability = `COL`, I journal entry debit = `JED`, J journal entry credit = `JEC`, K any other mode debit = `AOMD`, L any other mode credit = `AOMC`. In the workpaper write both, e.g. "B — cash received (CR)".

This means: if a loan was squared up by converting it into equity, by journal-entry set-off against a payable, or by a transfer of an asset in lieu of cash — that must now be coded explicitly (`COA`/`COL`/`JED`/`JEC`/`TOA`/`TOL`), not silently omitted. When reviewing the unsecured loan ledger, specifically look for loans that disappear from the balance without a corresponding bank entry — these are journal-entry squareups that must be captured under this new coding, and are a common miss.

**Source documents**: unsecured loan confirmation statements/balance confirmations, loan ledgers (party-wise), related-party loan/advance registers, bank statements (to identify cash deposits/withdrawals and distinguish account-payee vs. bearer cheques where visible from bank advice), cash book (for cash receipts/payments testing 269ST), sale/debtor ledgers for large single-customer cash collections, property sale/purchase agreements and advance receipts for 269SS "specified sum" testing.

**Procedure**:
1. Extract the full unsecured loan/deposit ledger (party-wise) for the year; for each party with a loan/deposit balance exceeding Rs 20,000 taken or squared up during the year, capture name, address, PAN (mandatory unless genuinely unavailable — flag `[MISSING — CONFIRM WITH CLIENT]` if PAN not on file), amount taken, whether squared up during the year, maximum outstanding at any time during the year (requires scanning the running ledger, not just opening/closing), and the mode/code of acceptance.
2. Repeat symmetrically for repayments (269T) using the loan ledger's debit side.
3. Independently scan the cash book and debtor/customer ledgers for any single-day aggregate cash receipt, single transaction, or event-linked set of transactions from one person totalling Rs 2,00,000 or more — this is NOT limited to loan transactions and is easy to miss if the review is scoped only to the loan ledger.
4. Check property transaction advances (booking advances/token money on immovable property, whether given or received) against the 269SS "specified sum" limb (31(b)) separately from ordinary loans.
5. For every 269SS/269T entry, confirm the mode of transfer from bank statements/vouchers rather than assuming "not cash therefore compliant" — a bearer cheque or a non-account-payee draft is still a violation even though it's "banking channel."

**Common mistakes**: testing only the loan ledger and missing large cash trade receipts/payments that trigger 269ST independently; treating an inter-branch or inter-partner capital account transfer as exempt without checking if it's genuinely a capital contribution (excluded) vs. disguised loan; missing the "maximum amount outstanding during the year" (a running balance calculation, not opening/closing); overlooking non-cash squareups (journal entries, asset conversions) that still require coding under the amended clause 31.

**Fabrication rule**: every name/PAN/amount must trace to the loan ledger, confirmation, or bank statement. Do not populate "maximum amount outstanding" by guesswork — it must be computed from the actual running ledger. If PAN is missing for a lender/depositor, flag rather than leaving blank silently, since PAN is a key statutory field for this clause.

---

## Clause 32 — Brought-forward losses, ownership-change restrictions, speculation

**Statute and schema mapping**:

**32(a) — Brought-forward loss/depreciation table.** Sec 32(2) (unabsorbed depreciation) and Chapter VI (Secs 70–80, set-off/carry-forward of losses). Schema: `Form3cdBflDa` (array, one row per AY/loss-type combination): `AssessmentYear` (format `YYYY-YY`), `NatureOfLossAllw` (enum: `HPLOSS` house-property loss, `BUSLOSS` business loss, `SPECLOSS` speculation loss, `SPECIFDLOSS` specified-business loss u/s 73A, `SHRTERMLOSS`/`LONGTERMLOSS` capital losses, `RACEHRSLOSS` owning-and-maintaining-race-horses loss, `UDLOSS`/`UDALLWNCE` unabsorbed depreciation/allowance), `AmtReturned` (as per the original return), `AmtAssessed` (as per assessment order, if assessed) with `OrderNo`/`DateOfOrder` reference, `amtAdjusted` (amount allowed to be carried forward to/set off in the current PY), and `Remarks`. Source: prior years' ITRs, prior years' tax audit reports (their own clause 32(a) tables — the cleanest source), assessment/appellate orders where scrutiny has occurred, and the current year's computation of income showing brought-forward figures claimed.

**32(b) — Change in shareholding restricting carry-forward, Sec 79.** Test: for a closely-held company, if beneficial shareholding carrying not less than 51% of voting power as of the last day of the loss year does not continue as of the last day of the current PY, brought-forward business losses (not unabsorbed depreciation, which is unaffected by Sec 79) lapse — subject to exceptions for eligible start-ups (Sec 79(1) proviso, more relaxed condition: continuity of at least one original shareholder), amalgamation/demerger of certain categories, and death/gift transfers among relatives. Schema: `Form3cdFlags.ChngShareSec79` (`Y|N|X` — `X` presumably for not-applicable, e.g. non-company assessees, firms, individuals for whom Sec 79 is irrelevant). Source: share transfer register/Form MGT-7, shareholding pattern as of the relevant balance sheet dates.

**32(c) — Set-off against 115BAA/special-regime income.** Where the assessee has opted for a concessional tax regime (Sec 115BAA for companies, or analogous 115BAC/115BAD elsewhere) certain brought-forward losses/unabsorbed depreciation attributable to deductions not allowed under that regime (e.g., additional depreciation, investment allowance) cannot be set off against regime income. In the bundled schema this is captured as a **per-row flag inside the clause 32(a) table itself** — `Form3cdBflDa.allnotSection115baa` — rather than a separate top-level question; i.e., for each brought-forward loss/allowance year, indicate whether that specific carry-forward is restricted by a 115BAA-type election. `[SCHEMA NOTE — CA TO CONFIRM]`: this field-to-clause mapping is inferred from field naming and structure, not from an explicit schema description — cross-check against the live utility's actual clause 32(c) presentation before relying on it for e-filing.

**32(d) — Deemed public company, Sec 2(18).** Whether the company qualifies as one "in which the public are substantially interested" (e.g., a government company, a company whose shares are listed and freely transferable, certain statutory/subsidiary companies, cooperative-society-controlled companies, or Sec 25/Sec 8 companies) — relevant because such companies get more favourable treatment under Sec 79 and other provisions. Schema: `Form3cdFlags.SharesOfMem` (`Y|N`). Source: shareholding pattern, listing status, MOA/AOA.

**32(e) — Speculation loss, Sec 73.** Whether the assessee incurred a speculation loss during the year (a "speculative transaction" under Sec 43(5) — a contract for purchase/sale of a commodity/stocks/shares periodically or ultimately settled otherwise than by actual delivery, subject to specified exceptions for hedging, jobbing, and derivatives traded on recognised exchanges). Schema: `Form3cdSpecloss73` = `Form3cdSpec73Flag` (`Y|N`) + `Form3cdSpec73Detail` (free text). Source: trading account/scrip-wise trading ledger, F&O/derivatives statements from the broker (note: exchange-traded derivatives transactions are statutorily excluded from "speculative transaction" and should not be flagged here).

**32(f) — Loss under Sec 73A (specified business, Sec 35AD).** Loss from a "specified business" eligible for 100% deduction under Sec 35AD (e.g., cold chain facilities, warehousing for agri-produce, hotels, hospitals, developing/operating infrastructure facilities meeting Sec 35AD conditions) can only be set off against profit of another specified business, and carried forward indefinitely for that purpose only. Schema: `Form3cdSpec73A` = `Form3cdSpec73AFlag` (`Y|N`) + `Form3cdSpec73ADetail`. Source: business classification/segment records — applicable only if the client actually operates a Sec 35AD-eligible business, which is uncommon for a typical SME/trading/professional client.

**32(g) — Deemed speculation business, Explanation to Sec 73 (companies only).** A company (other than a company whose principal business is banking, or the granting of loans and advances, or an investment company predominantly earning income from house property/capital gains/other sources) whose business consists wholly or mainly of the purchase and sale of shares of other companies is *deemed* to be carrying on a speculation business to the extent of that share-trading activity, even though the transactions involve actual delivery (so the Sec 43(5) speculative-transaction test doesn't strictly apply — this is a separate deeming fiction). Schema: `Form3cdSpecdeemdBus73` = `Form3cdSpecdeemdBusFlag` (`Y|N|X`, `X` likely for non-company assessees where this Explanation cannot apply) + `Form3cdSpecdeemdBusDetail`.

**Common mistakes across 32**: pulling brought-forward figures from the client's internal computation sheet without reconciling to the actual prior-year filed ITR/tax audit report (self-reported carry-forward figures can silently diverge from what was actually assessed/allowed); missing a Sec 79 shareholding-change trigger because share transfers were effected informally (unregistered transfer deeds, family settlements) without updating the statutory register; applying the Sec 73 Explanation deemed-speculation test to non-company assessees (it only applies to companies); treating derivatives/F&O trading losses as ordinary speculation loss under Sec 73 (F&O on recognised exchanges is excluded from "speculative transaction" under the Sec 43(5) proviso and is instead subject to its own turnover/loss rules, though this doesn't change how 32(e) NatureOfLossAllw is coded if it's a genuine off-exchange speculative loss).

**Fabrication rule**: every AY/amount in the 32(a) table must trace to an actual prior-year filed return, tax audit report, or assessment order — never back-compute a plausible-looking carry-forward figure. If a prior year's tax audit report or ITR is not available, flag `[MISSING — CONFIRM WITH CLIENT: prior year ITR/3CD for AY __ required]` for each missing year rather than omitting the row or guessing the figure.

---

## Clause 33 — Chapter VI-A / Chapter III deductions

**Statute**: Deductions under Chapter VI-A (Secs 80C–80U) and the SEZ/free-trade-zone exemptions under Chapter III (Secs 10A/10AA) — clause 33 requires, section-wise, the amount debited to the P&L (if any) and the amount actually admissible per the provisions (which may differ from the P&L-debited amount, since many Chapter VI-A deductions are computed *below the line* on total income, not as a P&L expense).

**Schema**: `Form3cdChapVIaChapIII` (array): `Section` (enum of 39 codes: `10A`, `10AA`, `80C`, `80CCC`, `80CCD`, `80CCF`, `80CCG`, `80CCH`, `80D`, `80DD`, `80DDB`, `80E`, `80EE`, `80G`, `80GG`, `80GGA`, `80GGB`, `80GGC`, `80IA`, `80IAB`, `80IAC`, `80IB`, `80IBA`, `80IC`, `80ID`, `80IE`, `80JJA`, `80JJAA`, `80LA`, `80M`, `80P`, `80PA`, `80QQB`, `80RRB`, `80TTA`, `80TTB`, `80U`, `80EEA`, `80EEB`), `Amt`.

**Business-relevant deductions to actively check** (most likely to be genuinely claimed by a business/firm/company audit client):
- **80JJAA** (additional employee cost deduction, 30% of additional employee cost for 3 years, subject to conditions on minimum employment period and wage caps) — check the P&L for wage/salary growth and whether the client has computed and claimed this; frequently under-claimed by SMEs who are unaware of it, and frequently over-claimed without proper new-employee identification.
- **80-IA/80-IAB/80-IAC/80-IB/80-IBA/80-IC/80-ID/80-IE** (profit-linked deductions for infrastructure, SEZ developers, eligible start-ups, specified industrial undertakings, housing projects, hotels, etc.) — check for a separate profit-and-loss segment/Form 10CCB (accountant's report, a prerequisite for these claims).
- **80GGA** (donations for scientific research/rural development, allowed to a non-business-income assessee, but also relevant where a business has made such donations if the donation isn't otherwise embedded in business expenditure) — verify against donation receipts and Form 10BE.
- **80M** (inter-corporate dividend deduction, for companies receiving dividends from other domestic companies and further distributing) — check dividend income and distribution timeline.
- **80P** (cooperative society deductions) — only relevant if the assessee itself is a cooperative society.
- **80LA** (offshore banking units / IFSC units) — narrow applicability.
- **10A/10AA** (SEZ unit profit exemption, being phased out — 10A largely sunset, 10AA still relevant for SEZ units within their eligibility window) — check for a separate SEZ-unit profit computation and Form 56F (accountant's certificate).

**Deductions that are usually personal, not business, in nature** — flag if seen attached to a firm/company/business audit as unusual: `80C`, `80CCC`, `80CCD`, `80CCF`, `80CCG`, `80CCH`, `80D`, `80DD`, `80DDB`, `80E`, `80EE`, `80EEA`, `80EEB`, `80G` (donations — usually personal, though a company can claim 80G on qualifying donations, so verify rather than assume it's an error), `80GG`, `80QQB`, `80RRB`, `80TTA`, `80TTB`, `80U`. Presence of these against a company/firm audit warrants a second look — likely a proprietorship's personal expenses run through the business, or a genuine but less common corporate 80G donation.

**Source documents**: computation of income/tax computation sheet (primary source — this is where claimed deductions are consolidated), P&L account (for any deduction actually debited as an expense, e.g., certain donations), Form 10CCB/56F/10BE accountant's certificates where the underlying deduction requires one, donation receipts, employee cost records for 80JJAA.

**Procedure**: cross-check every section claimed in the computation of income against supporting documentation (accountant's certificate where mandated, donation receipts, employee addition records); confirm the amount claimed as "admissible" reflects the correct statutory computation (e.g., 80JJAA's 30%-for-3-years mechanic, not just wage cost booked) rather than simply copying the P&L or computation-sheet figure without verification.

**Fabrication rule**: report only sections actually claimed in the computation of income with supporting documentation — do not infer a Chapter VI-A claim from indirect evidence (e.g., seeing a donation in the P&L does not by itself confirm an 80G claim was actually made in the computation; check the computation of income directly).

---

## Clause 34 — TDS/TCS compliance (Chapter XVII-B / XVII-BB)

This is one of the highest-value clauses to get right — TDS defaults surfaced here (short deduction, short deposit, late deposit) directly drive **disallowance under Sec 40(a)(ia)/40(a)(i), reportable at clause 21(b)** — always cross-reference the two clauses so a default identified here is reflected as a corresponding add-back there, and vice versa.

### 34(a) — TDS/TCS deducted/collected table

**Schema**: `Form3cdChapXVII` (array): `TAN` (format 4 letters + 5 digits + 1 letter), `Sec` (enum of 47 codes covering the deducting sections: `192`, `192A`, `193`, `194`, `194A`, `194B`, `194BA`, `194BB`, `194C`, `194D`, `194DA`, `194E`, `194EE`, `194F`, `194G`, `194H`, `194-I`, `194-IA`, `194-IB`, `194-IC`, `194J`, `194K`, `194L`, `194LA`, `194LB`, `194LBA`, `194LBB`, `194LBC`, `194LC`, `194LD`, `195`, `196A`, `196B`, `196C`, `196D`, `206C`, `194M`, `194N`, `194O`, `194Q`, `194P`, `206AB`, `206CCA`, `194S`, `194R`, `194T` (new — TDS on payments to partners, inserted by Finance Act 2024, effective FY 2024-25), `OTH`), `NatureOfPaymnt`, `AmtOfNatureSpec` (total payment/receipt of that nature), `TotTaxDedCollectd` (total amount on which tax was required to be deducted/collected), `TotTaxSpecRate`/`AmtTaxSpecRate` (amount deducted at the specified rate), `TotLessThanSpecRate` (amount deducted at a rate lower than specified — needs a reason), `AmtTaxDedOrCollect` (tax actually deducted/collected), `AmtNotDepToGovt` (amount not yet deposited to the Central Government). If the transaction table exceeds 500 rows, the utility expects a CSV attachment instead of inline rows (`Form3cdChapXVIIInfo.CsvDtls`: `HasMoreThan500`, base64 `Attachment` with `mimetype: text/csv`) — for a client with a large deductee base, plan to export a CSV rather than manually enumerating every row.

**Procedure**: build this table from the **TDS/TCS returns actually filed** (Form 24Q for salary, 26Q for other resident payments, 27Q for non-resident payments, 27EQ for TCS), not by re-deriving it from the P&L independently — the returns are the authoritative source for what was actually deducted, at what rate, and deposited by when. Then separately cross-check every payment ledger subject to TDS (salary, contractor payments 194C, professional/technical fees 194J, rent 194-I/194-IB, commission/brokerage 194H, interest 194A, purchase of goods 194Q, e-commerce 194O, VDA transfer 194S) to identify amounts that **should have been subjected to TDS but were not** at all (a gap the filed returns won't show, since a missed deduction produces no return entry) — this requires an independent walk of the P&L/payment ledgers above the applicable threshold for each section, not just a TAN-return reconciliation. Also check Sec 206C(1H) TCS-on-sale-of-goods applicability (turnover > Rs 10 crore in preceding year and receipts from a buyer > Rs 50 lakh) — note Sec 194Q (buyer-side TDS on purchase of goods) overrides 206C(1H) when both would otherwise apply, so confirm which side is actually responsible before flagging a gap.

### 34(b) — Timeliness of TDS/TCS statement filing

**Schema**: `Form3cdTaxDedCollect` (array): `TAN`, `TypeOfForm` (enum: `24`, `24G`, `24Q`, `26`, `26A`, `26B`, `26Q`, `26QAA`, `26QB`, `26QC`, `26QD`, `26QE`, `26QF`, `27`, `27A`, `27B`, `27BA`, `27C`, `27D`, `27E`, `27Q`, `27EQ`), `DueDateOfFurnish`, `DateOfFurnish`, `TransactionsFlag` (`Y|N` — whether any transactions were delayed), `ListDetailsTransactions` (if delayed). Gated by flag `Form3cdFlags.TaxPrescTime` (`Y|N`). Also supports a >500-row CSV attachment (`Form3cdTaxDedCollectInfo`).

**Source**: TRACES portal filing acknowledgements/statement status for each TAN/quarter, compared against the statutory due dates (quarterly, typically the last day of the month following the quarter, with Q4 salary/other statements due by 31 May).

### 34(c) — Interest under Sec 201(1A) / 206C(7)

**Schema**: `Form3cdSec2011A206C7` (array): `TAN`, `AmtOfIntrest`, `AmtPaid`, `DueDate`. Gated by flag `Form3cdFlags.Sec201_1A_206_C7` (`Y|N|X`).

**Statute**: Sec 201(1A) — interest at 1% per month (short/non-deduction) or 1.5% per month (deduction made but deposited late) from the date deduction was due to the date of actual deduction/deposit. Sec 206C(7) — parallel interest provision at 1% per month for TCS defaults.

**Procedure**: this is best computed from the TRACES portal's own interest/default computation (Form 26AS/TRACES justification reports for each TAN) rather than manually recomputing month-wise interest, since TRACES applies the exact deduction/deposit dates already on record; use manual computation only as a cross-check or where TRACES data is unavailable.

**Common mistakes across clause 34**: treating "TDS return filed" as proof that all TDS-liable payments were captured (returns only show what the client believed was deductible — independent P&L testing is required to catch omitted deductions); missing 194Q/206C(1H) interplay; missing the newly-inserted 194T (TDS on payments to partners — salary, remuneration, commission, bonus, interest paid by a firm to its partners, effective FY 2024-25 onward) for partnership/LLP clients; not reconciling `AmtNotDepToGovt` (deducted-but-not-deposited) which is a serious default with prosecution exposure under Sec 276B, not just a disallowance issue.

**Fabrication rule**: every TAN, section, amount, and date in this clause must trace to the actual filed TDS/TCS returns or TRACES records — never estimate deduction/deposit dates, and never assume a payment was TDS-compliant without checking the payment ledger against the applicable section's threshold. Missing TDS returns should be flagged `[MISSING — CONFIRM WITH CLIENT: TDS returns for TAN __ not provided]`.

---

## Clause 35 — Quantitative details

**Applicability note**: mandatory only for assessees subject to tax audit under Sec 44AB(a) (turnover-based audit) who deal in goods — i.e., trading or manufacturing concerns. **For a pure service business or a professional (44ADA-type or service-only 44AB(b)/(c) audit) with no goods/inventory, clause 35 is not applicable — write "N/A — service business, no goods dealt in" rather than leaving it blank without explanation**, since a reviewer should not have to guess whether "blank" means "not applicable" or "not yet completed."

**Schema**: `Form3cdTradeRawProdDet` (array), with `Form3cdTradeRawProdDetPK.ConcernType` distinguishing four row types, and a shared set of quantity fields reused with different meaning depending on `ConcernType`:

- **`TRADE`** — clause 35(a), trading concern. Fields used: `ItemName`, `Unit` (coded, e.g. `101`=gms, `102`=kilograms, `103`=litre, `107`=numbers, `108`=quintal, `109`=ton — see full code table in schema), `OpeningStock`, `PurchasePy`, `SalesDurPy`, `ClosingStock`, `ShortageExcess`. `ConsumptionManufacPy`/`FinishedProdYield`/`PercentageYield` are not meaningful for `TRADE` rows and should be left blank.
- **`RAWMAT`** — clause 35(b)(i), raw materials of a manufacturing concern. Fields: `ItemName`, `Unit`, `OpeningStock`, `PurchasePy`, `ConsumptionManufacPy` (consumption during the year), `SalesDurPy` (scrap/surplus raw material sold, if any), `ClosingStock`, `FinishedProdYield` (yield of finished product obtained from this raw material), `PercentageYield` (yield %), `ShortageExcess`.
- **`PRODNAME`** — clause 35(b)(ii), finished products. Fields: `ItemName`, `Unit`, `OpeningStock`, `PurchasePy` (finished goods purchased/traded, if any, separate from manufactured output), `ConsumptionManufacPy` (**repurposed for this row type to mean quantity manufactured during the year** — confirm this mapping against the live utility rather than assuming), `SalesDurPy`, `ClosingStock`, `ShortageExcess`.
- **`BYPRODNAME`** — clause 35(b)(ii), by-products, same field usage as `PRODNAME`.

**`[SCHEMA NOTE — CA/DEV TO CONFIRM]`**: the reuse of `ConsumptionManufacPy` for both "raw material consumed" (RAWMAT rows) and "quantity manufactured" (PRODNAME/BYPRODNAME rows) is inferred from the flat, shared row structure — verify against the current e-filing utility's actual field labels for these row types before final submission.

**Source documents**: perpetual/periodic stock/inventory register (item-wise), production reports/manufacturing statements (if the client maintains formal production records — many SMEs don't, and quantities may need to be reconstructed from purchase, sales, and closing stock alone), physical stock verification/count sheets if available, purchase and sales registers (item/quantity-wise, not just value-wise — this clause is quantity-driven, and value-only accounting records are insufficient on their own).

**Procedure**:
1. Identify the assessee's principal items of goods (do not attempt to list every SKU for a business with thousands of items — report the "principal items," consistent with how the client's own stock records are organised, and note where minor/residual items have been grouped).
2. For a trading concern, pull opening stock, purchases, sales, and closing stock in **quantity terms** (not value) for each principal item; compute shortage/excess as the balancing figure against what the stock register shows, and investigate/explain any material shortage or excess rather than reporting it as a bare number.
3. For a manufacturing concern, separately tabulate raw materials (with consumption and yield %) and finished products/by-products (with quantity manufactured), reconciling raw material consumption to finished output via the stated yield percentage — a yield percentage far outside the client's historical range or industry norm is worth flagging.
4. If the client has no formal stock/production register (common for smaller manufacturers), reconstruct quantities as best as available data allows and flag the specific gaps `[MISSING — CONFIRM WITH CLIENT: no item-wise quantity records maintained for __]` rather than fabricating a plausible-looking quantity reconciliation.

**Common mistakes**: reporting only value figures (Rs) instead of quantities, which is what this clause actually requires; omitting the shortage/excess column, or reporting a shortage without any investigation/explanation when it's unusually large; forgetting that a service business should be marked N/A with a reason rather than left blank; mixing up raw-material yield % (finished output per unit of raw material) with a generic gross-margin percentage.

**Fabrication rule**: this clause is unusually easy to fabricate plausibly because opening + purchases − sales ≈ closing arithmetic can be back-solved to make numbers "work" even when the underlying quantities are invented. Do not do this — every quantity must trace to the stock register, production report, or purchase/sales register. If item-wise quantity records don't exist, say so explicitly rather than presenting a self-consistent but unverified reconciliation.
