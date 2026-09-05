# Glossary

*Plain-English finance and AI terms for the Variance demo. Northwind Analytics is a synthetic B2B SaaS company; all examples come from its July–August 2026 demo data.*

## Customer tiers

**SMB — Small and midsize business**  
**Definition:** A customer segment made up of smaller organizations than enterprise accounts.  
**Why it matters:** Northwind SMB revenue rose from **$118,000 to $124,510 (+5.5%)**, providing steady secondary growth.

**Enterprise**  
**Definition:** Large customers with higher-value contracts and usually longer sales cycles.  
**Why it matters:** Enterprise revenue rose from **$185,000 to $244,000 (+31.9%)**, the main growth engine.

**Starter**  
**Definition:** The entry-level plan for smaller customers or lighter product use.  
**Why it matters:** Starter revenue fell from **$39,500 to $36,340 (-8.0%)**, revealing weakness hidden by total growth.

## Revenue and cost metrics

**MRR — Monthly recurring revenue**  
**Definition:** Predictable subscription revenue expected in one month.  
**Why it matters:** Six August cancellations created **$2,574 of lost MRR**, more than July’s $1,240.

**ARR — Annual recurring revenue**  
**Definition:** Recurring revenue expressed annually, commonly estimated as MRR multiplied by 12.  
**Why it matters:** Annualizing MRR lets judges see the longer-term scale of a monthly change.

**COGS — Cost of goods sold**  
**Definition:** Direct costs required to deliver the product, such as cloud compute and third-party data.  
**Why it matters:** Northwind COGS rose from **$79,140 to $84,670 (+7.0%)**, slower than revenue.

**OPEX — Operating expenses**  
**Definition:** Costs of running the business that are not directly tied to each sale.  
**Why it matters:** OPEX rose from **$186,000 to $208,320 (+12.0%)**, led by Sales expense at +23.6%.

## Transaction types

**New**  
**Definition:** Revenue from a customer beginning a new paid relationship.  
**Why it matters:** Initech’s **$12,800** August enterprise contract is a clear new-business driver.

**Expansion**  
**Definition:** Additional recurring revenue from an existing customer upgrading or increasing usage.  
**Why it matters:** Acme’s **$18,500** and Globex’s **$14,200** August expansions explain a large share of growth.

**Renewal**  
**Definition:** Recurring revenue from an existing customer continuing its contract.  
**Why it matters:** Renewals provide the baseline the agent separates from genuinely incremental growth.

**Churn**  
**Definition:** Recurring revenue lost when a customer cancels or stops paying.  
**Why it matters:** August recorded **six Starter cancellations and $2,574 of lost MRR**.

---
## Analysis and reliability

**Variance**  
**Definition:** The dollar or percentage difference between two comparable periods or values.  
**Why it matters:** August revenue variance was **+$62,350, or +18.2%**, versus July.

**Driver**  
**Definition:** An underlying customer, transaction, product, or cost that materially caused a variance.  
**Why it matters:** Enterprise added **$59,000**, accounting for nearly all net revenue growth.

**Reconciliation**  
**Definition:** A check that detailed records sum exactly to the reported summary totals.  
**Why it matters:** August tier transactions reconcile to **$404,850**, preventing unsupported explanations.

**Concentration risk**  
**Definition:** Exposure created when results depend heavily on a small number of customers.  
**Why it matters:** Acme, Globex, and Initech produced **$37,760—64.0% of the enterprise increase**.

**NRR — Net revenue retention**  
**Definition:** Starting-customer recurring revenue retained after expansion, contraction, and churn, excluding new customers.  
**Why it matters:** The agent should match customer IDs across periods before calculating NRR, rather than treating new sales as retention.

**PRISM trace**  
**Definition:** A recorded view of an agent run used to observe behavior, identify failures, and prove improvements.  
**Why it matters:** The team can compare traces to show that explanations stay grounded in finance evidence.

**Explain-the-Change**  
**Definition:** Analysis that moves from reporting a variance to proving what caused it and why.  
**Why it matters:** The demo connects **+18.2% revenue** to enterprise deals while surfacing Starter churn and rising Sales OPEX.

## Where the agent adds leverage

- **Exhaustive cross-period review:** It checks all **390 transaction rows** consistently, not only the largest visible lines.

- **Multi-level attribution:** It moves from total revenue to tier, customer, and transaction type, then quantifies each driver’s share.

- **Hidden-signal detection:** It explains that strong overall growth coexists with **Starter revenue down 8.0%** and **lost MRR up 107.6%**.

- **Evidence control:** It reconciles detail to summaries and avoids double-counting the churn memo already reflected in net revenue.

**Core demo takeaway:** Northwind grew quickly, but the quality of that growth depends on a few enterprise accounts while entry-level retention weakened.
