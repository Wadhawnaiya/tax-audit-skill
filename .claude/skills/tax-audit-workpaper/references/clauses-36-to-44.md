# Form 3CD — Clauses 36 to 44 (AY 2026-27 / FY 2025-26)

Reference for drafting the Form 3CD tax-audit workpaper under section 44AB of the Income-tax Act, 1961. Each clause below states: the statutory basis, the exact JSON schema fields the filled value must map to (from `schema_3CB.json` / `3CB_structure.txt`), the source documents, a step-by-step extraction procedure, common junior-staff mistakes, and the missing-data protocol. This range covers a cluster of largely dormant/obsolete clauses (36, 38, 39), a genuinely new one the schema reveals (36B), and the two clauses that most often get either over-reported (37/38/39/42/43 marked "Yes" on a client that doesn't actually qualify) or under-reported (44 wrongly treated as still deferred).

**Missing-data protocol (applies to every clause in this file):**
- Any **factual figure, date, name, or amount** not found in the source documents → write `[MISSING — CONFIRM WITH CLIENT]`. Never estimate, round, or infer a number that isn't in the records.
- Any **classification, characterization, or interpretive call** (e.g., "does this vendor qualify as GST-composition," "does this loan fall within accumulated profits") → make the call, but flag it `[JUDGMENT CALL — CA TO CONFIRM]` so the signing CA reviews it before the report is finalized.

**Flag-state convention used in this range:** several fields in this range use a three-state pattern `Y|N|X` (`CostAuditFlag`, `AuditExciseFlag`, `AuditSec72Flag`). Treat `X` as **"Not Applicable to this class of assessee"** (e.g., a non-company assessee for cost audit, a non-excise-liable business for clause 38) and `N` as **"Applicable category, but not carried out this year / no such event this year."** Confirm this Y/N/X split against the live e-filing utility's exact labels before relying on it as gospel — the schema itself carries no field-level description text, so this is the most defensible reading of the pattern rather than a directly documented one.

---

## Clause 36 — Dividend Distribution Tax under Section 115-O (OBSOLETE — mark N/A)

**Statutory basis:** Section 115-O (tax on distributed profits of domestic companies). **Abolished by the Finance Act, 2020, with effect from 1 April 2020 (AY 2021-22 onward).** Dividends declared, distributed, or paid on or after 1 April 2020 are taxable in the hands of the shareholder under normal provisions (as "Income from Other Sources," with TDS deductible by the company under section 194), not via DDT paid by the company.

**Schema mapping:** `Form3cdDistribtedProf115O[]` — array of `{TotAmtsDistProf, AmountRed115O1Ai, AmountRed115O1Aii, TotalTaxPaid, DateOfPayment, Amount}`. The field still exists in the schema (legacy retention) but has no current-year use case for a standard client.

**Current-year treatment:** For FY 2025-26, this clause is effectively **blank/Not Applicable for all standard cases**. Do not populate the array. There is no DDT liability arising on any dividend declared in FY 2025-26, regardless of company size or dividend quantum.

**The one edge case to actively rule out, not assume away:** a company that declared a dividend *before* 1 April 2020 but is only now, in FY 2025-26, making a delayed DDT payment or settling an old DDT demand/dispute (e.g., an appellate order from a pre-2020 DDT assessment concluding this year). This is rare but not impossible for a long-pending litigation client. Ask the client/review the tax litigation tracker for any *pre-FY2020-21* dividend declaration with unresolved DDT status before concluding "blank" — do not populate the array speculatively; if such a payment genuinely occurred, capture it and flag `[JUDGMENT CALL — CA TO CONFIRM]` since it is an unusual fact pattern deserving the signing CA's explicit sign-off.

**Common junior-staff mistakes:**
- Treating an old checklist/prior-year template literally and trying to "fill in" a DDT figure using the current year's dividend distributed — DDT does not exist on current-year dividends at all; this is a pure carry-over error from pre-2020 templates.
- Confusing this clause with the shareholder-level tax treatment of dividend income (which belongs in the shareholder's own return, not this clause of the *paying company's* Form 3CD).

---

## Clause 36A — Deemed Dividend under Section 2(22)(e)

**Statutory basis:** Section 2(22)(e) — deems as dividend any payment by a closely-held company (a company in which the public are not substantially interested) by way of loan or advance to: (a) a shareholder holding ≥10% of the voting power (beneficial owner of equity shares, not entitled only to a fixed dividend rate), or (b) any concern (HUF, firm, AOP/BOI, or company) in which such a shareholder has a "substantial interest" (beneficial entitlement to ≥20% of the concern's income); also covers any payment made by the company on behalf of, or for the individual benefit of, such a shareholder. The deeming is capped at the paying company's **accumulated profits** (excluding capitalized profits) as of the date of the loan/payment — it is not automatically the full loan amount.

**Schema mapping:** `Form3cdFlags.SubClauseeofClause22` (`Y`/`N` — the main clause 36A flag) + `Form3cdNatureOfDividend[]` — array of `{AmountRecieved, ReceiptDate}`, one entry per qualifying receipt.

**Critical direction check — this is the #1 trap on this clause:** clause 36A asks whether **the assessee under audit** *received* a deemed dividend, not whether it *paid* one. It is filled in the Form 3CD of the **recipient** (the shareholder-director, or the sister concern/HUF/firm in which the shareholder has substantial interest) — never in the Form 3CD of the closely-held company that advanced the loan, purely because it advanced the loan. If you are auditing the company that gave the loan, clause 36A of *that company's own* report stays `N` regardless of how large the loan was (though the loan is still relevant to the company's own related-party/loan disclosures and its TDS-under-section-194 compliance on the deemed dividend — that is a separate compliance thread, not this clause).

**Source documents:** Assessee's bank statements and loan/advance ledgers (or director's current account, if the assessee is that individual); shareholding register / register of members of the closely-held company(ies) in which the assessee or its controlling shareholder holds an interest, to establish the ≥10% voting-power or ≥20% substantial-interest test; balance sheet of the paying company (reserves & surplus, to establish accumulated profits, excluding capitalized profits such as a bonus-issue-funding general reserve); board minutes sanctioning the loan/advance; related-party transaction register.

**Extraction procedure:**
1. Establish whether the assessee (or, if the assessee is a firm/HUF/AOP, one of its partners/members) holds ≥10% voting power in any closely-held company, OR whether the assessee itself is a "concern" in which such a ≥10%-holding shareholder has substantial interest (≥20% profit entitlement).
2. If yes, scan the assessee's bank statements and loan ledgers for any loan, advance, or payment received from that closely-held company during FY 2025-26 (or any payment the company made for the assessee's individual benefit — e.g., settling a personal expense).
3. For each such receipt, obtain the paying company's accumulated profits as of the date of the loan (reserves & surplus per its balance sheet, adjusted per Explanation 2 to section 2(22) for depreciation computed at Income-tax rates rather than book rates) — the deemed dividend is capped at this figure, not the loan's face value. Flag `[MISSING — CONFIRM WITH CLIENT]` if the paying company's balance sheet isn't available, and `[JUDGMENT CALL — CA TO CONFIRM]` on the accumulated-profits computation itself.
4. Apply the statutory carve-outs before concluding a receipt is deemed dividend: loans advanced in the ordinary course of business where money-lending is a substantial part of the paying company's business (e.g., an NBFC), and genuine trade advances (e.g., security deposit for a bona fide business transaction), are excluded.
5. Populate `Form3cdNatureOfDividend[]` with `AmountRecieved` and `ReceiptDate` for each qualifying receipt (capped at accumulated profits, not the gross loan); set `SubClauseeofClause22 = Y`. If none, set `N` and leave the array empty.
6. As a cross-check, confirm the paying company deducted TDS under section 194 on the deemed dividend — a mismatch doesn't change this clause's answer but is worth flagging to the payer-side engagement team if the same firm audits both entities.

**Common junior-staff mistakes:**
- Reporting the company's *outward* loan to its director under clause 36A of the *company's own* Form 3CD (wrong direction — see the direction check above).
- Treating every debit balance in a director's current account as automatically deemed dividend without checking the company's accumulated profits — the deeming is capped, not open-ended.
- Missing indirect benefit — the company paying a shareholder's personal expense/credit card directly is also covered, not just direct cash loans to the shareholder.
- Missing the "concern" angle — a loan to a family-owned sister firm/HUF in which the shareholder (not the concern) has substantial interest also counts; staff often check only the shareholder's personal loan account and skip loans routed to associate concerns.
- Not applying the ordinary-course-of-business/NBFC or genuine-trade-advance carve-outs, over-reporting routine commercial credit as deemed dividend.

---

## Clause 36B — Buy-Back of Shares under Section 2(22)(f) (NEW — applicable from AY 2025-26 onward)

Not part of the historically-numbered clause list, but present in the current schema (`Section36BFlag`, `Form3cd36BRecievedAmt`) and squarely within the 36–44 range — a genuinely new clause staff need to know about, since it did not exist in templates/checklists from before FY 2024-25.

**Statutory basis:** Finance (No. 2) Act, 2024 inserted a new limb into section 2(22)(f), deeming the amount received by a shareholder on buy-back of shares by a domestic company (under section 68 of the Companies Act, 2013) as **dividend**, effective **1 October 2024**. Correspondingly, section 46A was amended so the buy-back consideration is no longer taxed as capital gains — instead, the full amount received is taxed as dividend income (no deduction for cost of acquisition against it), while the original cost of acquisition of the bought-back shares becomes a **capital loss** (consideration deemed nil for section 46A purposes), available for set-off/carry-forward against other capital gains. CBDT gave effect to the reporting requirement via the **Income-tax (Eighth Amendment) Rules, 2025** (Notification No. 23/2025, dated 28 March 2025), inserting clause 36B into Form 3CD, effective **1 April 2025** — applicable to tax audit reports for **AY 2025-26 onward**, and therefore squarely applicable to this AY 2026-27 / FY 2025-26 engagement.

**Schema mapping:** `Form3cdFlags.Section36BFlag` (`Y`/`N`) + `Form3cd36BRecievedAmt[]` — array of `{AmountRecieved1, AmountRecieved2}`. Based on the two-amount structure matching the clause's stated requirement ("amount received" and "cost of acquisition of shares bought back"), `AmountRecieved1` = amount received on buy-back (taxable as dividend) and `AmountRecieved2` = cost of acquisition of the shares bought back (the resulting capital-loss base) — this pairing is inferred from the field names and the clause's known two-part disclosure requirement, not from an in-schema label; verify against the live e-filing utility's on-screen labels at data-entry time before relying on the ordering.

**Applicability:** only for assessees (shareholders) who tendered shares in a buy-back offer of a domestic company **during FY 2025-26, where the buy-back consideration was received on or after 1 October 2024.** Buy-backs settled before 1 October 2024 remain under the old section 46A capital-gains regime — not this clause.

**Source documents:** Broker contract note / buy-back tender acceptance-cum-return advice from the company or its RTA; demat account statement showing the shares extinguished; bank statement showing the buy-back consideration credited; original purchase records for the specific shares tendered (to establish cost of acquisition); Form 26AS/AIS (buy-back proceeds attract TDS under section 194 by the company, similar to ordinary dividend TDS, effective from 1 October 2024).

**Extraction procedure:**
1. Scan the assessee's demat/investment records and bank credits for any buy-back-related receipt during FY 2025-26.
2. Confirm the buy-back consideration was actually received/record date fell on or after 1 October 2024 — anything settled earlier stays out of this clause.
3. Use the **accepted** quantity of shares (not the tendered quantity) in a proportionate/oversubscribed buy-back — these commonly differ.
4. Identify the original cost of acquisition of the specific shares accepted (FIFO or specific identification per the assessee's investment records) — this becomes the capital-loss base since the consideration for section 46A purposes is deemed nil.
5. Populate `AmountRecieved1` (buy-back proceeds, dividend income) and `AmountRecieved2` (cost of acquisition, capital-loss amount); set `Section36BFlag = Y`. Cross-check the section 194 TDS credited (Form 26AS/AIS) as a corroborating check, not as the reported figure itself.
6. Confirm the resulting capital loss is actually carried into the capital-gains schedule of the income computation (not just disclosed here and forgotten) and that the dividend amount is offered under "Income from Other Sources" — flag any mismatch `[JUDGMENT CALL — CA TO CONFIRM]`.

**Common junior-staff mistakes:**
- Applying section 2(22)(f)/clause 36B to a buy-back settled *before* 1 October 2024 (grandfathered under the old capital-gains regime — do not restate it here).
- Using the tendered quantity instead of the accepted quantity in an oversubscribed buy-back.
- Treating the disclosure as a dead-end data point and forgetting the resulting capital loss needs to flow into the capital-gains computation for carry-forward.
- Confusing this with clause 36A — both are sub-clauses of section 2(22), both use a parallel-looking two-field array structure in the schema, but they are entirely different transaction types (loans/advances vs. share buy-back).

---

## Clause 37 — Cost Audit

**Applicability — N/A for the vast majority of clients.** Cost audit has nothing to do with the Income-tax Act; it arises under the **Companies Act, 2013** read with the **Companies (Cost Records and Audit) Rules, 2014** (as amended), and applies only to **companies** — never to individuals, HUFs, firms, LLPs, or AOPs — and even among companies, only to those engaged in specified regulated/non-regulated sectors (e.g., telecom, electricity generation/distribution, petroleum, pharmaceuticals/bulk drugs, sugar, fertilizers, cement, steel, and a defined list of other manufacturing sectors under Table A/Table B of the Rules) that also cross prescribed turnover thresholds. Broadly cited thresholds are: Table A (regulated sectors) — overall annual turnover ≥ ₹50 crore **and** turnover from the specific regulated product/service ≥ ₹25 crore in the immediately preceding FY; Table B (non-regulated sectors) — overall turnover ≥ ₹100 crore **and** turnover from the specific product/service ≥ ₹35 crore. These are Companies Act thresholds, not Income-tax figures — **verify the currently notified thresholds and sector list under the Rules as amended** before relying on them, since MCA periodically revises the sector list and thresholds.

**Statutory basis:** No Income-tax Act section; Companies (Cost Records and Audit) Rules, 2014 (Companies Act, 2013).

**Schema mapping:** `CostAudit.CostAuditFlag` (`Y`/`N`/`X`) + `CostAudit.CostAuditDetail` (free text, ≤500 characters — a *summary* of any disqualification/disagreement, not the full cost audit report).

**How to recognize when it DOES apply:** (1) assessee is a company; (2) engaged in production/manufacture of goods or provision of services falling in one of the specified sectors under the Rules; (3) turnover crosses the prescribed threshold for that sector. If all three hold, cost audit is mandatory for that company and this clause is live.

**Source documents:** Cost Audit Report (Form CRA-3) and the cost auditor's qualification/disagreement remarks, if applicable; board resolution appointing the cost auditor; MCA filings (Form CRA-2 intimating appointment, Form CRA-4 filing the report); management representation on cost-audit applicability; prior year's Form 3CD for continuity.

**Extraction procedure:**
1. If the assessee is not a company, set `CostAuditFlag = X` and stop — no further work needed.
2. If a company, check whether it falls in a specified sector and crosses the turnover threshold. If not, set `X`.
3. If cost audit is applicable, confirm whether it was actually carried out for the year — obtain the filed CRA-3/CRA-4. Set `Y` if conducted, `N` if applicable but genuinely not yet conducted (a reportable gap in itself, worth flagging to the CA).
4. Extract any disqualification/disagreement noted by the cost auditor into `CostAuditDetail`, concisely (500-character limit) — do not paste the full report.
5. If applicable but the cost audit report isn't available at the time of signing, mark `[MISSING — CONFIRM WITH CLIENT]` — never assume "no disqualification" in the absence of the actual report.

**Common junior-staff mistakes:**
- Reflexively marking `X`/`N` for every client without actually checking whether a manufacturing-company client crosses the sector-and-turnover thresholds — this clause is rare enough that it gets skipped by habit even when it genuinely applies.
- Confusing cost audit (a Companies Act concept, about cost records/cost accounting) with the statutory financial audit or the tax audit itself.
- Dumping the full CRA-3 report text into `CostAuditDetail`, exceeding the practical/character-limited scope of the field.

---

## Clause 38 — Audit under the Central Excise Act, 1944

**Applicability — N/A for virtually all clients.** GST subsumed most excise-liable goods from 1 July 2017. Central Excise Act, 1944 now applies only to a **narrow residual list**: petroleum crude, high-speed diesel, motor spirit (petrol), natural gas, and aviation turbine fuel (the five petroleum products not yet brought under GST), plus **tobacco and tobacco products** (which attract Central Excise duty in addition to GST). **Alcohol for human consumption is outside GST but is taxed under STATE excise law — a state-level subject, not the Central Excise Act, 1944 — so alcohol/liquor clients do NOT trigger this clause**; any state-excise demand/refund order they receive belongs instead under clause 41 (see `NameOfTaxLaw = SED` there). This distinction is a common point of confusion — "excise" is used loosely for both regimes, but only the Central Excise Act (petroleum + tobacco) is in scope here.

**Statutory basis:** Central Excise Act, 1944, read with the Central Excise Rules — audit could be a routine departmental audit (Rule 22) or a special audit under section 14A/14AA of the Act.

**Schema mapping:** `AuditExcise.AuditExciseFlag` (`Y`/`N`/`X`) + `AuditExcise.AuditExciseDetail` (free text, ≤500 characters).

**Source documents:** Central Excise registration certificate (if the client deals in the residual excise-liable goods at all); departmental EA-2000 audit report/memo, or special audit report under section 14A/14AA; excise returns (e.g., ER-1) for the excisable goods.

**Extraction procedure:**
1. Confirm whether the assessee actually deals in excise-liable goods (the five specified petroleum products, or tobacco/tobacco products) as its current business — not merely whether it holds a legacy excise registration from before 2017. If not, set `X`.
2. If yes, check whether a departmental or special audit was actually conducted during FY 2025-26 — obtain the audit report/memo.
3. Extract disqualification/disagreement remarks into `AuditExciseDetail`.

**Common junior-staff mistakes:**
- Treating a client with a dormant/legacy excise registration (goods now entirely under GST) as still requiring this clause — reconfirm the *current* goods dealt in, not the historical registration.
- Conflating state excise (alcohol) with the Central Excise Act, 1944 — they are different statutes administered by different authorities; only the latter is this clause's scope.

---

## Clause 39 — Audit under Section 72A of the Finance Act, 1994 (Service Tax) — OBSOLETE, still present in the schema

**Statutory basis:** Section 72A of the Finance Act, 1994 (special audit of taxable services). **Do not confuse this with section 72 of the Income-tax Act, 1961** (carry-forward of business losses) — the schema field name `AuditSec72` refers only to the Finance Act, 1994 provision; it has nothing to do with the Income-tax Act's loss carry-forward section despite the superficially similar name. This naming overlap is a real trap for staff skimming the schema.

**Confirmed still in the current form/schema:** `AuditSec72.AuditSec72Flag` (`Y`/`N`/`X`) + `AuditSec72.AuditSec72Detail` (free text, ≤500 characters) are present in the current `schema_3CB.json` — clause 39 has **not** been removed or renumbered in the current form version, contrary to what one might assume given how thoroughly service tax has been superseded.

**Why it's functionally obsolete anyway:** service tax was subsumed into GST with effect from **1 July 2017**; there has been no service tax leviable on any transaction since. A section 72A audit could, in theory, still be initiated by the erstwhile service tax authorities in relation to a *pre-July-2017* period via legacy litigation, but such an audit — if it happened at all — would relate to old-period activity, not FY 2025-26. Given roughly eight years since GST rollout, most limitation periods for such legacy action have lapsed, making this an exceedingly rare live event.

**Current-year treatment:** N/A for essentially all clients in this filing cycle.

**Extraction procedure:**
1. Ask management / scan correspondence for any service-tax department notice or audit received during FY 2025-26 relating to a pre-GST period. In the overwhelming majority of cases, there is none.
2. Set `AuditSec72Flag` explicitly (`N` or `X` per the live utility's exact convention — confirm which one the current utility expects, since the object may be a mandatory field even though the underlying event is obsolete). **Do not leave it blank** — the field is required within the `AuditSec72` object once that object is populated at all.
3. In the rare case a legacy audit was concluded during the year, extract disqualification/disagreement remarks into `AuditSec72Detail`.

**Common junior-staff mistakes:**
- Leaving the field unanswered/blank on the assumption that "it doesn't apply so nothing needs to be entered" — an explicit N/X answer is still expected.
- Misreading the schema field name `AuditSec72` as referring to Income-tax Act section 72 (loss carry-forward) rather than section 72A of the Finance Act, 1994 — a pure naming trap, not a substantive issue, but one that has led to confused workpaper notes in practice.

---

## Clause 40 — Accounting Ratios (Turnover, Gross Profit, Net Profit, Stock-in-Trade, Material Consumed)

**Statutory basis:** Clause 40 of Form 3CD (Rule 6G) — a pure disclosure clause, no independent charging section.

**Schema mapping:** `Form3cdAccountingRatioCalculations` = `{PrevYrProfTurnOvr: ProfTurnOvrType, PrecPrevYrProfTurnOvr: ProfTurnOvrType}`. `PrevYrProfTurnOvr` = **current** previous year (FY 2025-26) figures; `PrecPrevYrProfTurnOvr` = **preceding** previous year (FY 2024-25) figures — both captured together in this year's report as a year-on-year comparative. Each `ProfTurnOvrType` block carries:
- `TotalTurnover` (mandatory) — total turnover for the year.
- `GrossprofitTurnover`, `NetprofitTurnover1`, `StockInTrade`, `MaterialconsumedFinishedgoods` — the four/five computed **ratios** (percentages).
- Paired raw numerator/denominator fields used to derive each ratio: `GrosProfNumertr`/`GrosProfDmntr` (gross profit ÷ turnover), `NetProfNumertr`/`NetProfDmntr` (net profit ÷ turnover), `StockTradeNmrtr`/`StockTradeDmntr` (closing stock-in-trade ÷ turnover), `MaterialNumrtr`/`MaterialDmntr` (material consumed ÷ finished goods produced — manufacturing only).

**Structural note grounded in the schema (a real practical constraint):** the schema captures only **one aggregate set** of ratios per year, not a segment-wise breakup by manufacturing/trading/professional line of business, even though the clause's stated intent (and the ICAI Guidance Note) contemplates reporting separately for each distinct line of business. For a multi-segment client, compute a blended aggregate for the actual utility entry, but keep a segment-wise workpaper on file internally, and flag the presentation approach `[JUDGMENT CALL — CA TO CONFIRM]`.

**Ratios required:**
- (a) Total turnover of the assessee.
- (b) Gross profit / turnover (%).
- (c) Net profit / turnover (%).
- (d) Stock-in-trade / turnover (%).
- (e) Material consumed / finished goods produced (%) — **manufacturing concerns only**; leave blank/zero (per utility convention) for pure trading or professional-service assessees rather than forcing a figure.

**Source documents:** Current year's audited financial statements/trial balance; **prior year's** audited financial statements **or** the prior year's own Form 3CD clause 40 (its "current year" column should equal this year's "preceding year" column — use this as a direct cross-check).

**Extraction procedure:**
1. Pull total turnover, gross profit, net profit, closing stock-in-trade, and (for manufacturing clients) material consumed and finished goods produced, for both FY 2025-26 and FY 2024-25.
2. Compute each ratio as a percentage for both years; populate both the raw numerator/denominator pair and the resulting percentage field, and manually cross-check that percentage = numerator ÷ denominator × 100 — a mismatch signals a data-entry or rounding error, not a real discrepancy to report.
3. Reconcile the FY 2024-25 ("preceding year") figures against **last year's own signed Form 3CD** clause 40 current-year column — they should tie exactly absent a restatement. Flag any variance `[JUDGMENT CALL — CA TO CONFIRM]`.
4. Compute the year-on-year swing for each ratio. **The clause itself only requires disclosure, not commentary** — but flag any material swing (e.g., gross margin dropping from the mid-20s% to low-teens%) as an internal note for the signing CA's attention, e.g. `[NOTE FOR CA: GP ratio fell from 24.6% to 11.2% YoY — investigate before finalizing]`. This note is not filed as part of the clause; it's a workpaper flag.
5. For non-manufacturing clients, leave the material-consumed ratio fields blank/zero rather than fabricating a figure.

**Common junior-staff mistakes:**
- Computing turnover on a GST-inclusive basis in one year and GST-exclusive in the other, distorting the year-on-year comparison.
- Forgetting the material-consumed ratio entirely for manufacturing clients (it's easy to treat this clause as "just three ratios").
- Using unaudited/provisional prior-year figures instead of the final signed prior-year Form 3CD, causing an avoidable mismatch with the auditor's own prior filing.
- Failing to flag a large swing for the CA's attention even though it isn't a strict disclosure requirement — this is exactly the kind of thing a reviewing partner expects to have been noticed, not just mechanically computed.

---

## Clause 41 — Demand Raised or Refund Issued Under Other Tax Laws

**Statutory basis:** Clause 41 of Form 3CD — covers demand/refund orders under **any tax law other than the Income-tax Act, 1961 and the Wealth-tax Act, 1957** (Wealth-tax itself is abolished from AY 2016-17 but the clause still excludes it by name). In practice: GST (CGST/SGST/IGST), Customs, State Excise (liquor), legacy Central Excise/Service Tax/VAT proceedings still working through litigation on old periods, Professional Tax, Stamp Duty, and similar levies.

**Schema mapping:** `Form3cdRefundDmdPrevYr[]` — array of `{FinYear, NameOfTaxLaw, TypeOfAmount, DateOfDemand, Amount, Remarks, StateCode, OtherTaxLaw}`.
- `FinYear` (enum, includes `"2025-26"`) — the financial year **the underlying tax liability relates to**, which may be an *earlier* year than the current audit year (e.g., a GST demand for FY 2021-22 raised via an order passed in FY 2025-26 is still reportable this year).
- `DateOfDemand` — the date of the **order itself**; this is the trigger for inclusion in *this* year's clause 41 (must fall within FY 2025-26), independent of which `FinYear` the order concerns.
- `NameOfTaxLaw` enum (`CED|SED|SET|GST|SAT|CD|OIT`) — read as: `CED` = Central Excise Duty, `SED` = State Excise Duty, `SET` = Service Tax, `GST` = Goods and Services Tax, `SAT` = Sales Tax/VAT, `CD` = Customs Duty, `OIT` = Other Indirect Tax. This decode is inferred from standard abbreviation convention (the schema carries no field-level description) — verify the exact label against the live e-filing utility's dropdown before final entry, and use `OtherTaxLaw` (free text) to specify the actual law when `OIT` is selected (e.g., "Professional Tax," "Entry Tax," "Stamp Duty").
- `TypeOfAmount` (`DEMAND`/`REFUND`) — report demand and refund events as **separate entries**, never netted.
- `StateCode` — populate for state-specific laws (SGST component, State Excise, Professional Tax, Sales Tax) using the assessee's state of registration for that order.

**Source documents:** GST portal downloads — demand orders (DRC-07) and refund sanction orders (RFD-06) for the period 1 April 2025 to 31 March 2026; customs assessment/refund orders; any legacy VAT/CST/service-tax/central-excise assessment or appellate order received during the year; correspondence register with tax authorities; professional-tax assessment/demand notices; books of account (provisions for demands, other income for refunds).

**Extraction procedure:**
1. Download the full set of GST portal orders (Demand & Recovery tab, and Refund application status) for FY 2025-26 — capture **every** order where a demand was raised or a refund was sanctioned/issued during the year, regardless of which tax period the order concerns.
2. Separately check for customs, state excise, professional tax, and any legacy VAT/service-tax/central-excise order received during the year — these are the ones most often missed because they're not tracked as systematically as the GST portal.
3. For each order, capture `NameOfTaxLaw` (nearest enum, or `OIT` + `OtherTaxLaw`), `TypeOfAmount`, `FinYear` (tax period concerned), `DateOfDemand` (order date, must fall in FY 2025-26), `Amount`, and a short `Remarks` on the nature/status of the proceeding (e.g., "GST demand u/s 73 for FY2022-23 — appeal filed before Commissioner (Appeals)").
4. Cross-check the amount against the books — a demand should generally appear as a contingent liability/provision note or an expense if accepted; a refund should appear as income/receivable. Flag inconsistencies `[JUDGMENT CALL — CA TO CONFIRM]`.
5. If an order's precise amount or date is not yet available, mark `[MISSING — CONFIRM WITH CLIENT]` rather than estimating.

**Common junior-staff mistakes:**
- Capturing only GST orders and missing professional tax, customs, and state excise orders, which are tracked less systematically.
- Reporting a single **net** figure (demand less refund) instead of separate `DEMAND` and `REFUND` entries.
- Using the underlying tax-period year instead of the order-date year to decide whether an item belongs in *this* year's clause 41 — the trigger is when the order was issued, not the year it concerns.
- Omitting orders that are under appeal or stayed — these are still reportable; the clause requires disclosure of the demand/refund and the related proceeding, not just final, unstayed demands.

---

## Clause 42 — Statement in Form No. 61, 61A, or 61B

**Applicability — N/A for the vast majority of standard SME/trading/professional clients.** Only relevant if the assessee itself is a "specified person" required to file one of these statements under Rule 114D/114E (Form 61/61A) or Rule 114G (Form 61B).

**What each form is for:**
- **Form 60**: a declaration filed *by a customer* who lacks a PAN, for specified transactions requiring PAN. This is source data, not the reporting form itself.
- **Form 61**: the periodic *statement* filed by the entity that **received** Form 60 declarations, compiling them for the tax department.
- **Form 61A**: Statement of Financial Transactions (SFT) — high-value/specified transactions (large cash deposits, property purchase/sale, high-value credit card payments, share/mutual fund transactions, etc.) filed by specified persons under Rule 114E: banks, post offices, sub-registrars (property registration), companies issuing shares/debentures above a threshold, mutual funds, NBFCs, credit card issuers, and others.
- **Form 61B**: Statement of Reportable Account under FATCA/CRS — filed by "reporting financial institutions" (banks, custodial institutions, depositories, specified insurers, investment entities) about accounts held by foreign tax residents. Relevant only to financial institutions, essentially never to an ordinary trading/manufacturing/professional client.

**How to recognize when it DOES apply to an "ordinary" client** (the two triggers most likely to catch an SME/private-company client by surprise):
- A **company issuing shares** (including premium) where the aggregate amount received for the share issue exceeds the Rule 114E threshold (commonly cited at ₹10 lakh in aggregate in the FY) — verify the current figure before relying on it.
- A tax-audit client (any assessee liable under section 44AB) that **receives cash payment for sale of goods or services exceeding a specified per-person threshold** (commonly cited at ₹2 lakh) — this is the trigger most often missed because it doesn't sound like an "SFT-relevant" business at first glance; always specifically check the cash-sales register for this.
- Also check: co-operative banks, NBFCs/companies accepting deposits above threshold, sub-registrars, and mutual funds/insurers, if the client happens to fall in one of these categories.

**Schema mapping:** `Form3cdFlags.FurnishStatement` (`Y`/`N` — the main clause 42 flag) + `Form3cdFurnishStatemnt[]` — array of `{EntityIdNumber, FormType, DueDateOfFurnish, DateOfFurnish, UnderSubSec286, ListOrTransactions}`.
- `EntityIdNumber` = **ITDREIN** (Income Tax Department Reporting Entity Identification Number) allotted on the Reporting Portal.
- `FormType` — enum `61`/`61A`/`61B`.
- `UnderSubSec286` (`Y`/`N`) — **despite its name**, in this field group it functions as clause 42's own sub-answer: "whether the statement contains information about all the details/transactions required to be reported." **Do not confuse this with the separate CbCR flag `Form3cdFlags.SubSec2Sec286` used for clause 43** — the two fields have confusingly similar names but serve entirely different clauses.
- `ListOrTransactions` — free text (≤100 chars) describing the nature of transactions reported.

**Source documents:** Reporting Portal ITDREIN allotment letter; filed SFT/Form 61/61B acknowledgment from the Reporting Portal; board resolution/share allotment register (for the share-premium trigger); cash sales register (for the cash-sale trigger); management representation on Rule 114E applicability.

**Extraction procedure:**
1. Determine whether the assessee is a "specified person" under Rule 114D/114E/114G at all — check nature of business (clause 10) and the two common triggers above (share issue over threshold, cash sales over per-person threshold) plus the institutional categories (bank/NBFC/mutual fund/insurer/registrar).
2. If not, set `FurnishStatement = N` and leave the array empty. This covers most clients.
3. If yes, obtain the `EntityIdNumber` (ITDREIN), `FormType` filed, `DueDateOfFurnish` (statutory due date — commonly 31 May following the FY for SFT under Rule 114E; confirm for other categories), and `DateOfFurnish` (from the Reporting Portal acknowledgment).
4. Cross-check the filed statement against the underlying transaction workpaper to confirm it genuinely captured **all** reportable transactions for the year — populate the `Y`/`N` sub-answer accordingly; if a known gap exists, mark `N` and describe it.
5. If due but not yet furnished as of the audit-report date, mark `DateOfFurnish` `[MISSING — CONFIRM WITH CLIENT]` and flag the delinquency for the CA (late/non-filing of SFT carries penal consequences under section 271FA).

**Common junior-staff mistakes:**
- Reflexively marking N/A for every client without specifically checking the cash-sales-over-threshold and share-premium-over-threshold triggers, both of which can catch an otherwise "ordinary" SME or private company by surprise.
- Confusing Form 60 (filed *by the customer*) with Form 61 (filed *by the entity* that received the Form 60s) — clause 42 is about the assessee's own reporting obligation as a specified person, not about whether its customers submitted Form 60.
- Mixing up `UnderSubSec286` (this clause's own sub-answer) with the unrelated `SubSec2Sec286` CbCR flag used in clause 43, due to the similar field names.

---

## Clause 43 — Country-by-Country Report under Section 286(2)

**Applicability — N/A for the overwhelming majority of standard domestic SME clients.** Relevant only if the assessee is a constituent entity (Indian subsidiary/branch/associate) of a multinational group whose global consolidated group revenue exceeds the prescribed threshold, or is itself the Indian ultimate parent of such a group.

**Statutory basis:** Section 286 (Country-by-Country Report for international groups), specifically sub-section (2); also section 286(4) (furnishing by an overseas parent/alternate reporting entity) and Rule 10DB.

**Threshold (verify before relying on it in a live engagement — periodically revised):** **₹6,400 crore** consolidated group revenue in the preceding accounting year, effective from 1 April 2021 per CBDT Notification No. 31/2021 dated 5 April 2021 (amending Rule 10DB), aligned to the OECD standard of EUR 750 million. No subsequent revision to this figure was located as of this writing.

**How to recognize when it DOES apply:** the assessee has a foreign parent/holding company, or is part of a group with entities across multiple countries, **and** the group's global consolidated revenue is very large (multinational, large-cap-sized) — for a typical Indian SME, family-owned business, or independent professional practice, this essentially never triggers. Check specifically for clients that are genuine subsidiaries of large foreign or Indian multinational corporate groups; a small Indian subsidiary of a giant global MNC still triggers this clause even though the *Indian entity's own* turnover is modest — **the test is the group's global revenue, not the assessee's own.**

**Schema mapping:**
- `Form3cdFlags.SubSec2Sec286` (`Y`/`N`/`D`) — the main clause 43 flag. `D` denotes a third state beyond plain Yes/No — most plausibly "liability exists but the due date for furnishing under section 286(4) has not yet arrived within the relevant accounting year." Confirm the exact semantics against the live filing utility's on-screen label before use.
- `Form3cdFurnishAltReportSec286` = `{FurnishAltReport, NameOfParEntity, NameOfAltEntity, DateOfFurnish}` — `FurnishAltReport` enum `A|P|R`, read as `A` = furnished by the **A**ssessee itself, `P` = furnished by the **P**arent entity, `R` = furnished by an alternate **R**eporting entity (this decode follows the letters directly; confirm exact utility labels before final entry). `NameOfParEntity`/`NameOfAltEntity` capture the parent/ARE name — the physical form also requires the country/territory of that entity, so record it in the accompanying workpaper narrative even though the JSON field itself is name-only.
- `ExpectedDate` (top-level field) = the **due date** for furnishing the report (statutorily 12 months from the end of the relevant reporting accounting year under section 286(2), or as separately notified for a secondary/local filing obligation). `Form3cdFurnishAltReportSec286.DateOfFurnish` = the **actual** date furnished, if already done.

**Source documents:** Group organizational chart/ownership structure; global consolidated financial statements of the ultimate parent (to test the revenue threshold); Form 3CEAC (intimation of the entity's reporting/parent details); Form 3CEAD (the actual CbCR, filed by the parent/ARE); Form 3CEAB (agreement designating an Alternate Reporting Entity, if applicable); group-level confirmation of who is filing.

**Extraction procedure:**
1. Determine whether the assessee is part of a multinational group at all — check the related-party/shareholding note in the financial statements.
2. If not, set `SubSec2Sec286 = N` and stop.
3. If yes, obtain or estimate the ultimate parent's global consolidated group revenue for the preceding accounting year and compare against ₹6,400 crore. If below, set `N`.
4. If above (or genuinely uncertain and material), determine who is actually furnishing the CbCR — the assessee itself, its parent, or a group-designated ARE — from Form 3CEAC/3CEAB filings and group confirmation.
5. Populate `FurnishAltReport`, `NameOfParEntity`/`NameOfAltEntity` (plus country/territory in the workpaper narrative), `ExpectedDate` (due date), and `DateOfFurnish` (actual date, if furnished).
6. If liable but the due date hasn't yet arrived as of the audit-signing date, use the `D` state rather than forcing a premature `Y`/`N`.

**Common junior-staff mistakes:**
- Not even checking the group structure for a foreign-owned subsidiary client because CbCR "sounds like a big-company-only thing" — always do at least a quick parent-and-revenue sanity check for any client with a foreign parent; don't skip the check outright.
- Testing the assessee's **own** revenue against ₹6,400 crore instead of the group's global consolidated revenue — the wrong number almost always makes a genuinely-in-scope small Indian subsidiary look "not applicable."
- Missing that a secondary/local filing obligation can fall on the Indian constituent entity itself in specific circumstances (e.g., the parent's home jurisdiction has no exchange agreement with India) — don't assume the parent's filing alone always closes out the Indian entity's own obligation.

---

## Clause 44 — Break-up of Total Expenditure by GST Registration Status of the Supplier

**CURRENT STATUS FOR AY 2026-27 / FY 2025-26: MANDATORY. This clause is NOT deferred.** This is the single most important thing to get right on this clause — many practitioners still carry over an outdated "clause 44 is deferred" assumption from its early years, and that assumption is now wrong and has been wrong for several filing cycles.

**Deferral history (for context, and to explain *why* the old assumption exists):** Clause 44 was introduced by the Income-tax (8th Amendment) Rules, 2018 (CBDT Notification No. 33/2018, dated 20 July 2018), intended to take effect from AY 2018-19. It was then kept in abeyance through a chain of CBDT circulars:
- Circular No. 6/2018 (17 Aug 2018) — deferred to 31 March 2019
- Circular No. 9/2019 (14 May 2019) — deferred to 31 March 2020
- Circular No. 10/2020 (24 Apr 2020) — deferred to 31 March 2021
- Circular No. 5/2021 (25 Mar 2021) — deferred to 31 March 2022

**No further deferral circular was issued after the March 2021 one.** Consequently, any tax audit report furnished on or after 1 April 2022 (i.e., from **AY 2022-23 onward**) is required to comply with clause 44, and it has remained mandatory every year since, with no subsequent deferral located. Treat it as a live, standard reporting requirement for FY 2025-26 — as a standing practice, do a quick check each filing season for any *new* deferral circular before relying on this, but as of the current filing cycle none exists.

**Statutory basis:** Clause 44 of Form 3CD (Rule 6G).

**Schema mapping:** `Form3cdBreakUpGST[]` — array of `{TotAmtExp, GoodOrSerGST, CompSchme, RegEntities, OthRegEntities, ExpNonRegGST}`, one entry per **expense head** (not one blended figure for the whole P&L):
- `TotAmtExp` — total expenditure incurred during the year for that head.
- `GoodOrSerGST` — expenditure relating to goods/services **exempt from GST**, procured from GST-registered entities.
- `CompSchme` — expenditure relating to suppliers registered under the GST **composition scheme**.
- `RegEntities` — expenditure relating to **other** normally-registered (regular taxable) suppliers.
- `OthRegEntities` — **total payment to registered entities**, i.e., the sum of `GoodOrSerGST + CompSchme + RegEntities` for that head — a cross-check total, not a fourth independent category.
- `ExpNonRegGST` — expenditure relating to suppliers **not registered** under GST at all.

**Field-name trap worth flagging explicitly:** `RegEntities` ("other registered entities," one component) and `OthRegEntities` ("total payment to registered entities," the sum) are easy to swap by mistake — the names look like near-mirrors of each other but hold different roles (one component vs. the aggregate). Double-check which field is which before populating, on every entry.

**Reconciliation logic:** for an expense head genuinely within GST's scope (i.e., it involves procuring a good/service from a third-party supplier), `TotAmtExp` should equal `OthRegEntities + ExpNonRegGST`. This does **not** hold for expense heads with no "supply" counterparty at all — salaries/wages (employer-employee relationship, outside the scope of "supply"), depreciation, provisions, statutory duties/taxes, and similar heads should either be excluded from `Form3cdBreakUpGST` entirely or entered with GST columns at zero, per the utility's convention — do not force a fabricated GST split onto a head that has none.

**Source documents:** GST purchase/expense register (cross-referenced against GSTR-2A/2B and the books); vendor master with GSTIN and registration type (regular/composition); GST-exemption status of the specific goods/services procured; expense-head-wise trial balance; vendor GST-return filing status (to confirm composition status — check the vendor's GST registration certificate or the composition-dealer list) for suppliers whose status isn't otherwise obvious.

**Extraction procedure:**
1. Pull the full expense-head-wise trial balance for FY 2025-26.
2. For each expense head involving a third-party supply (exclude salary/wages, depreciation, provisions, statutory levies, and other no-counterparty heads), obtain vendor-wise transaction detail.
3. Classify each vendor: not GST-registered → `ExpNonRegGST`; registered but the specific supply is GST-exempt → `GoodOrSerGST`; registered under composition → `CompSchme`; otherwise normally registered → `RegEntities`.
4. Sum `GoodOrSerGST + CompSchme + RegEntities` into `OthRegEntities` for that head.
5. Confirm `TotAmtExp = OthRegEntities + ExpNonRegGST` for heads genuinely in scope; investigate and flag any head that doesn't reconcile (commonly caused by cash purchases without a properly identified vendor) `[JUDGMENT CALL — CA TO CONFIRM]`.
6. Repeat per major expense head (Purchases, Freight, Rent, Professional Fees, Repairs & Maintenance, Advertisement, etc.) — a single blended total for the entire P&L does not satisfy this clause.
7. For any vendor whose GST registration/composition status can't be verified from available records, mark that vendor's classification `[MISSING — CONFIRM WITH CLIENT]` rather than guessing registered vs. unregistered.

**Common junior-staff mistakes:**
- **Treating this clause as optional or still deferred** — the single most important corrective here; it has been mandatory since AY 2022-23.
- Preparing one blended total instead of a genuine head-wise breakup.
- Mis-classifying a composition-scheme vendor as a regular registered vendor without actually checking the vendor's registration type.
- Confusing "goods/services exempt from GST" (a supply-side exemption — e.g., certain unprocessed agricultural produce, specified exempt services) with "vendor not registered" (a registration-status distinction) — these map to different columns and are frequently conflated.
- Swapping `RegEntities` and `OthRegEntities` due to the similarly-worded field names (see the field-name trap above).
- Skipping the per-head reconciliation of `TotAmtExp` against the registered + unregistered split, missing an internal-control check that would otherwise catch mis-classified or unidentified cash purchases.

---

### Forward-looking note (informational only — does not affect this engagement)

A new unified tax audit **Form 26** (under the Income-tax Act, 2025, which replaces the 1961 Act from 1 April 2026) is slated to replace Forms 3CA/3CB/3CD, but only for **tax years commencing on or after 1 April 2026** (i.e., FY 2026-27 and the audit cycle after this one). This AY 2026-27 / FY 2025-26 engagement — the previous year ending 31 March 2026 — still uses Form 3CD exactly as reflected in the current schema referenced throughout this file. No action needed now; just don't let a reference to "Form 26" in year-old articles or client questions cause confusion about which form applies to the current engagement.

---

### Cross-clause consistency checks (apply after drafting 36–44)
- Clause 36A's deemed-dividend receipts (if any) and clause 36B's buy-back receipts (if any) should both be cross-checked against the assessee's "Income from Other Sources" schedule in the income computation — both are dividend-taxable events that must actually be offered to tax, not just disclosed here and left out of the computation.
- Clause 36B's resulting capital loss (cost of acquisition of bought-back shares) should tie into the capital-gains schedule for carry-forward — confirm it isn't dropped between this clause and the computation.
- Clause 37/38/39 (cost audit / excise audit / service-tax audit) should be checked together in one pass against the assessee's registration profile (company status, sector, historical excise/service-tax registrations) — if none apply, this is a fast three-clause pass; don't spend disproportionate time on clauses that are N/A for 95%+ of the client base, but don't skip the sector/threshold check for manufacturing-company clients either.
- Clause 40's turnover figures should tie to the turnover reported for section 44AB applicability (clause 8) and to the P&L revenue line — a mismatch across these three places signals either a GST-inclusive/exclusive inconsistency or a genuine data error.
- Clause 41's GST demand/refund entries should be cross-checked against clause 44's expenditure figures only in the sense that both draw on the same GST portal access — pull both in the same portal session to save duplicate work, though the two clauses are otherwise unrelated in content.
- Clause 42's cash-sales trigger check (Form 61A) and clause 44's GST expenditure breakup both require a vendor/customer-wise transaction listing — where the client's accounting software can export one combined party-wise register, use it for both clauses rather than pulling it twice.
- Clause 43's group-structure review (foreign parent, consolidated revenue) is also the natural place to flag, for the CA's broader awareness, whether other international-taxation clauses elsewhere in Form 3CD (transfer pricing, section 92CE secondary adjustment, etc.) may need a closer look — CbCR-scale groups almost always have related-party international transactions worth a broader review, even though that review falls outside clauses 36–44 themselves.
