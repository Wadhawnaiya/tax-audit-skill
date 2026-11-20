# Demo Client Answer Key — Bright Horizon Textiles Private Limited

**For testing and training only. Never give this file to the skill as a source document.** (The extractor's
`--all` mode skips files starting with `_` for exactly this reason.)

Company: Bright Horizon Textiles Private Limited | PAN AABCB1234C | FY 2025-26 / AY 2026-27
Company → accounts audited under the Companies Act 2013 → **Form 3CA-3CD**.
Turnover Rs. 11.854 crore → above even the Rs. 10 crore cash-light limit → s.44AB(a) audit mandatory.

Version 2 of this key (skill v1.0). Part A is the original 23 planted issues, corrected for the current law.
Part B lists issues that were also hidden in the data and that a strong run should find. Part C is the scoring
sheet for training sessions.

## Part A — Planted issues (must catch)

| # | Clause | Expected result |
|---|---|---|
| A1 | 8a | 115BAA opted, first exercised AY 2021-22 via Form 10-IC (client_profile.txt). |
| A2 | 12 | N/A — no presumptive income. Not fabricated. |
| A3 | 14 | Inclusive method, consistent with s.145A — no deviation. |
| A4 | 17 | N/A — no land/building transfer. |
| A5 | 18 | Computer Rs. 3,00,000 added 15-Jan-2026 → half rate (20%). Vehicle sold 20-Nov-2025 for Rs. 4,50,000 → reduces block, block continues. IT depreciation Rs. 36,52,500. |
| A6 | 20(b) | Employee PF Feb-26 Rs. 42,000 paid 25-Apr-2026 (due 15-Mar-2026) → **permanently disallowed** (Checkmate Services, SC 2022). No return-due-date relief. |
| A7 | 21(a) | Political souvenir advertisement Rs. 2,00,000 (s.37(2B)); club Rs. 1,50,000 (reported — see B9 on treatment); GST penalty Rs. 45,000; CSR Rs. 1,80,000. |
| A8 | 21(b) | Apex Legal Rs. 1,20,000, s.194J (threshold **Rs. 50,000** from FY 2025-26), no TDS → 30% = Rs. 36,000. Needs bank + TB + TDS summary cross-check. |
| A9 | 21(d) | Cash Rs. 55,000 to Shree Balaji Packaging, 12-Aug-2025 → s.40A(3) disallowance. |
| A10 | 21(g) | GST demand Rs. 8,50,000 is a contingent liability NOT debited to P&L → 21(g) NIL, disclosed in 41. |
| A11 | 22(i) | No MSMED interest booked → NIL, with the reason stated. |
| A12 | 23 | Rajesh Shah: remuneration Rs. 24,00,000 + loan interest Rs. 5,00,000. |
| A13 | **22(iii)(b) and 26** | Om Fabrics (Micro) Rs. 6,50,000 overdue at year end → s.43B(h), no grace period. **Since Notification 23/2025 this is reported in clause 22 AND clause 26 — one disallowance.** Shakti Textile Traders Rs. 4,00,000 not yet due → not disallowed. |
| A14 | 27(a) | ITC reversal Rs. 18,000 (blocked credit, s.17(5)) ties GST summary to TB. |
| A15 | 27(b) | Prior-period expense Rs. 35,000 (FY 2024-25 audit fee). |
| A16 | 29A–30C | All NIL/N/A. (Clauses 28 and 29 no longer exist — a run that emits them is wrong.) |
| A17 | 31 | Cash loan Rs. 3,50,000 from director on 05-Sep-2025 → s.269SS breach, code **B (cash received)**, s.271D exposure flagged (not computed). |
| A18 | 32 | B/f loss AY 2022-23 Rs. 4,20,000; s.79 not triggered; 115BAA interaction flagged — best answer: loss arose after the option year, so set-off is available. |
| A19 | 34 | 194J default on Apex shown; s.201(1A) interest flagged as not computable. |
| A20 | 37, 38, 39, 42, 43 | N/A per client profile. |
| A21 | 40 | Ratios for both years from the FS (GP 39.26% / 38.73%; NP before tax 5.99% / 3.74%; stock 12.32% / 12.55%). |
| A22 | 41 | GST demand Rs. 8,50,000 dated 18-Feb-2026 reported here. |
| A23 | 44 | **Mandatory** for AY 2026-27 — not deferred. Data missing → `missing` with a client query. |

## Part B — Hidden issues a strong run should also find

| # | Clause | What is in the data | Expected handling |
|---|---|---|---|
| B1 | 21(e) | Gratuity provision Rs. 6,50,000 debited; same amount sits as a provision (unfunded). | s.40A(7) disallowance, judgment pending approved-fund evidence. Not double-counted in 43B. |
| B2 | 21(b), 34 | Interest Rs. 5,00,000 to the director — no s.194A entry in the TDS summary. | 30% = Rs. 1,50,000 under s.40(a)(ia). |
| B3 | 21(b), 34 | Rent Rs. 24,00,000 in P&L; 194-I returns show only Q1, Q3, Q4 (Rs. 18,00,000). | Q2 Rs. 6,00,000 → potential Rs. 1,80,000. |
| B4 | 21(b), 34 | Commission Rs. 9,60,000 in P&L; 194H return covers Rs. 2,40,000. | Rs. 7,20,000 uncovered — payee-wise data needed. |
| B5 | 21(b), 34 | All professional fees (Rs. 15,70,000) and audit fee (Rs. 3,00,000) — no 194J at all. | Apex is the confirmed default; the rest is `missing` pending party-wise ledgers. |
| B6 | 23 | Interest Rs. 5,00,000 on a Rs. 3,50,000 loan held 207 days ≈ 252% a year. | Flag as excessive (s.40A(2)(a)) or register incomplete. |
| B7 | 18, recon | Book depreciation Rs. 42,00,000 vs IT Rs. 36,52,500 although the FS says books use IT rates; FAR calls it "rounding". | Rs. 5,47,500 is not rounding; computation adjustment; no additional depreciation under 115BAA. |
| B8 | 27(a), recon | GSTR-9 ITC Rs. 8,16,00,000 vs GSTR-3B total Rs. 81,54,120. | Unexplained — likely keying error; ask for filed GSTR-9. |
| B9 | 21(a) | Club subscription. | Report it; disallowance not automatic (*United Glass*, SC 2012) — judgment. |
| B10 | 21(a) | CSR Rs. 1,80,000 — company is below every s.135 threshold. | Voluntary CSR: Explanation 2 arguably does not apply; conservative disallowance as judgment. |
| B11 | 21(a) | 80GGB for the souvenir advertisement. | Not available — 115BAA bars Chapter VI-A (except 80JJAA/80M). |
| B12 | 34, recon | Two sample Form 16s show TDS Rs. 5,63,000; the s.192 return shows Rs. 4,85,000 for all employees. | Unexplained — return looks incomplete. |
| B13 | 34 | Purchases Rs. 7.37 crore; FY 2024-25 turnover above Rs. 10 crore. | s.194Q applies to suppliers above Rs. 50 lakh — data needed. |
| B14 | recon | TB includes both P&L ledgers and "Profit for the year (transferred)", so it doesn't balance; TB other expenses exceed FS by Rs. 53,000. | Ask for a clean TB tied to signed accounts. |
| B15 | recon, 40 | FS shows a deferred tax credit although DTL rose by Rs. 1,50,000. | Use PBT for ratios; flag. |
| B16 | 16 | Exports of Rs. 1.40 crore but no RoDTEP/drawback/IGST refund in income. | Client query. |
| B17 | recon | AIS names the company itself as the dividend payer. | Flag. |
| B18 | 31 | s.269ST carve-out: the cash loan is covered by 269SS, so it is not also a 269ST breach. | Stated correctly. |
| B19 | 20(b) | Only one month of PF challans is available. | Clause marked `missing` for the other months. |
| B20 | hand-off | AY 2026-27 report due date was 21-Oct-2026 (extended). | If run later, mention s.271B exposure. |

## Part C — Scoring sheet (for training sessions)

- Part A: 2 points each (46). Part B: 1 point each (20). Total 66.
- Minus 5 for each fabricated figure (any number not traceable to a document).
- Minus 3 for each clause silently omitted, and for emitting clause 28 or 29.
- A good first-pass run scores 50+. The reference run in `demo-output/` of the training kit scores 66.

Reference draft impact (net addition to income, duplicates excluded): **Rs. 27,70,500**, of which only Rs. 55,000
(40A(3)) needs no CA judgment.
