# Demo Client Answer Key — Bright Horizon Textiles Private Limited

This file is for testing/validation only. It is **not** a source document — do not pass it to the skill as
client input. It exists so a developer (or the CA reviewing skill output) can quickly check whether a run
against this demo client correctly caught the issues deliberately embedded in the documents.

Company: Bright Horizon Textiles Private Limited | PAN AABCB1234C | FY 2025-26 / AY 2026-27
Company → accounts audited under Companies Act 2013 → **Form 3CA-3CD applies** (not 3CB).
Turnover ~Rs. 11.85 crore → comfortably exceeds even the enhanced Rs. 10 crore threshold → 44AB audit clearly mandatory.

## Embedded issues the skill should surface

1. **Clause 8a** — Company has opted for Section 115BAA (22% concessional rate), first exercised AY 2021-22 via Form 10-IC. Should be picked up from client_profile.txt.
2. **Clause 12** — Presumptive scheme: N/A (company on regular books). Should be correctly marked NIL, not fabricated.
3. **Clause 14** — Stock valuation policy note states inclusive method (GST/duty inclusive) consistent with Sec 145A — no deviation. Should be marked "no deviation."
4. **Clause 17** — No land/building transfer during the year. Should be marked N/A, not invented.
5. **Clause 18** — Depreciation: Computer addition of Rs. 3,00,000 on 15-Jan-2026 used <180 days → half rate (40%→20% effective). Vehicle sold 20-Nov-2025 (cost 8L, opening WDV 5L, sold for 4.5L) → block continues, reduces block by sale proceeds. Skill should catch the half-rate treatment and the block adjustment on sale.
6. **Clause 20(b) / Sec 36(1)(va)** — Employee's own PF contribution for Feb-26 wages (Rs. 42,000) deposited 25-Apr-2026, after the 15-Mar-2026 due date → **permanently disallowed** (Checkmate Services ruling — no grace period for employee contributions). This is the highest-value "gotcha" in the dataset; the skill must not treat it like an ordinary 43B item with return-due-date relief.
7. **Clause 21(a)** — Disallowable items sitting in "Other Expenses": Rs. 2,00,000 political donation/souvenir advertisement, Rs. 1,50,000 club membership, Rs. 45,000 GST penalty, plus CSR expenditure Rs. 1,80,000 (disallowed under Explanation 2 to Sec 37(1)).
8. **Clause 21(b) / Sec 40(a)(ia)** — Rs. 1,20,000 paid to Apex Legal Consultants (professional fees, Sec 194J, threshold Rs. 30,000) with **no matching TDS entry** in the TDS Returns Filed Summary (other_registers.xlsx, "TDS Returns Filed Summary" sheet, explicit note at the bottom). 30% disallowance = Rs. 36,000. This requires cross-referencing the bank statement, trial balance ledger, and the TDS returns sheet — a good test of whether the skill actually cross-checks rather than reading one document in isolation.
9. **Clause 21(d) / Sec 40A(3)** — Cash payment of Rs. 55,000 to Shree Balaji Packaging on 12-Aug-2025, single day single party, revenue expenditure, no Rule 6DD exception applies → fully disallowable.
10. **Clause 21(g)** — Contingent liability: Rs. 8,50,000 GST demand disclosed in notes but not provided for — should be disclosed here, not treated as a P&L disallowance (it was never debited to P&L).
11. **Clause 22 / MSMED Act** — No cash-flow-visible MSME interest is booked (none accrued/provided in this demo — deliberately NIL) — correct answer is NIL, but the skill should still explain why (no interest provision found) rather than silently skipping.
12. **Clause 23 / Sec 40A(2)(b)** — Related party payments to Rajesh Shah (MD, 62% shareholder): Rs. 24,00,000 remuneration + Rs. 5,00,000 loan interest. Should list both.
13. **Clause 26 / Sec 43B(h)** — Om Fabrics (Micro enterprise, Udyam registered), invoice 10-Jan-2026 Rs. 6,50,000, 30-day terms, unpaid at year end (50 days overdue) → disallowable under 43B(h) with **no return-due-date grace period** (unlike other 43B items). Shakti Textile Traders (Rs. 4,00,000) is NOT yet due at year end (within 45-day terms) → should NOT be disallowed — tests whether the skill distinguishes "overdue" from "not yet due."
14. **Clause 27(a)** — GST ITC of Rs. 18,000 reversed (blocked credit, motor car insurance, Sec 17(5)) — debited to P&L, ties gst_returns_summary.xlsx to the trial balance ledger "GST Input Credit Reversed."
15. **Clause 27(b)** — Prior period expense Rs. 35,000 (FY24-25 audit fee booked late) sitting in the trial balance — should be picked up as a prior-period item.
16. **Clause 28–30C** — All should be marked N/A / NIL (no share transactions, no hundi borrowings, no TP primary adjustment, no thin-cap interest >Rs 1cr to an AE, no GAAR arrangement). Tests that the skill doesn't hallucinate applicability for clauses that essentially never apply to a plain domestic SME.
17. **Clause 31 / Sec 269SS** — Rs. 3,50,000 unsecured loan taken in **cash** from director Rajesh Shah on 05-Sep-2025 → violates Sec 269SS (loan/deposit >Rs. 20,000 must be by account payee cheque/bank transfer). Should be flagged clearly as a violation requiring disclosure (and the CA's attention re: Sec 271D penalty exposure, which the skill doesn't compute but should mention as a flag).
18. **Clause 32** — Brought forward business loss AY 2022-23, Rs. 4,20,000, no shareholding change >51% during the year → Sec 79 not triggered, eligible to carry forward. Also flag as [JUDGMENT CALL] the Sec 115BAA set-off interaction — deliberately left ambiguous in the data for the CA to confirm.
19. **Clause 34** — TDS/TCS compliance table should reconcile against "TDS Returns Filed Summary" — all sections shown as timely except the missing 194J on Apex Legal Consultants (see #8) and no explicit TDS shortfall interest computed (should be flagged as JUDGMENT CALL for the CA to quantify precisely once the 194J default is confirmed).
20. **Clause 37/38/39/42/43** — All should be marked N/A per client_profile.txt (no cost audit, no excise audit, no Form 61A, no CbCR applicability) — tests correct suppression of inapplicable clauses using the explicit profile statements rather than silence/omission.
21. **Clause 40** — Accounting ratios: current year vs FY 2024-25 figures both given in financial_statements.docx — should compute GP/turnover, NP/turnover, stock/turnover ratios for both years.
22. **Clause 41** — The Rs. 8,50,000 GST demand (contingent liability note) should also surface here as "demand raised under a tax law other than Income-tax Act" during the year (18-Feb-2026 notice) — a good test of whether the skill connects the same fact across two different clauses (21/26 vs. 41) correctly, since clause 41 is about the demand *notice* itself, not a P&L disallowance.
23. **Clause 44** — GST-wise expenditure breakup: the skill should check current CBDT deferral status (per references/clauses-36-to-44.md) before deciding whether to actually attempt the computation for this client.

## What should NOT happen
- No document mentions land/building transfer, share premium (56(2)(viib)), hundi borrowings, GAAR, or CbCR — the skill must mark these NIL/N/A rather than inventing a transaction to fill the clause.
- The exact quantum of interest disallowance under Sec 201(1A) for the missed 194J deduction is **not** computable from the documents provided (no exact deduction date given for when TDS should have been withheld) — the skill should flag this as a judgment call needing the CA's input, not invent a number.
