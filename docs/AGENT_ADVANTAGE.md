# Agent Advantage Insights

## Why this analysis matters

A useful finance agent should do more than produce a persuasive explanation. It should reconcile totals, trace every claim to source rows, separate evidence from hypotheses, and reject narratives the data cannot support.

This review uses the **Northwind Analytics synthetic demo dataset**: 390 transactions across July and August 2026, plus monthly account summaries.

- Revenue increased from **$342,500 to $404,850**: **+$62,350, or +18.2%**.
- Enterprise increased from **$185,000 to $244,000**: **+$59,000, or +31.9%**.
- SMB increased from **$118,000 to $124,510**: **+$6,510, or +5.5%**.
- Starter decreased from **$39,500 to $36,340**: **-$3,160, or -8.0%**.

> **Agent advantage:** Several plausible-sounding candidate insights do not match the underlying files. Catching those discrepancies before they reach executives is itself a high-value finance control.

---

## 1. Revenue growth is concentrated in three customers

**What the agent found:** On a complete customer-period basis, Acme, Globex, and Initech contributed **$37,760** of the Enterprise increase. That equals **64.0% of Enterprise growth** and **60.6% of the total company revenue increase**.

**Evidence:**

- Acme: $18,640 in July to $33,500 in August = **+$14,860**
- Globex: $16,100 in July to $26,200 in August = **+$10,100**
- Initech: $0 in July to $12,800 in August = **+$12,800**
- Net customer-period contribution: $14,860 + $10,100 + $12,800 = **$37,760**
- $37,760 / $59,000 Enterprise lift = **64.0%**
- $37,760 / $62,350 total company lift = **60.6%**

**Reliability check:** The three highlighted August event rows total **$45,500**, but event value is not the same as cross-period contribution. The agent uses complete customer-period totals to avoid overstating the net driver.

**Why a human might miss it:** A manual review can sum the three visible event rows and divide by Enterprise growth. The agent joins both months by customer before calculating contribution.

**Business implication:** Growth is real but concentrated. Forecasts should include a scenario that excludes these three customer deltas, and customer-success coverage should prioritize their adoption and renewal risk.

---

## 2. Enterprise growth transactions cluster in mid-August

**What the agent found:** From August 5 through August 18, six Enterprise new or expansion transactions generated **$60,582**, or **60.7%** of all August Enterprise growth-transaction value. Looking only at expansions, three transactions generated **$35,869**, or **74.7%** of expansion value.

**Evidence:**

- `TXN-202608-0005` — Initech: $12,800 on Aug 5
- `TXN-202608-0037` — Seaboard Renewables: $5,739 on Aug 11
- `TXN-202608-0002` — Acme Corp: $18,500 on Aug 12
- `TXN-202608-0035` — Oakridge Pharmacy: $6,174 on Aug 14
- `TXN-202608-0008` — Redwood Manufacturing: $3,169 on Aug 16
- `TXN-202608-0004` — Globex: $14,200 on Aug 18
- Window sum: **$60,582**; all August Enterprise new plus expansion value: **$99,824**
- Expansion-only window: **$35,869**; all Enterprise expansion value: **$48,048**

**Context test:** Total OPEX increased **12.0%**, while Sales OPEX increased from **$74,000 to $91,460**, or **23.6%**. This is consistent with investment in sales, but the data contains no hiring dates or salesperson attribution. “Sales hiring caused the cluster” is a hypothesis, not a proven fact.

**Why a human might miss it:** The pattern requires filtering by tier and transaction type, applying a date window, summing two cohorts, and comparing the result with summary-level expense movement.

**Business implication:** Add salesperson, campaign, and pipeline-stage fields. If the timing link holds, management can estimate sales-investment payback instead of relying on correlation.

---

## 3. Starter churn is visible, but the proposed common cause is not

**What the agent found:** Six August Starter churn transactions total **-$2,574** in recorded lost MRR. All use the `Starter Monthly` plan, but their amounts range from **-$298 to -$568** and their notes show six different stated reasons.

**Evidence:**

- `TXN-202608-0117` — -$298; budget freeze
- `TXN-202608-0118` — -$351; business closed
- `TXN-202608-0119` — -$407; switched vendor
- `TXN-202608-0120` — -$438; low usage
- `TXN-202608-0121` — -$512; seasonal pause
- `TXN-202608-0122` — -$568; payment failure
- Total: **-$2,574**

**Reliability check:** The files do not contain acquisition date, promotion, quoted price, or feature-usage fields. Therefore, the claims that all six came from an April $39 promotion and that five of six used the same feature cannot be tested from this dataset.

**Why a human might miss it:** A reviewer may infer a common cause from six records appearing together. The agent checks whether the required causal fields actually exist before making the claim.

**Business implication:** Join billing data to `acquisition_date`, `campaign_id`, contracted MRR, and feature-usage logs. Then test whether the April cohort’s churn rate is statistically different from other cohorts.

---

## 4. Payment mix changed, but ACH did not increase

**What the agent found:** Enterprise ACH usage increased in absolute dollars but declined as a share of Enterprise activity. Wire and Corporate Card gained share instead.

**Evidence:**

- July Enterprise rows: `TXN-202607-0001` through `TXN-202607-0030`
- August Enterprise rows: `TXN-202608-0001` through `TXN-202608-0040`
- ACH transaction share: **63.3% to 55.0%**
- ACH revenue share: **63.2% to 53.2%**
- ACH dollars: **$116,940 to $129,762**
- Wire revenue share: **19.9% to 24.7%**
- Corporate Card revenue share: **16.9% to 22.1%**

**Reliability check:** The proposed shift from **12% to 28% ACH** is not present under either transaction-count share or dollar share. Payment method alone also does not prove deal quality.

**Why a human might miss it:** Absolute ACH dollars rose, which can create the impression that ACH gained importance. The agent distinguishes absolute growth from mix share and checks both count- and value-weighted definitions.

**Business implication:** Investigate whether more large accounts are paying by Wire or Corporate Card and whether this affects processing cost, cash timing, failed-payment risk, or contract quality.

---

## 5. The regional outlier exposes a data-quality problem

**What the agent found:** West SMB revenue increased **12.0%**, not 18%. The actual outlier is Southwest, up **131.5%**, from **$14,776 to $34,205**. However, regional attribution is unreliable because **51 of 65 matched SMB customers changed region between months**.

**Evidence:**

- West: $25,361 to $28,392 = **+$3,031, or +12.0%**
- Southwest: $14,776 to $34,205 = **+$19,429, or +131.5%**
- Sixteen matched customers moved into Southwest, contributing **$25,961** of August revenue there.
- Examples: `TXN-202607-0051` -> `TXN-202608-0061`, `TXN-202607-0068` -> `TXN-202608-0078`, and `TXN-202607-0073` -> `TXN-202608-0083`
- Region changed for **78.5%** of matched SMB customers: 51 / 65.

**Reliability check:** No `partner_referral` or acquisition-source field exists, so partner attribution cannot be proven. The region field appears unstable and should not drive executive action until corrected.

**Why a human might miss it:** A pivot table highlights Southwest growth but not dimension drift. The agent joins customers across periods and validates whether the grouping key remains stable.

**Business implication:** Fix region master data before allocating budget or sales capacity. Store customer region in a governed dimension table and add referral-source fields if channel attribution matters.

---

## 6. Unit economics improved despite higher COGS

**What the agent found:** Revenue grew **18.2%**, while total COGS grew **7.0%**, from **$79,140 to $84,670**. Gross margin improved from **76.9% to 79.1%**, a gain of **2.2 percentage points**.

**Evidence:**

- Cloud compute: $42,170 to $45,890 = **+8.8%**
- Third-party data: $28,740 to $30,210 = **+5.1%**
- Payment processing: $8,230 to $8,570 = **+4.1%**
- Total COGS: $79,140 to $84,670 = **+$5,530, or +7.0%**
- July gross margin: ($342,500 - $79,140) / $342,500 = **76.9%**
- August gross margin: ($404,850 - $84,670) / $404,850 = **79.1%**
- Infra OPEX: $36,000 to $36,660 = **+1.8%**

**Reliability check:** The **4.1%** figure applies only to payment-processing COGS, not total COGS. The data supports operating leverage, but it does not prove that usage-based infrastructure or Starter decline caused it.

**Why a human might miss it:** Revenue and expense lines sit in separate summary sections. The agent recomputes category totals, compares growth rates, and translates the result into margin movement.

**Business implication:** Enterprise growth appears accretive to gross margin. Finance should confirm cost allocation and track gross margin by tier before changing pricing or infrastructure commitments.

---

## Depth of data

This dataset is meaningful for a hackathon demo because it supports both financial reconciliation and transaction-level investigation.

- **390 transaction rows:** 180 in July and 210 in August.
- **Exact reconciliation:** Transaction totals equal monthly revenue summaries: $342,500 and $404,850.
- **Three customer tiers:** Enterprise, SMB, and Starter, each with a different amount profile.
- **Four transaction types:** Renewal, new, expansion, and churn.
- **Three payment methods:** ACH, Corporate Card, and Wire.
- **Five regions:** Midwest, Northeast, Southeast, Southwest, and West.
- **Uneven amounts:** Values range from -$568 to $18,640, with a $1,157.50 median; this avoids toy-data uniformity.
- **Mixed evidence levels:** Structured fields support arithmetic, while notes add context that must not be mistaken for proof.
- **Cross-period continuity:** 169 customers appear in both months, enabling cohort and dimension-stability checks.
- **Intentional analytical friction:** Concentrated growth, churn, changing payment mix, and unstable regional labels give the agent opportunities to detect both business drivers and data-quality risk.

### What would make it production-grade

Add stable customer dimensions, contract start and renewal dates, salesperson and campaign IDs, acquisition cohort, feature-usage events, invoice status, refunds, currency, and cost allocation by customer. These additions would let the agent test causality and retention quality rather than merely identify correlations.

---

## Technical terms in plain English

**ACH:** Automated Clearing House. A bank-to-bank electronic payment method commonly used for invoices and payroll.

**COGS:** Cost of goods sold. Direct costs required to deliver the service, such as cloud compute, third-party data, and payment processing.

**OPEX:** Operating expenses. Costs of running the business that are not assigned directly to each sale, such as Sales, Marketing, Support, and internal Infrastructure.

**SMB:** Small and medium-sized business. In this dataset, it is the customer tier between Starter and Enterprise.

**MRR:** Monthly recurring revenue. Subscription revenue expected to repeat each month. Lost MRR is recorded as a negative amount when a customer churns.

**Churn:** Customer or recurring-revenue loss caused by cancellation, non-renewal, or failed payment.

**Renewal:** Revenue from an existing customer continuing its contract or subscription.

**Expansion:** Additional revenue from an existing customer, such as more seats, regions, or product modules.

**Revenue lift:** The dollar increase from one period to another. Here, August revenue minus July revenue equals a $62,350 lift.

**Variance:** The difference between actual values across periods, budgets, forecasts, or categories.

**Driver attribution:** Connecting a high-level change to the transactions, customers, products, or operational events that produced it.

**Concentration risk:** Dependence on a small number of customers or transactions. Losing one can materially change the reported result.

**Gross margin:** Revenue remaining after COGS, expressed as a percentage of revenue.

**Percentage point:** The arithmetic difference between two percentages. Moving from 76.9% to 79.1% is a 2.2-point gain, not 2.2% growth.

**Mix share:** A category’s portion of a total. ACH dollars can rise while ACH mix share falls if total Enterprise revenue grows faster.

**Outlier:** A result that differs sharply from the surrounding pattern and deserves investigation.

**Cohort:** A group sharing a starting condition, such as customers acquired in the same month or campaign.

**Reconciliation:** Proving that detailed records sum exactly to the reported financial totals.

**Dimension drift:** A supposedly stable label, such as customer region, changing across periods and distorting comparisons.

**Correlation vs. causation:** Two changes can happen together without one producing the other. Sales expense and deal timing may correlate, but hiring records are needed to establish causation.

---

## Judge-ready conclusion

The strongest result is not a longer narrative; it is a more defensible one. This agent can explain the 18.2% revenue increase, identify the transactions behind it, expose concentration and margin effects, and stop unsupported claims from becoming executive “facts.” Every accepted conclusion has a calculation path, while every causal hypothesis names the additional data needed to prove it.
