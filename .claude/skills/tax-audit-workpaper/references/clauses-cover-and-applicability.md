# Form 3CA/3CB Selection, Section 44AB Applicability, and Form 3CD Part A (Clauses 1–8a)

Scope: AY 2026-27 (PY/FY 2025-26), Income-tax Act 1961, Section 44AB, Form 3CA-3CD / Form 3CB-3CD (Rule 6G, Ver2.5 e-filing schema). Do not use Form No. 26 under the Income-tax Act 2025 — that only becomes mandatory for tax years commencing on or after 1 April 2026.

**Numeric thresholds**: figures below (turnover/receipts limits, basic exemption limit, presumptive-scheme rates) are stated as commonly understood for this filing season. Treat `references/thresholds-ay2026-27.md` as the authoritative source for exact rupee figures — verify every number quoted here against it before it goes into a workpaper.

Schema field paths cited below (`PartA.X`, `F3CA.type`, etc.) were confirmed directly against `references/schema/schema_3CA.json` and `references/schema/schema_3CB.json` (not just the flattened `.txt` dumps, which truncate long enum descriptions).

---

## 1. Form 3CA vs Form 3CB — Which Form Applies

**Decision rule**: Form 3CA applies when the assessee's accounts for the year are *already* required to be audited under some law **other than** the Income-tax Act (most commonly the Companies Act 2013). The tax auditor does not re-audit the financials — Form 3CA is a short certificate that appends Form 3CD to the other-law audit report. Form 3CB applies when no other law compels an audit of these accounts — the tax auditor personally audits the P&L/Income & Expenditure account and Balance Sheet, opines on true and fair view, and appends Form 3CD.

**Determination procedure**:

1. Identify the legal form of the entity from incorporation documents / deed / PAN.
2. Check whether any other law mandates an audit of *this entity, for this year*:
   - **Company** (Pvt Ltd, Ltd, OPC, Sec 8) — Companies Act 2013 s.139/143 audit is mandatory for every company, every year → **Form 3CA**. Evidence: Certificate of Incorporation, CIN, and (decisively) a statutory auditor's report on file addressed "to the members," referencing s.143 and usually a CARO annexure.
   - **LLP** — LLP (Amendment) Rules 2011, Rule 24(8): audit under the LLP Act is mandatory only if turnover exceeds ₹40 lakh **or** capital contribution exceeds ₹25 lakh in the year; otherwise LLP-Act audit is exempt. If the LLP's own financials cross either figure (or an LLP Act audit report is on file) → **Form 3CA**. If below both figures and the LLP still meets Section 44AB (e.g., via the 44AD(4) carve-out) → **Form 3CB**, since it is not "otherwise audited" that year. This LLP Act threshold is a Companies-law figure, not an income-tax figure — it does not change with the income-tax thresholds file.
   - **Partnership firm** (not LLP) — Indian Partnership Act 1932 has no statutory audit mandate → **Form 3CB**, regardless of turnover.
   - **Proprietorship** — no other law mandates audit → **Form 3CB**.
   - **Trust/society** — a Section 12A(1)(b) audit (Form 10B/10BB) is an audit *under the Income-tax Act itself*, so it does not count as "any other law" for this test. If the trust separately runs a business crossing 44AB and is not incorporated as a company/co-operative society requiring an other-law audit → **Form 3CB**.
   - **Co-operative society / co-operative bank** — most State/Multi-State Co-operative Societies Acts (and, for banks, the Banking Regulation Act 1949 s.56 read with the applicable Co-operative Societies Act) mandate a statutory audit → typically **Form 3CA**; confirm against the specific state Act and look for the departmental/panel auditor's report.
3. Evidence to look for in the document set, in order of reliability: (a) a separate statutory audit report already in the file (strongest signal — if present, it's 3CA); (b) Certificate of Incorporation / CIN / LLPIN; (c) partnership deed / LLP agreement with no accompanying other-law audit report (signals 3CB).
4. If the entity type is an LLP or co-operative society and neither a statutory audit report nor turnover/contribution figures needed to test the other-law threshold are available: **[MISSING — CONFIRM WITH CLIENT: does the LLP Act / Co-operative Societies Act mandate an audit this year — turnover/contribution figures or an existing audit report?]**. Never default to 3CB just because no report was supplied — an LLP crossing the LLP Act threshold that hasn't yet gotten its LLP Act audit done is still a 3CA case once that audit is completed.

**Schema note**: `schema_3CA.json` and `schema_3CB.json` are two structurally distinct top-level objects (`F3CA` vs `F3CB`), selected via `Form_Details.FormName` = `FORM3CA` or `FORM3CB`. Their `Declaration` blocks differ in substance, not just label: `F3CA.Declaration.Point1` carries `CA_FirmName`, `Act` (a 67-entry enum of the "other law" under which accounts were audited) and `Other_Act`, i.e. it names the other-law audit; `F3CB.Declaration` instead carries the auditor's own opinion structure — `Point2.HeadOfficeLocation`/`NumberOfBrances`, and `Point3.PointA.OCDI` (Observations/Comments/Discrepancies/Inconsistencies) where the auditor records qualifications on the true-and-fair view. Picking the wrong form at data-entry time is not just a labeling error — the two JSON shapes are not interchangeable.

---

## 2. Section 44AB Applicability — When a Tax Audit Is Required at All

Section 44AB triggers a mandatory audit under any of the following (verify all rupee figures against `references/thresholds-ay2026-27.md`):

- **Clause (a) — Business**: total sales/turnover/gross receipts exceed ~₹1 crore in the PY. An enhanced ~₹10 crore threshold applies instead if aggregate cash receipts **and** aggregate cash payments each do not exceed ~5% of the respective totals for the year (i.e., the business is substantially cashless/digital).
- **Clause (b) — Profession**: gross receipts exceed ~₹50 lakh in the PY. A parallel enhanced threshold (commonly cited around ~₹75 lakh, subject to a similar ≤5% cash condition) has applied to professionals in recent years — confirm current-year applicability and the exact figure in the thresholds file.
- **Clause (c) — Presumptive business under 44AE / 44BB / 44BBB**: assessee's income is otherwise computed on a presumptive basis under one of these sections, but the assessee **declares profits lower** than the deemed presumptive profit for that section, **and** total income exceeds the basic exemption limit → audit mandatory regardless of turnover.
- **Clause (d) — Presumptive profession under 44ADA**: assessee declares profits lower than the deemed 50% presumptive income under 44ADA, **and** total income exceeds the basic exemption limit → audit mandatory regardless of receipts.
- **Clause (e) — 44AD(4) applicability**: assessee had opted for presumptive taxation under 44AD in an earlier year, and in the current year declares profits below the 44AD presumptive rate — triggering 44AD(4)/(5)'s rule that presumptive taxation cannot be claimed again for 5 subsequent AYs. If, in a year covered by that lock-out, total income exceeds the basic exemption limit → audit mandatory regardless of turnover. **This is the specific "opted out of presumptive scheme" mandatory-audit trap** — turnover can be well under ₹1 crore and audit is still required.
- **Proviso to clause (a)** (schema code `44ABAA`): the cash-restriction condition is met, but turnover still exceeds even the enhanced ~₹10 crore limit → audit still triggered.
- **Third proviso** (schema code `44AB3`): accounts are already audited under another law — this is precisely the Form 3CA scenario from Section 1 above; it does not remove the 44AB obligation, it just changes which form is used to discharge it.

**Important carve-out**: clauses (c)/(d)/(e) only force an audit if total income exceeds the basic exemption limit. If total income is below the BEL, under-declaring against the presumptive rate does **not**, by itself, trigger mandatory audit. Always test total income against the BEL before concluding (c)/(d)/(e) applies.

**Procedure to determine applicability from client documents**:

1. Pull turnover/gross receipts for the PY from the trial balance / financial statements. Cross-check against GSTR-1/GSTR-3B annual totals where available — a mismatch between books turnover and GST turnover is itself a red flag worth noting separately.
2. Classify business vs profession from the nature-of-business/profession description (prior year ITR, GST registration "nature of business," trade license).
3. Test against clause (a)/(b) base limits. If close to the threshold, pull cash receipts and cash payments from the cash book / bank statements to test the ≤5% condition for the enhanced limit.
4. If turnover is below the (a)/(b) thresholds, check prior-year ITRs/computations for presumptive-scheme history (44AD/44ADA/44AE) and compare current-year declared income against the deemed presumptive rate for that scheme. If declared income is lower and total income exceeds the BEL, audit is mandatory under (c)/(d)/(e) even though turnover is nowhere near the (a)/(b) limits — this is easy to miss when only looking at turnover.
5. If none of the above triggers apply, no tax audit is required — do not draft a 3CD.
6. If turnover, cash-mix, or presumptive-scheme history cannot be established from the documents provided: **[MISSING — CONFIRM WITH CLIENT: turnover / cash-vs-digital split / prior-year presumptive scheme history]**. Do not assume audit is or isn't required — say so explicitly and stop.

---

## 3. Form 3CD Part A — Clauses 1 through 8a

### Clause 1 — Name of the Assessee
**Schema**: `PartA.AssesseeName.{FirstName, MiddleName, LastName}`. (Do not confuse with `Declaration.Point1.AssesseeName` in 3CA / 3CB, which is the same person but a separate copy in the schema, or `OtherInformation1.{FirstName,...}`, which is the **signing CA's** name, not the assessee's.)
**Source**: PAN card (name must match PAN database exactly — e-filing validates against it), or Certificate of Incorporation / LLP Agreement / Partnership Deed for entity names (use the ROC/MCA-registered legal name for companies and LLPs).
**If missing/unclear**: `[MISSING — CONFIRM WITH CLIENT]`. Never guess an expansion of initials or a spelling variant — a PAN mismatch causes e-filing rejection.

### Clause 2 — Address
**Schema**: `PartA.AddressDetail.{AddrDetail1, AddrDetail2, CityOrTownOrDistrict, LocalityOrArea/LocalityOrAreaName, PostOffice/PostOfficeName, StateCode, CountryCode, PinCode}`. `StateCode` is a 2-digit code, enum 01–37 for Indian states/UTs plus `99` for Foreign (full list in the schema description on `PartA.AddressDetail.StateCode`).
**Source**: principal place of business per the GST registration certificate, or registered office per the Certificate of Incorporation/MCA master data, or the prior year's tax audit report address for continuity. Cross-check against the PAN card address if nothing else is available.
**If registered office and principal place of business differ**: use the address of the place where books of account are maintained unless the reviewing CA instructs otherwise — flag the discrepancy rather than silently picking one.
**If missing/illegible**: `[MISSING — CONFIRM WITH CLIENT]`.

### Clause 3 — PAN / Aadhaar
**Schema**: `PartA.PAN` (required; 10-char pattern `[A-Za-z]{5}[0-9]{4}[A-Za-z]`), `PartA.AadhaarCardNo` (optional; 12 digits).
**Source**: PAN card / PAN allotment letter. Aadhaar is relevant only for individual assessees furnishing it in addition to/in lieu of PAN under s.139AA linkage — do not populate `AadhaarCardNo` for company/firm/LLP/trust assessees.
**Cross-check tip**: PAN's 4th character indicates assessee type — P=Individual, C=Company, H=HUF, F=Firm (LLPs conventionally also carry F on the PAN card, though verify the actual card rather than assuming), A=AOP, T=Trust, B=BOI, L=Local Authority, J=AJP, G=Government. Use this only as a sanity check against Clause 5's Status — the constitution document is the authority, not the PAN letter, if the two conflict.
**If missing**: `[MISSING — CONFIRM WITH CLIENT]` — PAN is mandatory in the schema (`PartA.required` includes `PAN`); do not proceed without it.

### Clause 4 — Registration Under Indirect Tax Laws
**Schema**: `PartA.IndirectTaxFlag` (`Y`/`N`, required) + `PartA.Form3cdIndirectTax[]`, each entry `{IndirectTaxType, StateCode, OtherIndirectTaxType, RegNo}`. `IndirectTaxType` pattern = `CED|SED|SET|SAT|GST|CD|OIT`. The schema only gives the code, not a label — best-effort reading, confirm against the live e-filing utility tooltip if it matters: CED = Central Excise Duty, SED = State Excise Duty, SET = Sales Tax (state), SAT = Service Tax, GST = Goods & Services Tax, CD = Customs Duty, OIT = Other Indirect Tax (free-text label goes in `OtherIndirectTaxType`).
**Determination**: set `IndirectTaxFlag = Y` if the assessee holds *any* indirect tax registration. In practice this is almost always GST for any entity crossing 44AB thresholds; also check for legacy Central Excise (petroleum, tobacco, liquor manufacturers still outside GST) and Customs/IEC registration for importers/exporters.
**Source**: GST Registration Certificate (Form REG-06) → one `Form3cdIndirectTax` entry with `IndirectTaxType=GST`, `RegNo` = the 15-digit GSTIN, `StateCode` derived from the GSTIN's state-code prefix. Multi-state entities get one entry per GSTIN. Excise/Customs registration certificates → CED/CD entries with their own registration numbers.
**If no indirect tax registration exists** (e.g., pure exempt-supply or below-GST-threshold service provider): `IndirectTaxFlag = N`, empty array — this is a valid, complete answer, not a gap.
**If turnover clearly exceeds the GST registration threshold but no GST certificate was provided**: do not assume `N` — `[MISSING — CONFIRM WITH CLIENT: GST registration status / GSTIN]`.

### Clause 5 — Status
**Schema**: `PartA.Status`, integer code 1–12 (required). Full mapping, confirmed from the schema's own `description` field (not the truncated flattened dump):

| Code | Status |
|---|---|
| 1 | Individual |
| 2 | Hindu Undivided Family (HUF) |
| 3 | Firm |
| 4 | Limited Liability Partnership (LLP) |
| 5 | Company |
| 6 | Trust |
| 7 | Association of Persons (AOP) |
| 8 | Local Authority |
| 9 | Artificial Juridical Person (AJP) |
| 10 | Co-Operative Society |
| 11 | Co-Operative Bank |
| 12 | Body of Individuals (BOI) |

**Determination**:
- **Individual** — no incorporation/constitution document; prior ITR filed as individual; PAN 4th char P.
- **HUF** — HUF deed/declaration or prior ITR filed as HUF; PAN 4th char H.
- **Firm** — partnership deed, not registered as an LLP; PAN 4th char F.
- **LLP** — Certificate of Incorporation (LLP) from MCA, LLPIN, LLP Agreement.
- **Company** — Certificate of Incorporation, CIN; PAN 4th char C.
- **Trust** — Trust Deed, registration under the Indian Trusts Act/applicable Public Trusts Act, or a 12A/12AB registration certificate.
- **AOP / BOI** — usually arises from a joint venture/collaboration arrangement with no formal incorporation. AOP implies persons combined with a common purpose and profit motive; BOI implies a combination without that intent (often individuals only, no "association" element). This is a judgment call from the underlying agreement — flag to the reviewing CA rather than guessing if the arrangement's intent isn't explicit.
- **Local Authority / AJP / Co-operative Society / Co-operative Bank** — identify from the specific enabling statute/registration certificate (municipal/panchayat constitution, State/Multi-State Co-operative Societies Act registration, Banking Regulation Act 1949 s.56 licence for co-op banks).
**If constitution is unclear**: `[MISSING — CONFIRM WITH CLIENT: legal status/constitution]`.

### Clause 6 — Previous Year
**Schema**: `PartA.PartAStartDate`, `PartA.PartAEndDate` (both required, `YYYY-MM-DD`).
For AY 2026-27 the PY is normally **2025-04-01 to 2026-03-31**. Use a shorter period only where the business was newly set up during the year (start date = date of commencement/incorporation, not 1 April) or discontinued during the year (end date = date of discontinuation/dissolution/GST cancellation).
**Source**: Certificate of Incorporation date for a new entity; closure intimation, GST cancellation order, or dissolution deed for discontinuation.
**If unclear whether the business commenced/ceased mid-year**: `[MISSING — CONFIRM WITH CLIENT]`.

### Clause 7 — Assessment Year
**Schema**: `PartA.AssessmentYear`, enum including `'2025-26'`, `'2026-27'`. For this filing season, value = `2026-27`. This is computed mechanically as PY+1 once Clause 6 is fixed — it is not independently sourced from any client document.

### Clause 8 — Relevant Clause of Section 44AB
**Schema**: `PartA.Clause[]`, array of `{ClauseNo}`; pattern/enum = `44ABa | 44ABb | 44ABci | 44ABcii | 44ABciii | 44ABd | 44ABe | 44AB3 | 44ABAA`. Multiple codes can be selected simultaneously — e.g., a company that is both statutorily audited (`44AB3`, hence Form 3CA) **and** separately crosses the turnover limit (`44ABa`) may need both.

| Schema code | Meaning |
|---|---|
| `44ABa` | Clause (a) — business turnover/gross receipts exceeds the base limit |
| `44ABAA` | Proviso to clause (a) — cash-restricted business (≤5% cash) but turnover still exceeds the enhanced limit |
| `44ABb` | Clause (b) — professional gross receipts exceed the limit |
| `44ABci` | Clause (c)(i) — profits declared lower than deemed presumptive profit under s.44AE |
| `44ABcii` | Clause (c)(ii) — structurally this should be the s.44BB limb of clause (c). **Caution**: the schema's own free-text `Description` for this code is mislabeled "(c)-iii" and points to s.44BBB — an apparent data-entry error in the government schema itself, since `44ABciii` (below) separately and correctly carries the 44BBB description. Verify against the live e-filing utility's dropdown label before relying on this beyond the structural reading. |
| `44ABciii` | Clause (c)(iii) — profits declared lower than deemed presumptive profit under s.44BBB |
| `44ABd` | Clause (d) — professional presumptive income under s.44ADA declared lower than deemed profits |
| `44ABe` | Clause (e) — s.44AD(4) applicable (business presumptive opt-out/under-declaration) |
| `44AB3` | Third proviso — accounts already audited under another law (the Form 3CA scenario) |

**Source**: this clause is a **conclusion**, not something read off a single document — it is the direct output of the Section 2 applicability analysis above (turnover from trial balance/GST returns, cash % from cash book/bank statements, presumptive-scheme history from prior-year ITRs).
**If the underlying applicability analysis could not be completed**: do not guess a clause. `[MISSING — CONFIRM WITH CLIENT: basis for 44AB applicability]`.

### Clause 8a — Option for Special Tax Regime
**Schema**: `F3CA.type` / `F3CB.type` — confirmed as a **top-level field, sibling to `PartA`**, not nested inside it (`definitions.F3CA.properties.type` / `definitions.F3CB.properties.type`, both `$ref`-ing a shared `definitions.type` with pattern `115BA|115BAA|115BAB|115BAC|115BAD`). It is **not** in either form's `required` array — omit it entirely if the assessee has not opted into any of these regimes, rather than leaving an empty string.

| Section | Applies to | Concessional feature |
|---|---|---|
| 115BA | Domestic manufacturing companies set up on/after 1 Mar 2016 | 25% flat rate, some exemptions foregone |
| 115BAA | Any domestic company | 22% flat rate, all exemptions/incentives foregone |
| 115BAB | New domestic manufacturing companies set up on/after 1 Oct 2019 (production commenced by the specified date) | 15% flat rate |
| 115BAC | Individuals / HUF | Concessional slab rates, exemptions/deductions foregone; **default regime from AY 2024-25 onwards** unless opted out |
| 115BAD | Resident co-operative societies | 22% flat rate, exemptions/incentives foregone |

**Not applicable to partnership firms or LLPs** — none of these five sections extend to firms/LLPs (they remain at flat 30% + surcharge/cess). Do not search for a regime election for a firm/LLP assessee; clause 8a is simply left blank for them.

**Evidence of opt-in/opt-out (form filing history)**:
- 115BA → Form 10-IB (one-time, filed with/before the ROI of the first year the option is exercised).
- 115BAA → Form 10-IC.
- 115BAB → Form 10-ID.
- 115BAC → for individuals/HUF *with* business/professional income: pre-AY 2024-25, opting **in** required Form 10-IE. From AY 2024-25, 115BAC is the **default** — an individual/HUF with business/professional income who wants to stay on the **old** regime instead must file Form 10-IEA (opt-**out**). Individuals without business/professional income choose the regime directly in the ITR each year with no separate form.
- 115BAD → Form 10-IF.

**Determination procedure**: check the prior year's ITR acknowledgment/computation sheet for the section under which tax was computed, or the specific Form 10-IB/10-IC/10-ID/10-IE/10-IEA/10-IF filing acknowledgment from the income-tax portal. For companies/co-operative societies, the 115BAA/115BAB/115BA/115BAD election is generally a one-time choice carried forward from the year first exercised — check the prior year's tax audit report if the current year's filing history is silent. For individual/HUF assessees with business/professional income specifically: **absent a Form 10-IEA on file, treat 115BAC (default new regime) as the answer** rather than leaving it blank, since that is now the statutory default.
**If the P&L shows tax computed at a rate consistent with one of these regimes (flat 22%/15%/25% with no Chapter VI-A deductions) but no filing evidence is available**: treat this as a supporting indicator only — still flag `[MISSING — CONFIRM WITH CLIENT: Form 10-IB/10-IC/10-ID/10-IE/10-IEA/10-IF acknowledgment or other basis for the regime claimed]` rather than asserting the clause from inference alone.
