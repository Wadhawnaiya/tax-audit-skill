# Self-review checklist and red-flag patterns

Run this after drafting all clauses and before `validate_workpaper.py`. It catches the errors that first-pass
drafts most often make. Fix what you find; do not just note it.

## A. Integrity (a failure here makes the workpaper unusable)

- [ ] Every number in an answer or table can be pointed to in a source document (inventory ref + sheet/row or
      page). If you cannot point to it, it is `missing`, not `filled`.
- [ ] No clause 28 or 29 (omitted by Notification 23/2025). Clause 36B is present.
- [ ] Every canonical clause is present — N/A ones with a reason.
- [ ] Every `judgment` and `missing` clause has notes; every `missing` clause has a `client_query`.
- [ ] Each disallowance is in `impact` once. If the same amount is disclosed in two clauses (43B(h) in 22 and 26;
      gratuity in 21(e) not 26), the second entry carries `double_count_of`.
- [ ] The period is FY 2025-26 / AY 2026-27. A later period → stop (Form 26, see `form-26-transition.md`).

## B. The ten most common misses (check each one explicitly)

1. **Employee PF/ESI paid late** — s.36(1)(va), no grace period, permanently disallowed. Employer share is 43B.
2. **MSME dues overdue at 31 March** — s.43B(h), no return-due-date relief; report in clauses 22 AND 26.
3. **TDS gaps found only by comparing ledgers with returns** — rent quarters, commission, professional fees,
   interest to directors/relatives, director sitting fees, 194Q on purchases.
4. **Unfunded gratuity / leave provisions** — s.40A(7) (gratuity); leave encashment is 43B(f).
5. **Cash** — payments over Rs. 10,000 (40A(3)); loans/deposits over Rs. 20,000 (269SS/269T, clause 31 code A/B);
   receipts of Rs. 2 lakh or more (269ST).
6. **Related-party payments** — list them all in clause 23; test reasonableness (implied interest rate,
   remuneration vs. role).
7. **Book vs tax depreciation** — half rate for <180 days; block reduced by sale proceeds; no additional
   depreciation under 115BAA/115BAB.
8. **Prior-period items** — clause 27(b); deductible only if the liability crystallised this year.
9. **Penalties, political advertisements, CSR, club fees** — clause 21(a); know which are automatic
   (s.37(2B), penalties for offences) and which need judgment (club subscriptions, voluntary CSR, GST late fees).
10. **Regime consequences** — 115BAA/115BAB/115BAC: no Chapter VI-A (except 80JJAA/80M for companies), no additional
    depreciation, loss set-off restrictions only for losses from specified deductions before the option year.

## C. Red flags that should make you dig, not move on

- A client note that "explains" a difference as rounding when the amount is material.
- A sample (Form 16, invoices) that is larger than the population total it belongs to.
- An accounting-policy note that contradicts the numbers.
- A register that is "complete" but has one quarter, one month or one party missing.
- AIS/TIS entries that name odd payers, or income in AIS that is not in the books.
- Year-end statutory dues payable with no evidence of payment.
- An exporter with no export incentives, refunds or drawback in income.
- Interest paid that is large relative to the loan balance shown.

## D. Language

- Answers are written as they will be typed into the utility: short, factual, figures in Indian format
  (12,34,567), dates as DD-MMM-YYYY.
- Notes explain the call in plain words: the fact, the rule, the conclusion, what would change it.
- Never state a penalty amount (271D, 271B, 271H…) — flag the exposure only.
