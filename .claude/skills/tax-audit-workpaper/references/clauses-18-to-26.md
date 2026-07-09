# Form 3CD — Clauses 18 to 26: Detailed Reference (AY 2026-27 / FY 2025-26)

Conventions used throughout this file:
- **Never fabricate a factual figure that is not present in the source documents provided.** If a document needed to complete a sub-item is missing, write `[MISSING — CONFIRM WITH CLIENT]` against that line instead of guessing a number.
- Where data IS present but requires an interpretive/judgment call (e.g. classifying an expense, deciding if an exception applies), make your best-supported call and tag it `[JUDGMENT CALL — CA TO CONFIRM]`. Do not leave judgment calls blank — a defensible first-pass answer is the deliverable.
- Schema field/group names below are from `schema_3CB.json` / `3CB_structure.txt` in this skill's `references/schema/` folder — use them to know exactly which structure to populate.
- "P&L" = Statement of Profit and Loss / Income & Expenditure account of the client for FY 2025-26 (1 April 2025 to 31 March 2026).

---

## Clause 18 — Depreciation allowable under the Income-tax Act (Section 32)

**Statutory basis:** Section 32(1) (rates, WDV method, 50% rate for assets used <180 days), Section 32(1)(iia) (additional depreciation — see note below), Section 43(1) read with Explanations 9 and 10 (adjustment to actual cost for CENVAT/GST input credit and for subsidy/grant), Section 43A (adjustment to actual cost for exchange-rate fluctuation on imported assets), Section 50 (deemed short-term capital gains on depreciable assets), Rule 5 and Appendix I to the Income-tax Rules (block-wise rates).

**Schema fields:** `Form3cdDeprAllw` — array, one row per block of assets. Key sub-fields: `methodOfDepreciation` (enum `WDV`/`SLM`), `DescBlockAssets` (enum 1–48 mapping block description + rate, e.g. `1: Plant and Machinery @ 15%`, `8: Building @ 5%`, `12: Intangible Assets @ 25%`), `RateOfDep`, `OpeningWDV`, `Additions[]` (each: `PurchaseOrSaleDate`, `DatePutToUse`, `PurchaseOrSaleValue`, `Modvat` [CENVAT/GST ITC reduction], `ExchangeRateChange` [s.43A], `subsidyGrant` [Explanation 10], `TotalPurchaseValue`), `TotalPurchase`, `Puttouseforlessthan180days` / `Puttousefor180daysormore` totals, `Lessthan180` / `morethan180` (depreciation computed at half/full rate on each bucket), `Deductions[]` (each: `PurchaseOrSaleDate`, `PurchaseOrSaleValue`, `Deletioncheckbox`), `TotalDeduction`, `DepAllowable`, `WrittenDownVal`.

### Source documents
1. Prior year's Form 3CD depreciation schedule / Clause 18 workpaper (gives Opening WDV per block — this is the single most important starting number; if the prior year's tax audit report is unavailable, opening WDV must come from the client's tax computation / ITR filed for AY 2025-26).
2. Fixed Asset Register (FAR) for the year — additions and deletions with dates.
3. Purchase invoices for additions (to verify GST/CENVAT credit availed and, for imported assets, the forex rate and any exchange fluctuation on repayment of the related foreign currency loan).
4. Sale invoices / scrap sale vouchers / insurance-claim settlement for deletions, with dates.
5. Any government subsidy/grant sanction letter linked to acquisition of a specific asset.
6. Board resolution / management note on any asset written off, destroyed, or scrapped without sale consideration.

### Step-by-step procedure
1. **Reconcile opening WDV.** Opening WDV per block for FY 2025-26 = closing WDV per block as per the tax audit report / income-tax computation for AY 2025-26 (NOT the books WDV, which follows Companies Act/AS rates and will differ). If prior-year Form 3CD is unavailable: `[MISSING — CONFIRM WITH CLIENT]` and request the last filed tax computation.
2. **Classify every addition into the correct block** using `DescBlockAssets`. Match the FAR description to the closest Appendix I category — most SME clients will only need: Building (residential 5% / non-residential incl. office/factory/godown 10% / purely temporary structure 40%), Furniture & Fittings (10%), Plant & Machinery — general (15%), Motor cars not used in hiring business (15%), Motor buses/taxis/lorries used in a hiring business (30%), Computers including computer software (40%), Intangible assets — know-how, patents, copyrights, trademarks, licences, franchises, any other business/commercial right of similar nature (25%). **Goodwill is NOT depreciable** (Finance Act 2021 removed goodwill from the "intangible asset" block w.e.f. AY 2021-22) — if the FAR still carries goodwill in an intangible block, exclude it and flag `[JUDGMENT CALL — CA TO CONFIRM]`.
3. **Compute actual cost of additions** = invoice cost − CENVAT/GST input tax credit availed on the asset (Explanation 9 to s.43(1); schema field `Modvat`) − any portion funded by a government subsidy/grant (Explanation 10; field `subsidyGrant`) ± exchange-rate adjustment for imported assets where the acquisition was funded by foreign-currency borrowing and there has been an actual increase/decrease in the liability on repayment during the year, not merely notional year-end restatement (s.43A; field `ExchangeRateChange`).
4. **Split additions by usage period**: assets put to use for 180 days or more in the PY get full rate; assets put to use for less than 180 days get exactly half the normal rate (proviso to s.32(1)). Use `DatePutToUse`, not `PurchaseOrSaleDate` — an asset purchased in April but commissioned/installed only in November is a <180-day addition. Populate `Lessthan180`/`morethan180` (or `Puttouseforlessthan180days`/`Puttousefor180daysormore`) accordingly. **Common mistake**: staff apply the 180-day test to the purchase date instead of the "put to use" date — always ask for the commissioning/installation date for capital equipment, not just the invoice date.
5. **Process deletions**: for each asset sold/discarded, capture `PurchaseOrSaleDate` and `PurchaseOrSaleValue` (net sale proceeds, i.e. after deducting selling expenses if any — deduct scrap value/sale proceeds from the block, not from the individual asset).
6. **Test Section 50 (block ceases to exist / negative WDV):**
   - If ALL assets in a block are sold/discarded during the year (block ceases to exist), and sale proceeds exceed (Opening WDV + Additions), the excess is a **short-term capital gain under Section 50** (report separately in the capital gains schedule of the ITR, not in clause 18) and depreciation on that block for the year is **NIL**. If sale proceeds are less than (Opening WDV + Additions), the shortfall is a short-term capital LOSS under Section 50 — again no depreciation is allowable since the block is empty.
   - If the block still has assets remaining but (Opening WDV + Additions − Deductions) is negative (i.e. sale proceeds of the assets sold exceed opening WDV + additions), the closing WDV is restricted to NIL, and the negative amount is again a short-term capital gain under Section 50. WDV can never be carried forward as negative.
   - Flag any block hitting either condition with `[JUDGMENT CALL — CA TO CONFIRM]` since the STCG entry must additionally flow into the capital gains schedule of the return, outside Form 3CD.
7. **Compute depreciation allowable** = (Opening WDV + full-rate additions) × full rate + (half-rate additions) × half rate, less any Section 50 adjustment above, giving `DepAllowable`. Closing `WrittenDownVal` = Opening WDV + Additions − Deductions − DepAllowable.
8. **Method**: for the Income-tax Act, depreciation is almost always WDV (`methodOfDepreciation = WDV`); SLM is available only to specified electricity generation/distribution undertakings under Rule 5(1A) — do not select SLM unless the client is such an undertaking.
9. **Additional depreciation (s.32(1)(iia))** on new plant & machinery for manufacturing/power-generation companies (20% of actual cost, or 10% if put to use <180 days, with the balance 10% claimable in the immediately following year) is computed and added to `DepAllowable` for the relevant block, not reported as a separate line — verify eligibility (new P&M, not second-hand, not office appliances/vehicles/ships/aircraft) before adding it.

### Common mistakes to watch for
- Using books WDV (Companies Act Schedule II rates) instead of tax WDV as the opening balance.
- Missing the CENVAT/GST credit reduction on additions (overstates actual cost and depreciation).
- Applying full rate to assets used <180 days.
- Forgetting Section 50 short-term capital gains when a block empties out or WDV would go negative.
- Continuing to depreciate goodwill.
- Netting sale proceeds against WDV of the individual asset rather than the block as a whole (Income-tax Act depreciation is on a block basis, not asset-by-asset).

If the fixed asset register or prior-year tax computation is not provided, mark the entire clause `[MISSING — REQUEST FIXED ASSET REGISTER / PRIOR YEAR FORM 3CD FROM CLIENT]` rather than estimating WDV.

---

## Clause 19 — Amounts admissible under Sections 33AB, 33ABA, 35, 35ABB, 35AC, 35AD, 35CCA, 35CCB, 35CCC, 35CCD, 35D, 35DD, 35DDA, 35E

**Statutory basis:** as named per sub-section; see table below.

**Schema fields:** `Form3cdDebitPlTotAllw` — array, one row per applicable section. Fields: `Section` (enum: `32AC`, `32AD`, `33AB`, `33ABA`, `35_1_i`, `35_1_ii`, `35_1_iia`, `35_1_iii`, `35_1_iv`, `35_2AA`, `35_2AB`, `35_ABA`, `35ABB`, `35AC`, `35AD`, `35CCA`, `35CCB`, `35CCC`, `35CCD`, `35D`, `35DD`, `35DDA`, `35E`, `any other relevant section`), `Total` (amount debited to P&L), `Allowable` (amount admissible as per the Act), `Admissible`, `Others` (free text, used for the "any other relevant section" row). Note the schema enum also includes `32AC`/`32AD` (investment allowance) and `35_ABA` (telecom spectrum fee, s.35ABA — distinct from 33ABA site restoration fund) even though these are not in the task's core list; include them if applicable to the client.

### General approach — most SME clients will have NIL for this entire clause
Before doing detailed sub-section analysis, scan the P&L and the notes to accounts / tax computation for any of: (a) a "preliminary expenses written off" or "share issue expenses amortised" line — points to s.35D; (b) any R&D / scientific research expenditure, especially if the client is a pharma, manufacturing, agri-input, or tech company — points to s.35(1)/(2AB); (c) amalgamation/demerger/VRS costs — s.35DD/35DDA; (d) tea/coffee/rubber, petroleum/gas exploration, mining, or telecom licensing businesses — s.33AB/33ABA/35E/35ABB (all industry-specific and rare). If none of these triggers are present, this clause is safely `NIL` for the whole row set — do not invent line items.

### Sub-section reference table

| Section | What it covers | Admissible amount | Typical client |
|---|---|---|---|
| 33AB | Tea/coffee/rubber development account deposit (with NABARD-approved bank/authority) | Lower of amount deposited (within 6 months of year-end or return due date, whichever earlier) OR 40% of profits of that business (before this deduction, before c/f losses) | Tea/coffee/rubber growers/manufacturers only — rare |
| 33ABA | Site Restoration Fund deposit (petroleum/natural gas prospecting/extraction) | Lower of amount deposited OR 20% of profits of that business | Oil & gas E&P companies only — very rare |
| 35(1)(i) | Revenue expenditure on in-house scientific research related to the business (incl. 3 years pre-commencement expenditure, deemed incurred in year of commencement) | 100% of expenditure | R&D-heavy manufacturing/pharma |
| 35(1)(ii) | Payment to an approved research association/university/college/institution for scientific research | 100% (weighted rates of 125%/150% were phased out; from AY 2021-22 onward the rate is 100% for most such donations — verify against the institution's current approval/notification) | Uncommon; verify recipient's valid approval under s.35(1)(ii) is current |
| 35(1)(iia) | Payment to an approved company for scientific research | 100% | Rare |
| 35(1)(iii) | Payment to an approved research association/university/college/institution for research in social science or statistical research | 100% | Rare |
| 35(1)(iv) | Capital expenditure (other than land) on scientific research related to the business, per s.35(2) | 100% deduction in year incurred (no block/WDV carry) | R&D companies |
| 35(2AA) | Payment to a National Laboratory/university/IIT/specified person for scientific research under an approved program | 100% (was 200%, phased down; 100% from AY 2021-22) | Rare, needs matching certificate |
| 35(2AB) | In-house R&D expenditure (revenue + capital, excluding land/building) by a company, at a facility approved by DSIR (Form 3CM) | 100% (was 200%/150% for AY 2018-19 to AY 2020-21; 100% from AY 2021-22 onward — this is settled law now, do not apply old weighted rates) | **Most common of this whole clause** — check DSIR Form 3CL certificate; the amount DSIR certifies as eligible R&D expenditure often differs from the amount debited to P&L — report both figures, `Total` (debited) vs `Allowable` (DSIR-certified/admissible), and flag any gap `[JUDGMENT CALL — CA TO CONFIRM]` |
| 35ABA | Expenditure for obtaining right to use spectrum for telecom services | Amortised over useful life of the right | Telecom only — rare |
| 35ABB | Capital expenditure to acquire a telecom licence | Amortised in equal instalments over the number of years the licence remains in force | Telecom only — rare |
| 35AC | Payment to a PSU/local authority/approved association for an eligible project or scheme | **NIL — deduction was discontinued for all assessees for AY 2018-19 onward** (Finance Act 2016 inserted s.35AC(7)). Any current-year debit under this head should NOT be claimed; it is most likely CSR expenditure that is separately disallowed under s.37(1) Explanation 2 — verify and reclassify, don't put it here | Discontinued — flag if client claims it |
| 35AD | Deduction for capital expenditure (other than land, goodwill, financial instrument) of a "specified business" (e.g. cold chain facility, warehousing for agri produce/sugar, 2-star+ hotel, 100+ bed hospital, affordable housing project, developing/maintaining infrastructure facility, semiconductor fab unit, bee-keeping, national gas/petroleum pipeline network) | 100% of capital expenditure in the year incurred, if business commenced in the year and conditions of s.35AD(2)/(3)/(4) met (no other deduction for the same asset, asset used for the specified business for 8 years or its WDV becomes taxable u/s 28) | Only if client is in a listed "specified business" — confirm eligibility criteria before claiming |
| 35CCA | Payment to an association/institution for a rural development program | Effectively obsolete for new payments in most cases (available broadly only for approvals predating early-1980s cut-offs) | Almost always NIL |
| 35CCB | Payment for a program of conservation of natural resources | Effectively obsolete (approvals largely predate 1 March 2002) | Almost always NIL |
| 35CCC | Expenditure on a notified agricultural extension project | 100% (was 150%, phased to 100% from AY 2021-22) | Agri-input companies (seed/fertiliser/agrochemical) running notified farmer-training programs |
| 35CCD | Expenditure (other than land/building) on a notified skill development project, by a company | 100% (was 150%, phased to 100% from AY 2021-22) | Companies running notified govt skill-development programs |
| 35D | Preliminary expenses (incorporation/ROC fees, share issue expenses, project report, legal charges for drafting MOA/AOA/agreements, market/feasibility survey costs) before commencement of business or extension of an undertaking | 1/5th of qualifying expenditure per year for 5 years, qualifying expenditure capped at 5% of "cost of the project" (or, for a company, the higher of cost of project / capital employed, at the assessee's option) | **Very common for newly incorporated/recently-listed companies** — check the P&L for "preliminary expenses written off"/"amortisation of share issue expenses"; verify the 1/5th computation and the 5%-of-project-cost cap; confirm which year of the 5-year amortisation window the client is in |
| 35DD | Expenditure on amalgamation or demerger, incurred by an Indian company | 1/5th per year for 5 years | Uncommon; check for one-off corporate restructuring in the year or prior years |
| 35DDA | Expenditure on payment under a Voluntary Retirement Scheme (VRS) to employees | 1/5th per year for 5 years, **regardless of how it is expensed in the books** (books may expense it upfront or per Ind AS actuarial rules) | Check if any VRS/restructuring payout occurred this year or in the preceding 4 years — book vs tax timing mismatch is the key thing to catch |
| 35E | Expenditure on prospecting for specified minerals | 1/10th per year for 10 years, subject to overall ceiling | Mining companies only — rare |

### Procedure
1. Pull the notes to accounts and P&L schedules for any amortisation/write-off line matching the above.
2. For each applicable section, record `Total` = amount actually debited to P&L this year, and `Allowable` = amount admissible per the Act's formula for that section (which may differ due to caps, spread-over-years amortisation, or DSIR-certified ceilings).
3. Where the P&L debit and admissible amount differ, this difference becomes an addition/deduction in the computation of total income — cross-check it flows correctly into the computation sheet.
4. If a section is inapplicable, do not create a row for it — leave the array empty for that section rather than inserting a zero placeholder unless the filing utility requires an explicit NIL declaration.

---

## Clause 20 — Bonus/commission to employees (s.36(1)(ii)) and employees' contributions to welfare funds (s.36(1)(va))

### 20(a) — Bonus or commission paid to an employee in lieu of profit/dividend (Section 36(1)(ii))

**Statutory basis:** Section 36(1)(ii) — bonus or commission paid to an employee is disallowed to the extent it would otherwise have been payable to the employee as profit or dividend, had it not been paid as bonus/commission.

**Schema fields:** `Form3cdEmpBonusComm` — array of `{ DetailsUs36, Amount }`.

**Source documents:** P&L bonus/commission expense ledger, employment contracts/board resolutions authorising bonus or commission to director-employees, shareholding pattern (to identify director-shareholders), Statutory Bonus Act computation (if applicable, for rank-and-file bonus which is NOT the target of this clause).

**Procedure:**
1. This clause is primarily relevant for **closely-held companies** where a director/employee is also a substantial shareholder. Statutory bonus paid to ordinary employees under the Payment of Bonus Act is not normally hit by s.36(1)(ii) — the concern is discretionary bonus/commission paid to director-shareholders that substitutes for a dividend the company would otherwise have had to declare (and which, unlike a dividend, is tax-deductible to the company and was — until dividend became taxable in the hands of shareholders again from AY 2021-22 — a tax-arbitrage device).
2. Scan the bonus/commission ledger for large, non-formulaic, or year-end payments to directors who are also significant shareholders. Compare against the company's distributable profits and dividend history for the year — a large "commission" to a director-shareholder in a year with no dividend declared, especially one that tracks the shareholder's ownership percentage rather than a performance metric, is the classic Section 36(1)(ii) fact pattern `[JUDGMENT CALL — CA TO CONFIRM]`.
3. For partnerships/LLPs, this test doesn't directly apply (partner remuneration is governed separately by s.40(b) — see Clause 21(c)).
4. If no such payment pattern exists, this sub-clause is NIL.

### 20(b) — Employees' contributions to welfare funds (Section 36(1)(va))

**Statutory basis:** Section 36(1)(va) read with Section 2(24)(x) — any sum received by the employer from an employee as the employee's contribution to a PF, superannuation fund, ESI, or any other fund for employee welfare, is allowable as a deduction ONLY IF credited to the employee's account in the relevant fund on or before the "due date" under the Act/Rules/order/notification governing that fund. This is entirely separate from Section 43B (which governs the EMPLOYER's own contribution).

**Schema fields:** `Form3cdEmpPfSuperann` — array of `{ NatureOfFund [enum: PROVIDENT | SUPERAN | GRATUITY | PROV1948 | OTHERWELFARE], Amount, DueDate, ActualAmount, ActualDate }`. (`PROV1948` = ESI, referencing the ESI Act 1948; `PROVIDENT` = EPF under the EPF & MP Act 1952; `SUPERAN` = superannuation fund; `GRATUITY` = employees' contribution to an approved gratuity fund, rare; `OTHERWELFARE` = any other employee welfare fund.)

**THE CRITICAL POINT — read this carefully, this is the single highest-value catch in this entire reference file:**

The Supreme Court in **Checkmate Services Pvt. Ltd. v. CIT** (Civil Appeal No. 2833 of 2016, decided 12 October 2022) held that:
- Section 36(1)(va) and Section 43B operate on **entirely different footing**. Section 43B's "grace period" (deduction allowed if paid on or before the due date for filing the return under s.139(1)) applies ONLY to the **employer's own contribution** to PF/ESI/superannuation etc.
- The **employee's contribution** (i.e., the amount deducted from the employee's salary/wages that the employer holds in trust and must deposit into the relevant fund) is never the employer's own money in the first place — it is deemed income of the employer under s.2(24)(x) the moment it is deducted, and is allowed as a deduction under s.36(1)(va) **only if actually credited to the employee's account in the relevant fund by the due date prescribed under that fund's own Act** (e.g., 15th of the following month for EPF; 15th/21st of the following month for ESI, per the respective statute/scheme, with a limited grace period under the specific Act's own rules, if any).
- **There is no extension to the income-tax return filing due date for employee contributions.** Even one day's delay in depositing the employee's share, beyond the due date fixed under the PF/ESI Act itself, results in **permanent, 100% disallowance** of that contribution — it cannot be cured by paying before the tax return due date, unlike almost every other item in this reference file that is governed by Section 43B relief.

**Source documents:** Salary register / payroll summary showing PF and ESI deductions made from employee salaries month by month, PF challans (ECR/challan receipt from EPFO portal) and ESI challans showing actual date of remittance, bank statement showing the actual debit date for each month's PF/ESI payment, PF/ESI due-date rules (generally, deposit within 15 days from the end of the month/wage period to which the contribution relates, though the CA should confirm current due dates under the applicable scheme — mark `[MISSING — CONFIRM WITH CLIENT]` if the exact statutory due date for the specific fund isn't independently verified).

**Procedure:**
1. Obtain a month-wise summary from the client of: (i) total employee PF/ESI contribution deducted from salary for that month, (ii) the statutory due date for depositing that month's contribution, (iii) the actual date of payment per the challan/bank statement.
2. For EVERY month, compare actual payment date to due date. If actual date > due date, even by one day, the ENTIRE employee's contribution for that month is disallowable under s.36(1)(va) and must be added back — regardless of whether it was eventually paid before the ITR due date.
3. Populate one row per fund per period (or a consolidated annual row per fund type, per the return utility's expected granularity) with `Amount` (contribution due), `DueDate`, `ActualAmount` (paid), `ActualDate`. Where `ActualDate` > `DueDate`, that amount is disallowed.
4. **Do not confuse this with the employer's own PF/ESI contribution** — that portion is governed by Section 43B (see Clause 26(b)) and DOES get the benefit of payment-before-return-due-date relief. Keep the two streams (employee's share vs employer's share) analytically separate even though they are often paid together in a single combined challan — the combined challan amount must be split back into employee and employer components using the payroll register.
5. If salary register / PF-ESI challans are not provided: `[MISSING — REQUEST SALARY REGISTER AND PF/ESI CHALLANS FROM CLIENT]`. Do not assume timely payment in the absence of evidence.

**Common mistakes:** treating this like a normal 43B item and giving return-due-date relief (wrong — no such relief exists for employee's share post-Checkmate); netting employee and employer contributions together instead of analysing them separately; missing a single late month buried in an otherwise-timely annual pattern; using the bank debit date instead of the date the fund records the credit (some challans are debited from the bank a day or two before EPFO/ESIC processes and dates the receipt — use the EPFO/ESIC challan date, not the bank value date, when they differ).

---

## Clause 21(a) — Amounts debited to P&L: capital/personal/political-ad/club/penalty/offence expenditure

**Statutory basis:** Section 37(1) (general disallowance of capital and personal expenditure, and of any expenditure incurred for a purpose that is an offence or prohibited by law — Explanation 1), Section 37(2B) (disallowance of advertisement expenditure in a souvenir/brochure/tract/pamphlet published by a political party), Explanation 3 to Section 37(1) (inserted by Finance Act 2022 — disallowance of expenditure incurred to settle proceedings initiated in relation to a contravention under specified laws).

**Schema fields:** `Form3cdDebPLExpnditure` — array of `{ ParticularType, Particulars, Amount }`. `ParticularType` enum: `CAPITAL`, `PERSONAL`, `ADVERTISMNT` (political party souvenir/brochure ad), `CLUBFEE` (club entrance fee/subscription — always disallowable as capital/personal in nature), `CLUBSERVICE` (club expenditure on services availed — allowable to the extent of genuine business use, disallow the personal-use portion), `PENALTY` (penalty/fine for violation of law), `OTHERPENALTY` (any other penalty or fine not for a legal violation, e.g. a contractual liquidated-damages-style penalty that is still not compensatory in nature), `UNDERLAW` and `OFFENCE` (the two limbs of Explanation 1 to s.37(1) — expenditure for a purpose that is prohibited by law / that is an offence), `SETTLE` (Finance Act 2022 addition — expenditure to settle a proceeding for contravention of a specified law; note this is a recent, easy-to-miss category).

### Procedure — how to spot each category from ledger scrutiny
1. Export/print the full P&L expense ledger (or a general ledger dump if the P&L is only summarised) and run text searches on account narrations for: `penalty`, `fine`, `fee/late fee`, `interest on delayed`, `donation`, `political`, `club`, `membership`, `entertainment`, `personal`, `director`, `settlement`, `compounding`, `SEBI`, `late payment charge`, `GST late fee`, `TDS late filing fee`. Also review any "Miscellaneous expenses" or "Other expenses" ledger line by line — these are where such items are most often buried.
2. **Capital expenditure debited to P&L**: look for large one-off amounts in repair/maintenance, or "consumables"/"tools" that are actually fixed-asset-scale purchases; cross-check against the FAR (Clause 18) — if an item should have been capitalised and depreciated but was expensed instead, it belongs here.
3. **Personal expenditure**: for owner-managed/family businesses, scan for expenses that read as personal (family travel, personal insurance premiums booked to the business, home expenses of proprietor/director routed through the company) — common in proprietorships and closely-held companies.
4. **Political-party advertisement**: search narrations for "advertisement", "souvenir", cross-reference against any political party name; note this is different from political donations under s.80GGB/80GGC (which are a deduction-from-total-income matter, not a P&L addback, though the P&L debit itself, if any, is still added back here since it's not a business expense at all).
5. **Club expenses**: obtain the club membership/subscription ledger; entrance fee and annual subscription are always disallowed as capital/personal in nature (`CLUBFEE`); expenditure on services actually availed at the club for business purposes (e.g. hosting a client lunch) may be allowed to the extent of demonstrable business use — `[JUDGMENT CALL — CA TO CONFIRM]` on the business-use proportion.
6. **Penalty/fine for violation of law**: search for GST/Customs/Excise/Income-tax/Labour-law/Environmental/ROC/SEBI/RBI penalty and interest-for-default line items. Note: **interest for delayed payment of a statutory due that is compensatory in nature (e.g. simple interest on late GST payment) is generally allowable and is NOT to be added back here** — only the penal/punitive component (penalty, fine) is disallowed. Reviewing the exact head under which the department levied the amount (penalty vs interest) is essential; don't blanket-disallow every "GST interest & penalty" ledger line without splitting the two.
7. **Offence / prohibited by law**: this includes things like fines for statutory non-compliance that don't fall neatly under "penalty" wording, illegal payments, or expenditure that is itself illegal (e.g., unauthorised freebies to doctors by pharma companies per CBDT Circular applying Explanation 1 read with Indian Medical Council regulations — a well-litigated example).
8. **Settlement expenditure (Explanation 3, Finance Act 2022, from AY 2023-24)**: any amount paid to settle proceedings initiated for a contravention under a law notified for this purpose (e.g. SEBI settlement, competition law settlement) is disallowed. This is a genuinely new provision — do not miss it if the client has settled any regulatory proceeding during the year.
9. Populate one row per identified item with `Particulars` describing the item and `Amount`.

**Common mistakes:** disallowing compensatory interest along with penal fines (only the penal portion is disallowed); missing small/recurring penalty amounts scattered across many ledger lines (e.g., monthly GST late fees) that add up to a material figure; forgetting the new Explanation 3 settlement category.

---

## Clause 21(b) — Amounts inadmissible under Section 40(a) (TDS-default disallowance)

**Statutory basis:** Section 40(a), sub-clauses (i) through (v) as detailed below.

**Schema fields:** `Form3cdAmtInadm40A` (and its parallel row-groups `Form3cdAmtInadm40A1` through `Form3cdAmtInadm40A6`, all sharing the same row shape — used for the detailed, payee-level sub-clauses) — each row: `{ ParticularType [enum: SUBCLAUSEi, SEC200(1), SUBCLAUSEia, SEC139, SUBCLAUSEib, SEC139B, SUBCLAUSEiii], DateOfPayment, AmtOfPayment, NatureOfPayment, NameOfPayee, AadhaarCardNo, PANOfPayee, AddressDetails, AmtTaxDeducted, AmtTaxDeposited }`. Sub-clause (iii) [salary payable outside India/to a non-resident without TDS] uses the same detailed shape via `Form3cdAmtInadm40ASubClauseiii`. Sub-clauses (ic), (iia), (iib), (iv), (v) are simple aggregate-amount fields with no payee-level breakup required: `Form3cdAmtInadm40ASubClauseiC`, `...iia`, `...iib`, `...iv`, `...v` respectively (each just an integer amount).

### Sub-clause map (verified against the bare Act text)

| Sub-clause | Covers | Disallowance | Schema field |
|---|---|---|---|
| (i)(A) | Interest, royalty, FTS, or other sum chargeable under the Act, payable to a non-resident (not being a company) or a foreign company, outside India or in India, on which TDS was deductible under Chapter XVII-B but was not deducted, or was deducted but not paid on or before the s.139(1) return due date | **100%** disallowed (allowed as deduction in the later year in which tax is actually deducted and/or deposited) | `Form3cdAmtInadm40A` / `40A1` (detailed) |
| (i)(B) | Same category of sum, but payable to a **resident**, where TDS deductible under Chapter XVII-B was not deducted, or was deducted but not paid on or before the s.139(1) return due date | **30%** of the sum disallowed (not 100% — this is the key numerical difference from the non-resident limb; the other 70% remains allowable even if TDS defaulted) | `Form3cdAmtInadm40A2`–`40A6` (detailed) |
| (ib) | Equalisation levy (Chapter VIII, Finance Act 2016 — 6% levy on specified services, chiefly online advertisement, paid to a non-resident without a PE in India) not deducted, or deducted but not deposited by the s.139(1) due date | **100%** of the payment disallowed | `Form3cdAmtInadm40ASubClauseiii`-shape row, or dedicated group per utility |
| (ic) | Fringe Benefit Tax under (erstwhile) Chapter XII-H | **Obsolete — FBT was abolished from AY 2010-11.** This row will essentially always be NIL; flag any non-zero client-provided figure as suspicious and re-verify what it actually represents | `Form3cdAmtInadm40ASubClauseiC` (amount only) |
| (ii) | Income-tax itself paid on business profits (basic non-deductibility of income-tax) | Not separately itemised in Clause 21(b)'s schema row-set (it's a blanket non-deductibility of the tax itself, generally handled directly in the computation sheet rather than as a Clause-21(b) line item) | n/a |
| (iia) | Wealth-tax paid | **Obsolete — Wealth-tax Act was abolished from AY 2016-17.** Will always be NIL | `Form3cdAmtInadm40ASubClauseiia` (amount only) |
| (iib) | Royalty, licence fee, service fee, privilege fee, service charge, or any other fee/charge levied exclusively on, or appropriated from, a **State Government undertaking**, by the State Government | **100%** disallowed | `Form3cdAmtInadm40ASubClauseiib` (amount only) |
| (iii) | Salary payable outside India, or to a non-resident, without TDS deduction/deposit under Chapter XVII-B | **100%** disallowed | `Form3cdAmtInadm40ASubClauseiii` (detailed) |
| (iv) | Payment to a provident or other fund established for employees, UNLESS the employer has made effective arrangements to deduct TDS at source on payments made from the fund that are chargeable as "Salaries" | Disallowed to the extent TDS arrangements are absent | `Form3cdAmtInadm40ASubClauseiv` (amount only) |
| (v) | Tax actually paid by the employer on a non-monetary perquisite provided to an employee, where the employer has borne the tax under Section 10(10CC) (tax-on-tax / grossed-up perquisite arrangement) | The tax so borne by the employer is not deductible | `Form3cdAmtInadm40ASubClausev` (amount only) |

Note: sub-clauses (ic) and (iia) will be NIL for virtually every FY 2025-26 audit since the underlying taxes (FBT, Wealth-tax) no longer exist — do not spend time investigating these unless the client's records show a specific non-zero figure, in which case investigate what it actually is before classifying it here.

### How to determine ParticularType for the detailed rows
- `SUBCLAUSEi` / `SUBCLAUSEia` / `SUBCLAUSEib` — TDS not deducted at all.
- `SEC200(1)` / `SEC139` / `SEC139B` — TDS was deducted but deposited late, i.e. after the due date prescribed under s.200(1)/relevant rule but claim is being tested against the s.139(1) return-filing due date; select the value matching whichever specific late-deposit scenario the utility is asking about for that row.

### Procedure — cross-checking against TDS records
1. Obtain the client's Form 26Q/24Q/27Q TDS returns filed for FY 2025-26 (all four quarters), or at minimum a TDS deduction summary/ledger. **If TDS returns are not available: `[MISSING — REQUEST TDS RETURNS (26Q/24Q/27Q) FROM CLIENT]`** — this clause cannot be reliably completed without them.
2. Pull the trial balance and list every expense ledger that is normally subject to TDS: rent (194-I), professional/technical fees (194J), contractor/sub-contractor payments (194C), commission/brokerage (194H), interest other than on securities (194A), payments to non-residents (195), etc.
3. For each such ledger, compute total expense debited and compare against (a) TDS actually deducted per the 26Q/24Q/27Q returns, and (b) the applicable TDS rate/threshold for that payment type, to identify: no TDS deducted at all; TDS deducted at a lower rate than required (short deduction); TDS deducted correctly but deposited late.
4. For any gap identified, determine payee residential status (resident → 30% disallowance under (i)(B); non-resident/foreign co → 100% disallowance under (i)(A)) and populate the relevant row with payee name, PAN, date of payment, amount, TDS deducted, TDS deposited.
5. Cross-check the client's own Form 26AS/AIS (if available) for any TDS credits reflecting deduction by the client that weren't in the returns provided, as a consistency check.
6. For equalisation levy (ib): check for any payment to a non-resident digital advertising platform (Google, Meta, etc.) without a PE in India, where aggregate payments to that entity exceed Rs. 1 lakh in the year — verify 6% equalisation levy was deducted and deposited by the 7th of the following month (or the specified due date), and that a return in Form 1 was filed.

### Common mistakes
- Applying 100% disallowance to a resident-payee default instead of 30% (or vice-versa for non-resident payees).
- Forgetting that TDS deducted-but-deposited-late is cured (added back is reversed) once actually deposited — in a LATER year, not necessarily in the disallowance year itself; the current-year Form 3CD must still show the disallowance for the year of default if not cured by the s.139(1) due date of that year.
- Missing equalisation levy entirely — it is easy to overlook since it isn't "TDS" in the traditional Chapter XVII-B sense.
- Not distinguishing short-deduction (TDS deducted at a lower rate than mandated — proportionate disallowance) from complete non-deduction.

---

## Clause 21(c) — Interest/salary/bonus/commission/remuneration to a partner disallowed under s.40(b)/40(ba)

**Statutory basis:** Section 40(b) (partnership firms — caps on partner interest and working-partner remuneration), Section 40(ba) (AOPs/BOIs — no deduction at all is allowed for interest, salary, bonus, commission, or remuneration paid to a member, subject to a partial exception for interest where the AOP/BOI itself pays interest to a member and the member also pays interest to the AOP/BOI, in which case only the net excess is disallowed).

**Schema fields:** `Form3cdAmtInadm40AAmtDebit` — array of `{ Particulars [enum: Interest, Salary, Bonus, Commission, Remuneration], Section [enum: 40b, 40ba], AmountDebitPl, AmountAdmisible, AmountInAdmisible, Remarks }`. Also referenced via `Form3cdExpOth` with `ExpenditureType = INTSALBON`, `Particulars` (Salary/Commission/Interest/Remuneration/Bonus), `Section` (Section40b/Section40ba).

### Section 40(b) caps (partnership firms only — LLPs are also treated as firms for this purpose)
1. **Interest to partners**: allowable only if authorised by, and consistent with, the partnership deed, and capped at a **simple interest rate of 12% per annum**. Any interest paid/credited in excess of 12% p.a., even if authorised by the deed at a higher rate, is disallowed to the extent of the excess.
2. **Remuneration (salary/bonus/commission) to WORKING partners only** (remuneration to a non-working/sleeping partner is wholly disallowed under s.40(b), regardless of amount): must be authorised by the partnership deed AND must not exceed the following slab computed on "book profit" (book profit here = net profit per the P&L account, computed under the head "Profits and gains of business or profession" BEFORE deducting partner remuneration itself, but after all other adjustments including depreciation, and after adding back partner remuneration if already debited):
   - On the first Rs. 3,00,000 of book profit (or in case of a loss): **Rs. 1,50,000, or 90% of book profit, whichever is more**;
   - On the balance of book profit: **60%** of the balance.
3. Any remuneration paid in excess of this ceiling, or to a non-working partner, or without deed authorisation, or before the deed authorising it was executed/effective, is disallowed under s.40(b)(v).

### Section 40(ba) (AOP/BOI)
No deduction at all for interest, salary, bonus, commission, or remuneration paid by an AOP/BOI to any member — 100% disallowed, with only the narrow interest-netting exception noted above.

### Procedure
1. Obtain the partnership deed (and any supplementary deeds) — check: (a) is there an explicit clause authorising interest to partners and, if so, at what rate; (b) is there an explicit clause authorising remuneration to working partners and the computation method/cap agreed (the deed's authorised amount cannot exceed the statutory ceiling, but it CAN authorise less than the statutory ceiling, in which case the LOWER of deed-authorised and statute-permitted amount is allowable).
2. Recompute book profit per the s.40(b) Explanation 3 definition (net profit per P&L under "business or profession" head, as adjusted, before deducting remuneration) and apply the slab formula independently — do not simply accept the client's own remuneration figure without recomputing the ceiling.
3. Compare actual interest rate paid/credited per partners' capital/current account ledgers against the 12% cap and against the deed-authorised rate (use the lower of the two).
4. Populate `AmountDebitPl` (per books), `AmountAdmisible` (per the s.40(b) computation), `AmountInAdmisible` (difference) for each of Interest/Remuneration, tagging `Section = 40b` for firms or `40ba` for AOP/BOI as applicable.
5. If the partnership deed is not available: `[MISSING — REQUEST PARTNERSHIP DEED FROM CLIENT]` — do not assume the client's remuneration/interest figures are correctly authorised without seeing the deed.

**Common mistakes:** applying the remuneration slab to total book profit without excluding partner remuneration already debited (circularity error); allowing interest at the deed rate without capping at 12%; allowing remuneration to a partner who is technically a partner in the deed but not actually "working" in the business; missing that book profit for this purpose is computed after depreciation but before remuneration.

---

## Clause 21(d) — Disallowance under Section 40A(3)/40A(3A) (cash payments)

**Statutory basis:** Section 40A(3) (revenue expenditure paid in cash exceeding the threshold, disallowed in the year of expenditure), Section 40A(3A) (where the expenditure was allowed as a deduction on accrual basis in an earlier year, and the actual cash payment discharging that liability in a SUBSEQUENT year exceeds the threshold, the payment amount is deemed to be profits and gains of business/profession chargeable to tax in the year of payment). Rule 6DD prescribes exceptions.

**Schema fields:** `Form3cdIncomeUnderSec40A_3` — array of `{ PaymntSec40A_3A: { DateOfPayment, NatureOfPayment, AmtOfPayment, NameOfPayee, AadhaarCardNo, PANOfPayee } }` — this captures the (B) limb, s.40A(3A) deemed income for subsequent-year cash payment of an earlier-year accrued expense. `ExpendSec40A_3` — array of `{ DateOfPayment, NatureOfPayment, AmtOfPayment, NameOfPayee, AadhaarCardNo, PANOfPayee }` — this captures the (A) limb, current-year cash revenue expenditure disallowed under s.40A(3).

### Threshold
- General threshold: **Rs. 10,000** — any payment (or aggregate of payments) made in cash to a single person **in a single day** exceeding Rs. 10,000, in respect of an expenditure otherwise deductible, is disallowed. (Test is "aggregate of payments to a person in a day", not per-voucher — multiple small cash payments to the same party on the same day that together exceed Rs. 10,000 are equally caught.)
- Higher threshold for goods-carriage transport operators: **Rs. 35,000** — payment for plying, hiring, or leasing goods carriages.

### Rule 6DD exceptions (payment otherwise caught by 40A(3)/40A(3A) is NOT disallowed if it falls under any of these)
(a) Payment to the Reserve Bank of India or any banking company (incl. co-operative bank), the SBI or a subsidiary bank, or a corresponding new bank.
(b) Payment to the Government, where required to be paid in legal tender.
(c) Payment by way of a letter of credit / mail or telegraphic transfer / book adjustment through a bank account / bill of exchange payable to a bank / use of an electronic clearing system / a credit card / debit card / other prescribed electronic mode, or a bank draft/pay order where the banking system was used (i.e., genuinely NOT cash at all — this exception is really the "non-cash mode" carve-out).
(d) Payment to the Reserve Bank / co-operative land mortgage bank / land development bank / primary agricultural credit society.
(e) Payment made by an assessee, by way of adjustment, against a liability incurred by the assessee for goods supplied or services rendered by the payee to the assessee (book adjustment scenarios involving commission agents / kutcha arahtias handling produce on the assessee's behalf).
(f) Payment made for the purchase of agricultural or forest produce, or produce of animal husbandry (including livestock, meat, hides, skins) or dairy/poultry farming, or fish/fish products, or products of horticulture/apiculture, to the cultivator/grower/producer of such produce (i.e., direct purchase from the primary producer, no intermediary process beyond what a cultivator/grower ordinarily performs).
(g) Payment for the purchase of products manufactured/processed without the aid of power in a cottage industry, made to the producer of such products.
(h) Payment made in a village or town which, on the date of payment, is not served by any bank, to a person who resides, or carries on business/profession/vocation, in that village or town.
(i) Payment of terminal benefits (retirement/retrenchment/resignation/death benefits, gratuity, retrenchment compensation) to an employee or their heirs, where the aggregate does not exceed Rs. 50,000.
(j) Salary payment to an employee, after deducting tax at source, where the employee is temporarily posted for a continuous period of 15 days or more at a place other than their normal place of duty or on a ship, and does not maintain a bank account at that place.
(k) Payment made on a day on which the banks were closed either due to a holiday or a strike.
(l) Payment made by any person to their agent, who is required to make payment in cash for goods/services on the person's behalf.
(m) Payment made by an authorised dealer or money-changer for the purchase of foreign currency or travellers cheques in the normal course of business.
Additional relief: certain payments made through banking channels rendered impossible by exceptional circumstances (e.g., banking disruption in specified areas) have historically been notified — confirm if any such notification applies before relying on it.

### Procedure
1. Obtain the cash book / petty cash ledger and bank payment vouchers for the year.
2. Scan for any single-day cash payment exceeding Rs. 10,000 (Rs. 35,000 for goods-transport operators) to a single party. Aggregate multiple same-day cash payments to the same party before testing the threshold.
3. For each flagged payment, check whether a Rule 6DD exception applies (most common in practice: agricultural produce purchase from farmers, payment in an unbanked village, or payment to a legal heir/terminal benefit within the Rs. 50,000 cap). If an exception applies, do not disallow — but document which exception and why `[JUDGMENT CALL — CA TO CONFIRM]`.
4. For payments where the underlying expense was accrued/expensed in a PRIOR year (i.e., it was a creditor/payable brought forward) and settled in cash THIS year above the threshold, route this to the 40A(3A) / `Form3cdIncomeUnderSec40A_3` array (deemed profit in the year of payment) rather than the 40A(3) array — check the creditor ageing/ledger to confirm the liability's origin year.
5. For payments where the expense itself was incurred AND paid in cash THIS year above the threshold, route to `ExpendSec40A_3` (straightforward 40A(3) disallowance).
6. Populate `DateOfPayment`, `NatureOfPayment`, `AmtOfPayment`, `NameOfPayee`, `PANOfPayee` for each disallowed item.

**Common mistakes:** testing threshold per-voucher instead of aggregating same-day same-payee payments; disallowing cash purchases of agricultural produce from farmers (a common and legitimate exception); missing the 40A(3A) subsequent-year-payment limb entirely (staff often only check current-year cash expenditure and forget to check whether any OLD outstanding creditor was paid off in cash this year); applying the Rs. 10,000 threshold to transport operators instead of the correct Rs. 35,000.

---

## Clause 21(e) — Provision for gratuity disallowed under Section 40A(7)

**Statutory basis:** Section 40A(7) — no deduction is allowed for any provision made by the assessee for the payment of gratuity to employees on retirement/termination, EXCEPT: (a) provision made for a contribution to an approved gratuity fund, or (b) provision made for gratuity that has actually become payable during the year (i.e., an ascertained, crystallised liability, not a general reserve/actuarial provision for future contingent gratuity).

**Schema fields:** part of `Form3cdExpOth` with `ExpenditureType = GRATSEC40A7` (Particulars/Section/Amount/Details as applicable).

### Procedure
1. Obtain the gratuity provision/actuarial valuation report (AS-15/Ind AS-19) and the P&L gratuity expense line.
2. Determine whether the client maintains an **approved gratuity fund** (a fund approved by the jurisdictional CIT/PCIT under Part C of the Fourth Schedule) and whether the provision debited to P&L represents an actual contribution paid/payable into that approved fund. If yes, it is allowable (subject also to Section 43B — see Clause 26).
3. If the client does NOT have an approved gratuity fund, and the amount debited is a general actuarial provision for future gratuity liability (not gratuity actually paid or become payable to specific employees who exited during the year), the ENTIRE provision is disallowed under s.40A(7), irrespective of its accuracy as an accounting estimate.
4. If gratuity was actually paid out during the year to retiring/exiting employees (an ascertained, crystallised payment), that specific paid amount is allowable even without an approved fund.
5. Reconcile: (opening provision + current year charge − amount actually paid during the year) = closing provision; only the "actually paid" or "approved-fund-contribution" component is allowable; the balance of the P&L charge (representing the unfunded actuarial increase in provision) is disallowed.

**Common mistakes:** allowing the full actuarial gratuity expense (P&L charge) without checking whether it corresponds to actual payments or approved-fund contributions; not distinguishing the funded vs unfunded portion of the provision.

---

## Clause 21(f) — Disallowance under Section 40A(9)

**Statutory basis:** Section 40A(9) — no deduction is allowed for any sum paid by the assessee, as an employer, towards the setting up or formation of, or as a contribution to, any fund, trust, company, AOP, BOI, society, or other institution for any purpose, EXCEPT where such sum is paid towards a recognised provident fund, approved superannuation fund, approved gratuity fund, or any other fund set up under a specific statutory obligation on the employer (e.g. ESI).

**Schema fields:** part of `Form3cdExpOth` with `ExpenditureType = SUMSEC409` (i.e., "sum under s.40A(9)").

### Procedure
1. Scan the P&L for any employer contribution/payment to a "welfare trust", "employee welfare fund", "staff benefit fund", or similar non-statutory vehicle that is NOT one of: recognised PF, approved superannuation fund, approved gratuity fund, ESI, or another fund the employer is statutorily obligated to contribute to.
2. Any such payment is fully disallowed under s.40A(9), regardless of its bona fide welfare purpose — the section is a blanket disallowance for non-statutory/unapproved employee welfare vehicles.
3. Cross-check against Clause 20(b)/26(b) fund contributions to avoid double-counting — statutory PF/ESI/superannuation/approved-gratuity contributions belong there, not here; this clause is specifically for the residual, non-statutory category.

**Common mistakes:** disallowing legitimate statutory PF/ESI/superannuation contributions under this clause by mistake (they belong under s.36(1)(va)/43B instead); missing payments to informally-run "employee welfare trusts" that are common in family-owned businesses.

---

## Clause 21(g) — Contingent liabilities debited to P&L

**Statutory basis:** general principle under Section 37(1)/business income computation — only an ascertained (crystallised, quantifiable, present) liability is deductible; a contingent liability (one dependent on the happening or non-happening of a future uncertain event, e.g. a pending litigation claim, a disputed demand not yet finally adjudicated, a general provision for anticipated future losses) is not an allowable deduction merely because it is debited to the P&L and disclosed in the notes to accounts.

**Schema fields:** part of `Form3cdExpOth` with `ExpenditureType = CONTGNTNAT`.

### Procedure
1. Obtain the notes to accounts / contingent liabilities disclosure (AS-29/Ind AS-37 "Provisions, Contingent Liabilities and Contingent Assets" note) — most audited financial statements carry a dedicated contingent liability note (pending litigation, guarantees given, disputed tax demands, etc.).
2. Distinguish: (a) a **provision** for a liability that is present and reasonably estimable (e.g. warranty provision based on historical claim experience, provision for a known, quantified but not-yet-paid statutory demand that the company accepts is payable) — this is an ascertained liability and generally allowable if it otherwise meets s.37(1) tests; vs (b) a **contingent liability** — a possible obligation depending on an uncertain future event not wholly within the entity's control (e.g., a pending court case where liability is disputed and not admitted, a guarantee given on behalf of a third party not yet invoked) — this is NOT deductible even if a corresponding amount was debited to the P&L as a "provision".
3. Only amounts actually **debited to the P&L account** (reducing the reported profit) for a contingent liability need to be picked up here — pure balance-sheet/notes-only disclosures with no P&L debit don't create a Clause 21(g) item.
4. `[JUDGMENT CALL — CA TO CONFIRM]` is appropriate for borderline provisions (e.g. a provision for a disputed tax demand where the company has strong grounds to contest but has nonetheless provided for it conservatively) — the classification of "ascertained" vs "contingent" is often genuinely debatable and should be flagged for the CA's sign-off rather than auto-decided.

**Common mistakes:** disallowing legitimate, ascertained provisions (e.g. warranty, bad-debt provision — bad debt provisions have their own separate tax treatment under s.36(1)(vii)/(viia) and are not automatically "contingent") purely because they are estimates; missing a genuinely contingent litigation provision buried in "other expenses" or "exceptional items".

---

## Clause 21(h) — Disallowance under Section 14A (expenditure relating to exempt income)

**Statutory basis:** Section 14A — no deduction is allowed for expenditure incurred by the assessee in relation to income that does not form part of total income (exempt income). Computed per Rule 8D if the assessee has not made a reasonable suo-moto disallowance itself. Rule 8D(2) (post-2016 simplified formula) = (i) the amount of expenditure directly relatable to exempt income, PLUS (ii) 1% of the annual average of the monthly average of the opening and closing values of investments whose income is exempt (this replaced the older, more complex interest-apportionment formula). **Important recent point**: Finance Act 2022 inserted an Explanation to Section 14A clarifying, with effect from AY 2022-23, that the provisions of Section 14A apply even in a year where the assessee has NOT earned any exempt income at all — this overturned the earlier judicial position (Cheminvest, Chettinad Logistics, etc.) that no disallowance arises absent actual exempt income in the year. Do not rely on the old "no exempt income, no 14A disallowance" case law for FY 2025-26.

**Schema fields:** part of `Form3cdExpOth` with `ExpenditureType = DEDUCSEC14A`.

### Procedure
1. Identify all exempt income earned by the client during the year — for most business assessees today, actual candidates are narrow since dividend income is now taxable (post AY 2021-22 abolition of the dividend exemption). Look for: agricultural income, PPF interest, specified LTCG/other income genuinely exempt under Chapter III (Sections 10 etc.), share of profit received by a partner from a partnership firm (exempt in the partner's hands under s.10(2A)), interest on tax-free bonds.
2. Even if no exempt income was earned this year, confirm whether the client holds investments capable of yielding exempt income (e.g., investment in a partnership firm, tax-free bonds) — post the Finance Act 2022 Explanation, a s.14A disallowance can still arise based on such holdings even without actual exempt income this year; flag this scenario `[JUDGMENT CALL — CA TO CONFIRM]` since it is a genuinely debatable, litigated area.
3. If exempt income (or exempt-income-capable investments) exist, check whether the client has made a suo-moto disallowance in its own computation. If yes and it appears reasonable, generally accept it; if no suo-moto disallowance has been made, compute per Rule 8D(2): direct expenses (if any interest-bearing funds were traceably used to acquire the exempt-income investment) + 1% of average investment value (opening + closing monthly average) yielding exempt income.
4. The disallowance under s.14A cannot exceed the total expenditure actually claimed by the assessee (recent judicial guidance restricts the disallowance to actual expenditure debited, not an artificial figure exceeding total expenses).

**Common mistakes:** ignoring this clause entirely because "no exempt income was earned" (no longer sufficient post Finance Act 2022 for years from AY 2022-23); applying the old, more punitive pre-2016 Rule 8D formula (interest apportionment) instead of the current simplified 1%-of-average-investment formula; not checking partner's share of firm profit as an exempt-income category.

---

## Clause 21(i) — Disallowance under proviso to Section 36(1)(iii)

**Statutory basis:** proviso to Section 36(1)(iii) — interest paid on capital borrowed for acquisition of an asset (whether capitalised in the books or not) for extension of the existing business or profession, for the period from the date of borrowing until the date the asset is first put to use, must be capitalised (added to the cost of the asset) and is NOT allowable as a revenue deduction for that pre-put-to-use period, even if the borrowing itself is otherwise for business purposes and even if the funds are commingled with general working capital.

**Schema fields:** part of `Form3cdExpOth` with `ExpenditureType = AMTINADMSEC36I`.

### Procedure
1. Identify any capital asset acquired/constructed during the year (or continuing from a prior year) that was funded, wholly or partly, by borrowed capital, where the asset represents an EXTENSION of the existing business (a new plant, a new unit, a new capital project) — note this proviso targets extension/expansion capex specifically, distinguishing it from ordinary working-capital-funded revenue expenditure.
2. Determine the date the borrowing was drawn down and the date the asset was first put to use (commissioning date, same date used for the Clause 18 180-day test).
3. Compute interest attributable to that borrowing for the period from draw-down to put-to-use date. If the borrowing is a term loan specifically for the asset, this is straightforward (loan-specific interest for the period). If funds are commingled (general-purpose working capital/cash credit funding a capital project alongside regular operations), apportionment of interest to the capital project is a `[JUDGMENT CALL — CA TO CONFIRM]` — a common reasonable method is proportionate allocation based on the capital-work-in-progress balance funded by borrowed funds versus own funds, but this needs the CA's confirmation of methodology.
4. Confirm whether the client has ALREADY capitalised this interest in the books (many clients under AS 16/Ind AS 23 "Borrowing Costs" already capitalise such interest as a matter of accounting policy — in which case there is no P&L debit to disallow, and this clause is NIL) or has expensed it to the P&L despite the tax law requiring capitalisation (in which case it must be added back here).
5. This clause is about interest for asset ACQUISITION for BUSINESS EXTENSION — routine working capital interest, or interest on loans for replacement/maintenance capex (not an "extension"), is not covered.

**Common mistakes:** disallowing all capex-period interest without checking if it was already capitalised under AS 16/Ind AS 23 (double-counting risk — if already capitalised in the books, it flows through as depreciation, not as a direct P&L debit, and shouldn't be separately added back here); missing the "extension of existing business" qualifier and over-applying this to ordinary replacement asset purchases.

---

## Clause 22 — Interest inadmissible under Section 23 of the MSMED Act, 2006

**Statutory basis:** Section 16 of the Micro, Small and Medium Enterprises Development Act, 2006 (compound interest, with monthly rests, at three times the RBI-notified bank rate, payable by a buyer who fails to pay a micro or small enterprise supplier within the time limit under Section 15) read with **Section 23 of the MSMED Act, 2006**, which provides that "notwithstanding anything contained in the Income-tax Act, 1961, the amount of interest payable or paid by any buyer... shall not, for the purposes of computation of income under the Income-tax Act, 1961, be allowed as deduction."

**IMPORTANT SCOPE NOTE — do not confuse with Clause 26(h)**: This Clause 22 is ONLY about the **interest** component levied under Section 16 of the MSMED Act for delayed payment to a micro/small enterprise supplier. The separate, newer disallowance of the **principal** amount payable to a micro/small enterprise beyond the Section 15 time limit — introduced by Finance Act 2023 as Section 43B(h) of the Income-tax Act — is reported under **Clause 26**, not here. A single instance of a delayed MSME payment can therefore generate TWO separate Form 3CD entries: the interest portion under Clause 22 (s.23 MSMED Act, always 100% disallowed, no due-date relief, applies from the year the interest itself is levied/accrued) and the principal portion under Clause 26(h) (s.43B(h) Income-tax Act, disallowed only if unpaid beyond the time limit at year-end, subject to the special no-grace-period rule described in Clause 26 below).

**Schema fields:** `Form3cdInadm` — array of `{ ParticularType [pattern: SEC69D | SEC23], Particulars, Amount1, Amount2, Amount3, Amount4 }`. For this clause, filter/use rows with `ParticularType = SEC23` only (`SEC69D` rows in the same array relate to Section 69D hundi borrowings, which is a different clause outside this file's scope — do not populate SEC69D rows here).

### Section 15/16 mechanics (MSMED Act, 2006)
- **Section 15**: the buyer must pay a micro or small enterprise supplier for goods/services within the period agreed in writing (which cannot exceed 45 days from the date of acceptance/deemed acceptance of the goods or services), or, if there is no written agreement, within 15 days.
- **Section 16**: on failure to pay by the Section 15 due date, the buyer is liable to pay compound interest with monthly rests, at **three times the RBI-notified bank rate**, on the amount outstanding, from the appointed day (the Section 15 due date) until the date of actual payment.
- **Section 23**: this Section-16 interest — whether actually paid or merely payable — is **never deductible** for income-tax purposes, overriding anything else in the Income-tax Act. This is a blanket, unconditional disallowance; there is no exception for interest actually paid during the year (unlike ordinary Section 43B logic, which is oriented toward payment curing the disallowance — here the interest itself is disallowed by law regardless of payment).

### Procedure
1. Obtain the client's trade payables ledger/ageing and identify which suppliers are registered as Micro or Small Enterprises under the Udyam Registration scheme — request Udyam Registration certificates from the client for its key suppliers, or check GSTR-2B/purchase register for any supplier who has self-declared MSME/Udyam status on their invoices (many MSME-registered suppliers print their Udyam number on the invoice).
2. **Traders are excluded**: per Ministry of MSME Office Memorandum dated 1 September 2021, retail and wholesale trade enterprises registered under Udyam are excluded from the Section 15/16 delayed-payment protection (their Udyam benefits are restricted to priority-sector lending only) — even if a supplier holds a Udyam certificate, check whether its registered activity is "trading"; if so, MSMED Act interest/Section 43B(h) implications do NOT apply to that supplier `[JUDGMENT CALL — CA TO CONFIRM]`.
3. **Registration timing matters**: the supplier must have been registered as a Micro or Small enterprise under Udyam ON THE DATE OF THE TRANSACTION (date of supply) for Section 15/16 to apply to that transaction — a supplier who registers only later in the year does not retrospectively trigger MSMED protection for earlier-year transactions with that supplier. Confirm registration date against transaction date for each supplier flagged.
4. For each identified Micro/Small supplier (non-trader, registered as of the transaction date), compute the payment due date under Section 15 (per any written agreement, capped at 45 days, else 15 days from acceptance) and compare to the actual payment date.
5. Where payment was delayed beyond the Section 15 due date, compute compound interest (with monthly rests) at 3× the RBI-notified bank rate on the overdue amount for the delay period. This computation is genuinely intricate (monthly compounding) — if a precise computation isn't feasible from available data, present the best-effort calculation and flag `[JUDGMENT CALL — CA TO CONFIRM]`, or if the RBI bank rate for the relevant period isn't available, `[MISSING — CONFIRM WITH CLIENT / VERIFY CURRENT RBI BANK RATE]`.
6. Populate `Particulars` (supplier name/description) with `ParticularType = SEC23`; use the four amount columns to capture, per the return utility's actual on-screen labels, components such as principal outstanding, interest period, applicable rate, and computed interest amount disallowed — verify the exact column labels in the live filing utility since the raw schema does not itself label `Amount1`–`Amount4`.
7. Whether or not this Section 16 interest was actually accrued/booked in the P&L, if it is legally payable (even if the supplier hasn't invoked it or the client hasn't provided for it), technically it should be recognised and disallowed — in practice, materiality and the client's own books/awareness of the liability will drive how deep to dig; note any unprovided contingent MSMED interest exposure `[JUDGMENT CALL — CA TO CONFIRM]`.

### Common mistakes
- Confusing this clause with Section 43B(h) (Clause 26) — remember: Clause 22 = interest under MSMED s.23; Clause 26(h) = principal under Income-tax s.43B(h).
- Treating all "small" suppliers as MSME without checking actual Udyam registration.
- Applying MSMED protection to trader/wholesaler suppliers (excluded per the 2021 OM).
- Checking registration status as of today rather than as of the transaction date.
- Missing that this interest disallowance applies even to interest that is merely payable/accrued, not just interest actually paid.

---

## Clause 23 — Payments to persons specified under Section 40A(2)(b) (related parties)

**Statutory basis:** Section 40A(2) — where the assessee incurs any expenditure for which payment has been or is to be made to a "specified person" under s.40A(2)(b) (broadly: relatives of an individual assessee; directors of a company and their relatives; partners of a firm and their relatives; any individual having a substantial interest in the business (beneficial owner of ≥20% of equity/voting power/profit share) and their relatives; any company, firm, AOP, or HUF having a substantial interest in the assessee's business, and their directors/partners/members and relatives; any company of which a director has a substantial interest in the assessee's business; and entities under common substantial-interest control), and the Assessing Officer is of the opinion that such expenditure is excessive or unreasonable having regard to the fair market value of the goods/services/facilities, or the legitimate business needs, the excessive/unreasonable portion may be disallowed.

**Important distinction**: Clause 23 itself is purely a **disclosure clause** — it requires listing ALL payments made to specified persons during the year, regardless of whether they are reasonable or not. The actual disallowance of any excessive/unreasonable portion under s.40A(2) is a separate substantive determination (and, if made, would itself appear as a P&L addback elsewhere in the computation) — do not conflate "must be disclosed here" with "must be disallowed here."

**Schema fields:** `Form3cdPymtSec40a2bDetail` — array of `{ RelatedParyName, RelatedParyType, Amount, RelatedPAN, AadhaarCardNo, NatureOfTrnsc }`.

### Procedure
1. Obtain the related-party disclosure note from the audited financial statements (AS-18 "Related Party Disclosures" for non-Ind-AS entities, or Ind AS-24 for Ind-AS entities) — this note lists related parties and the nature/quantum of transactions with each, and is the natural starting checklist.
2. Cross-reference the AS-18/Ind AS-24 related-party list against the s.40A(2)(b) "specified person" definition — note these two lists are NOT identical (AS-18/Ind AS-24 has its own, broader accounting definition of "related party," e.g. it includes key management personnel more broadly and entities under common control in ways that may or may not align exactly with s.40A(2)(b)'s tax definition). Filter to only those related parties who also meet the tax-law "specified person" test.
3. For each qualifying specified person, pull the actual payment/transaction amounts from the trial balance/ledger for the year (the AS-18/Ind AS-24 note may only disclose a subset or a rounded/aggregated figure — verify against the ledger for the precise amount).
4. Populate one row per specified person per nature of transaction: `RelatedParyName`, `RelatedParyType` (e.g. "Director", "Relative of Director", "Partner", "Entity with substantial interest"), `Amount`, `RelatedPAN`, `NatureOfTrnsc` (e.g. "Rent paid", "Salary/remuneration", "Purchase of goods", "Professional fees", "Interest paid", "Loan given/taken").
5. Include ALL such payments regardless of amount or apparent reasonableness — this is a disclosure clause, so under-reporting on the basis that "the amount looked reasonable" is itself a compliance failure.
6. Separately (outside Clause 23 itself, but flag for the CA), assess whether any of the disclosed payments appear excessive relative to fair market value or business need — `[JUDGMENT CALL — CA TO CONFIRM]` on whether a s.40A(2) disallowance should additionally be proposed in the computation.

**Common mistakes:** relying solely on the AS-18/Ind AS-24 note without independently verifying amounts against the ledger; omitting related-party loans/advances (not just expense payments) — the disclosure covers "any expenditure," which should be read to include payments for goods, services, assets, and financing arrangements with specified persons, not just routine revenue expenses; missing relatives of directors/partners (the definition extends beyond the director/partner themselves).

---

## Clause 24 — Amounts deemed to be profits and gains under Section 32AC/32AD/33AB/33ABA

**Statutory basis:** Section 32AC (investment allowance — 15% deduction for new plant & machinery acquired and installed by a manufacturing company within specified windows, now a sunset provision for older years but the CLAWBACK remains relevant: if such P&M is sold/transferred within 5 years of installation, other than on amalgamation/demerger/reorganisation, the investment allowance earlier claimed is treated as deemed business income in the year of sale), Section 32AD (similar investment allowance clawback for undertakings in notified backward areas of Andhra Pradesh/Bihar/Telangana/West Bengal), Section 33AB(7)/(8) and Section 33ABA(6)/(7) (deemed income where amount withdrawn from the special Tea/Coffee/Rubber Development Account or Site Restoration Fund is utilised for a non-specified purpose, or the scheme conditions are otherwise violated, or the business is closed/converted — the withdrawn amount, or the amount misutilised, is treated as deemed profits of the year of withdrawal).

**Schema fields:** `Form3cdProfGainsTax` — array of `{ SectionNo [pattern: 32AC | 32AD | 33AB | 33ABA | 33AC], NameOfParty, Description, Amount }`. Note the schema also includes `33AC` (a legacy, largely historical shipping-business reserve deduction for government shipping companies) — include only if genuinely applicable, which will be exceedingly rare.

### Procedure
1. This clause is relevant ONLY if the client (or a predecessor whose claims carry forward) claimed an investment allowance under s.32AC/32AD in an earlier year (these are old provisions, generally relevant to plant & machinery acquired in FY 2013-14 to FY 2017-18 windows), or has an active Tea/Coffee/Rubber Development Account (s.33AB) or Site Restoration Fund (s.33ABA) with withdrawals during the year.
2. **32AC/32AD clawback test**: check the Fixed Asset Register/Clause-18 deletions for any plant & machinery sold/transferred during FY 2025-26 that was originally acquired and installed within 5 years and formed the basis of an earlier s.32AC/32AD investment allowance claim. If found, the earlier-claimed investment allowance amount attributable to that specific asset becomes deemed business income this year. Cross-reference the earlier year's ITR/tax computation for the exact allowance claimed on that specific asset. `[MISSING — CONFIRM WITH CLIENT / REQUEST EARLIER YEAR COMPUTATION]` if the original claim amount can't be traced.
3. **33AB/33ABA test**: check the Tea/Coffee/Rubber Development Account or Site Restoration Fund passbook/statement for any withdrawal during the year, and confirm from the client whether the withdrawn amount was applied strictly for the scheme-specified purpose (as per the relevant scheme rules). Any withdrawal not so applied, or applied for prohibited purposes (e.g., distribution as dividend/profit, or for a purpose outside the approved scheme), or triggered by closure/discontinuance of business, is deemed income in the year of withdrawal.
4. For virtually all typical SME/service/trading clients, this clause will be **NIL** — these are narrow, industry-specific, sunset-window provisions. Do not populate a row unless there is clear evidence of an underlying earlier-year claim.

---

## Clause 25 — Profit chargeable to tax under Section 41

**Statutory basis:** Section 41, sub-sections (1) through (5):
- **s.41(1)(a)** — remission or cessation of a trading liability by the assessee itself: where a deduction has been allowed in any earlier year in respect of a trading liability (a purchase, an expense, a loss), and during the current year the assessee has obtained, by way of remission or cessation, any benefit in respect of that liability (e.g., a creditor writes off the balance, a liability becomes time-barred/statute-barred and is written back, a loan/liability waiver) — the amount obtained (or the value of the benefit) is deemed profits and chargeable to tax in the year of remission/cessation, whether or not the business/profession in respect of which the allowance was made continues.
- **s.41(1)(b)** — same as above, but where the benefit is obtained by a **successor** to the business (e.g. on business reorganisation/succession) rather than the original assessee.
- **s.41(2)** — balancing charge on transfer of assets of an undertaking engaged in generation/generation-and-distribution of power, where such undertaking uses the SLM method (moneys payable on transfer, to the extent it exceeds WDV, is deemed profit, capped at the difference between original cost and WDV).
- **s.41(3)** — sale, discarding, demolition, or destruction of a capital asset that was used for scientific research (for which a full deduction was earlier allowed under s.35(1)(iv)/35(2)) — the sale proceeds (to the extent of the aggregate of the earlier deduction and any earlier capital-nature deduction, less the actual cost) are deemed profits of the year of sale.
- **s.41(4)** — recovery of a bad debt that was earlier allowed as a deduction under s.36(1)(vii) — the amount recovered, to the extent it exceeds the difference between the debt and the amount allowed as deduction, is deemed profit of the year of recovery.
- **s.41(4A)** — amount withdrawn from a special reserve created and maintained under s.36(1)(viii) (special reserve for long-term finance provided by specified financial corporations/institutions) is deemed income of the year of withdrawal.
- **s.41(5)** — where a business/profession has been discontinued and, in a later year, a deemed s.41 profit arises in respect of that discontinued business, any loss (other than a speculation loss) of that discontinued business which arose in the year of discontinuance and could not be set off (and would otherwise have lapsed) can be set off against such deemed income.

**Schema fields:** `Form3cdProfGainsTaxSec41` — array of `{ NameOfParty, Amount1, Amount2, Amount, SectionNo [pattern: SEC411a | SEC411b | SEC412 | SEC413 | SEC414 | SEC41a | SEC415], Description, Computation }`. (Mapping: `SEC411a` = s.41(1)(a); `SEC411b` = s.41(1)(b); `SEC412` = s.41(2); `SEC413` = s.41(3); `SEC414` = s.41(4); `SEC41a` = s.41(4A); `SEC415` = s.41(5).)

### Procedure
1. Scan the P&L "Other Income" / "Exceptional Items" section for credit entries such as: "liabilities/balances written back", "sundry balances written back", "creditors written off", "excess provision written back" (only the portion relating to an ORIGINALLY-DEDUCTED trading liability counts — a write-back of a provision that was never claimed as a deduction, e.g. a provision that was itself disallowed/added-back in the year it was created, is not s.41(1) income since there's no "benefit obtained in respect of a loss/expenditure/trading liability earlier allowed"), and "bad debts recovered".
2. For each such credit, trace back to confirm the ORIGINAL liability/expense/bad-debt write-off was actually claimed as a tax deduction in an earlier year (check the prior year's tax computation/Form 3CD if available). If the original expense was never claimed as a deduction (e.g., it was capitalised, or was itself disallowed in the earlier computation), the write-back this year is NOT taxable under s.41(1) even though it is credited to the P&L as income (it may still be includible under general income principles depending on facts — flag for CA review) `[JUDGMENT CALL — CA TO CONFIRM]`.
3. For bad debts recovered (s.41(4)): confirm the bad debt write-off was claimed as a deduction under s.36(1)(vii) in an earlier year; if the debt was never claimed as a deduction (e.g., only a provision was made and never actually written off/claimed), s.41(4) does not apply to the recovery.
4. Populate `NameOfParty` (creditor/debtor whose liability ceased or debt was recovered), `Description`, `Computation` (brief working showing the earlier-year deduction traced to this year's recovery/write-back), and `Amount`.
5. If the prior year's tax computation is not available to confirm the earlier deduction was actually claimed: `[MISSING — CONFIRM WITH CLIENT / REQUEST PRIOR YEAR TAX COMPUTATION]` rather than assuming the earlier claim.

**Common mistakes:** taxing every "liability written back" credit under s.41(1) without confirming the underlying expense was originally deductible; missing that a statute-barred debt becoming irrecoverable-to-the-creditor still counts as "cessation" even without a formal waiver document; confusing a straightforward income credit (e.g., a genuine new income item mislabelled as "written back") with a true s.41 remission.

---

## Clause 26 — Sums referred to in Section 43B (allowed only on actual payment)

**Statutory basis:** Section 43B — notwithstanding the method of accounting followed, a deduction for any of the categories listed below is allowed ONLY in the year of actual payment (not on accrual), subject to the proviso that if the sum is actually paid on or before the due date for furnishing the return of income under s.139(1) for that year, it is deemed to have been paid in the relevant previous year and is allowable in the accrual year itself — this is the standard "43B relief." **Section 43B(h), inserted by the Finance Act 2023 with effect from AY 2024-25, is the one exception to this due-date relief — see below.**

**Schema fields:** `Form3cdUnpaidStrySec43b` — array of `{ LiabilityType [pattern: PDPY | NPDPY | PBDD | NPBDD | TAX], Section [enum: 43Ba, 43Bb, 43Bc, 43Bd, 43Bda, 43Be, 43Bf, 43Bg, 43B, 43Bh], Description, Amount }`. `LiabilityType` distinguishes: pre-existing liability (brought forward from an earlier year's disallowance) that was Paid During the Previous Year (`PDPY`) vs Not Paid During the Previous Year (`NPDPY`); and current-year liability Paid By the Due Date (`PBDD`) vs Not Paid By the Due Date (`NPBDD`); `TAX` is used where the row specifically represents a tax/duty/cess/fee category. Confirm the exact selector required against the live filing utility's on-screen labels — the schema alone doesn't narrate the UI wording, so cross-check the utility when populating.

### Category-by-category table

| Section (schema code) | Category | Notes |
|---|---|---|
| 43B(a) → `43Ba` | Any tax, duty, cess, or fee (GST, excise, customs, municipal/property tax, professional tax, any other statutory levy under any law) | Very common — check GST payable/output-input netting, TDS/TCS payable if the assessee itself owes tax as a deductor's own liability doesn't apply here (this is about the assessee's OWN tax/duty/fee liability), municipal tax, etc. |
| 43B(b) → `43Bb` | Employer's contribution to PF, superannuation fund, gratuity fund, or any other fund for employee welfare | **This is the EMPLOYER's own share only** — do not confuse with Clause 20(b)'s employee's-share analysis (s.36(1)(va), no due-date relief). The employer's own PF/ESI/superannuation contribution DOES get the standard 43B due-date relief (allowable if paid before the s.139(1) return due date even if paid after year-end). |
| 43B(c) → `43Bc` | Bonus or commission payable to employees (for services rendered — as distinct from the s.36(1)(ii) profit-substitution issue in Clause 20(a), which is a different test) | Check statutory bonus payable under the Payment of Bonus Act, and any other accrued-but-unpaid bonus/commission at year-end |
| 43B(d) → `43Bd` | Interest on any loan or borrowing from a public financial institution (e.g. IFCI, ICICI-erstwhile, SIDBI as specified) or a State Financial Corporation or State Industrial Investment Corporation | |
| 43B(da) → `43Bda` | Interest on any loan or borrowing from a deposit-taking NBFC, or a systemically important non-deposit-taking NBFC (as notified by RBI) | Added by Finance Act 2019 — relevant wherever the client has NBFC borrowings; verify the specific NBFC's classification (deposit-taking, or systemically important ND-NBFC with asset size above the RBI threshold) if uncertain, flag `[JUDGMENT CALL — CA TO CONFIRM]` |
| 43B(e) → `43Be` | Interest on any loan or advance from a scheduled bank, or a co-operative bank other than a primary agricultural credit society or a primary co-operative agricultural and rural development bank | Very common — most business loan/cash-credit/overdraft interest falls here |
| 43B(f) → `43Bf` | Any sum payable by the employer in lieu of leave earned by employees (leave encashment) | |
| 43B(g) → `43Bg` | Any sum payable to the Indian Railways for the use of railway assets | Rare — relevant mainly to logistics/manufacturing clients with siding/wagon arrangements |
| 43B(h) → `43Bh` | Any sum payable to a micro or small enterprise, beyond the time limit specified in Section 15 of the MSMED Act, 2006 | **See special rule below — this is the newest and most commonly mishandled category.** |

### Procedure (general, categories (a)–(g))
1. For each category, obtain the relevant statutory liability ledger (GST payable, PF/ESI payable, bonus payable, interest accrued on term loans/NBFC loans/bank loans, leave encashment provision) and the corresponding payment challans/bank statements.
2. Determine, for the amount outstanding as at the START of the year (i.e., last year's closing unpaid balance, which would have been disallowed in the prior year's return): was it paid during FY 2025-26? If yes, it becomes allowable THIS year (regardless of when in the year it was paid) — this is the "(a) pre-existing liability" limb of Clause 26. If still unpaid at 31 March 2026, it remains disallowed and carries forward again.
3. For the liability newly ACCRUED during FY 2025-26 (i.e., current year's P&L charge for that category): was it paid by 31 March 2026? If yes, no issue — already paid within the year. If unpaid at year-end, was it paid on or before the s.139(1) return due date (the standard 43B relief window)? If yes, it remains allowable for FY 2025-26 (deemed paid in the relevant year) — but it must still be disclosed in this clause showing the payment-before-due-date fact pattern. If still unpaid even by the return due date, it is disallowed for FY 2025-26 and becomes next year's "pre-existing liability not paid" carry-forward.
4. Populate `Section`, `LiabilityType`, `Description` (nature of the liability, e.g. "GST payable for March 2026", "Employer PF contribution for Feb-Mar 2026"), `Amount`.

### Section 43B(h) — the special MSME principal-payment rule (read carefully; materially different from (a)–(g))

1. **What it covers**: the PRINCIPAL amount payable to a supplier who is a **Micro or Small enterprise** (not Medium — Medium enterprises are excluded), registered under the **Udyam Registration** portal as such, for goods supplied or services rendered, where payment remains outstanding beyond the time limit under Section 15 of the MSMED Act (45 days if there is a written agreement, else 15 days from acceptance).
2. **No due-date-of-return relief for this category** — this is the critical, materially different rule. Unlike categories (a) through (g), where payment any time up to the s.139(1) return filing due date cures the disallowance, **Section 43B(h) explicitly carves itself out of the standard proviso** ("the proviso to this section shall not apply to such payments" — read the exact statutory language rather than assuming standard 43B relief applies). If the amount is not paid to the MSME supplier by 31 March 2026 (the previous year's close), it is disallowed for FY 2025-26 **even if paid in April/May 2026, well before the return filing due date**. It only becomes allowable in the year it is ACTUALLY paid, whenever that is.
3. **Traders are excluded**: per the Ministry of MSME's Office Memorandum dated 1 September 2021, wholesale and retail trading enterprises, even if Udyam-registered, are excluded from Section 15/16 MSMED protection (their Udyam registration benefit is limited to priority-sector lending) — so Section 43B(h) does not apply to amounts payable to a suppler whose Udyam registration reflects a trading activity. Confirm the supplier's registered activity category, not merely the fact of registration.
4. **Registration timing**: the supplier must have held Udyam registration as a Micro or Small enterprise on the date of the relevant transaction (date of supply) — Udyam registration is not retrospective. A supplier registering mid-year does not trigger 43B(h) for transactions that occurred before their registration date. Verify registration date against invoice/transaction dates.
5. **Effective from FY 2023-24 (AY 2024-25) onward** — balances outstanding as at 31 March 2023 (i.e., the transition point) were not retrospectively affected; the rule applies to liabilities arising from FY 2023-24 onward. For FY 2025-26, this is now in its third year of applicability — no longer "brand new," but still a common error area because: (a) staff default to normal 43B due-date relief out of habit; (b) Udyam registration status/category (trader vs manufacturer/service provider) is often not verified; (c) the 45-day/15-day due date calculation from "date of acceptance" (not invoice date) is easy to get wrong.
6. **Scope — revenue vs capital**: Section 43B, by its structure, applies to sums "otherwise allowable as a deduction" — so it is generally understood to apply to trade payables for goods/services that are revenue in nature (i.e., claimed as a P&L deduction), not to amounts capitalised as fixed assets (which are never claimed as a direct P&L deduction and instead flow through depreciation). Treat payables to an MSME supplier for a capitalised fixed-asset purchase as outside Section 43B(h)'s scope, but flag any borderline case (e.g. large capital work-in-progress payable to an MSME contractor) `[JUDGMENT CALL — CA TO CONFIRM]` since this is a debated interpretive area without a definitive settled position.

### Procedure specific to 43B(h)
1. Obtain the trade creditors/payables ageing schedule as at 31 March 2026.
2. Obtain Udyam Registration certificates (or self-declared Udyam numbers on supplier invoices/GST portal vendor master) for all significant suppliers; classify each as Micro, Small, Medium, or Not Registered, and note their registered activity (Manufacturing / Service / Trading).
3. Exclude Medium enterprises and Trading-category suppliers from this analysis.
4. For each remaining Micro/Small (non-trading) supplier with an outstanding payable at year-end, determine the Section 15 due date for each individual invoice (45 days from acceptance if a written agreement specifies a period up to 45 days, else 15 days from acceptance — "acceptance" generally means delivery/deemed acceptance, not the invoice date, though in practice invoice date is often used as a reasonable proxy in the absence of a documented acceptance date `[JUDGMENT CALL — CA TO CONFIRM]`).
5. Any invoice-level amount unpaid beyond its Section 15 due date, and STILL unpaid as at 31 March 2026, is disallowed under s.43B(h) for FY 2025-26 in full — populate `Section = 43Bh`, `LiabilityType` per the utility's expected value (this is a "not paid during previous year" scenario, so likely `NPDPY`/`NPBDD` depending on how the utility frames it — confirm against the live form), `Description` (supplier name/invoice reference), `Amount`.
6. Do NOT apply return-due-date relief to this figure, and explicitly note in the workpaper that the amount remains disallowed even if the client subsequently pays it before the ITR filing date — this is the point most likely to be gotten wrong by a junior preparer defaulting to the general 43B pattern.
7. If Udyam registration certificates for suppliers are not available: `[MISSING — REQUEST UDYAM REGISTRATION STATUS FOR MAJOR SUPPLIERS FROM CLIENT]` — do not assume a supplier is or isn't MSME-registered without documentary confirmation; a materiality-based sampling approach (obtain Udyam status for the largest year-end payables first) is a reasonable practical fallback, flagged `[JUDGMENT CALL — CA TO CONFIRM]`.

### Common mistakes across Clause 26
- Giving 43B(h) the same return-due-date grace period as every other 43B category — this is the single most consequential error in this clause.
- Confusing employer's PF/ESI contribution (43B(b), gets due-date relief) with employee's contribution (s.36(1)(va), Clause 20(b), NO due-date relief) — these sit in different clauses and follow opposite rules; do not merge them.
- Treating a Udyam-registered trading enterprise as covered by 43B(h).
- Missing the pre-existing (brought-forward) liability limb — i.e., forgetting to check whether LAST year's disallowed-and-carried-forward 43B items were paid this year (and are therefore now allowable).
- Using invoice date instead of acceptance date for the Section 15 due-date computation (usually a minor difference, but can matter for month-end invoices).
