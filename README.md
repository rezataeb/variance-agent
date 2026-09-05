# Variance — Explain the Change

**Money Operations track · Built with GIDE · Observed with PRISM**

Variance is a finance agent that compares two periods, reconciles summary figures to transaction detail, ranks material drivers, and produces a concise explanation with evidence and data-quality guardrails.

> Demo data is synthetic but operationally realistic. It represents Northwind Analytics, a fictional B2B SaaS company, and does not contain real customer data.

## Problem statement

Monthly reporting tells leaders *what* moved, but finding *why* requires manual pivots across summaries and transactions. That process is slow and vulnerable to double counting, denominator errors, unstable dimensions, and confident causal stories that the data cannot prove.

## Solution

Variance follows a repeatable agent workflow:

1. Validate the four input files.
2. Reconcile transaction totals to reported revenue.
3. Rank dollar and percentage variances.
4. Attribute changes to customer-period deltas—not just eye-catching event rows.
5. Test churn, concentration, unit economics, and dimension stability.
6. Produce an executive memo that separates evidence from hypotheses.
7. Submit an aggregate trajectory to PRISM for evaluation and comparison.

## Key features

- Two-period CSV upload with a one-click realistic demo
- Exact summary-to-ledger reconciliation
- Revenue, COGS, OPEX, and gross-margin analysis
- Customer-level driver attribution and top-three concentration
- Churn detection and evidence-linked quality controls
- Region-drift guardrail that blocks unsafe regional conclusions
- Optional GIDE/Ornith or other OpenAI-compatible memo rewrite
- PRISM trajectory submission without sending raw transaction rows
- 390-row synthetic SaaS dataset, glossary, and judge-ready insight guide

## Demo finding

August revenue rises from **$342,500 to $404,850: +$62,350, or +18.2%**. Enterprise is the dominant tier driver, Starter declines, six churn transactions appear, and gross margin improves because COGS grows more slowly than revenue. The agent also detects unstable region labels across matched customers, preventing a plausible but unsafe regional attribution.

## Tech stack

- Python 3.10+
- Streamlit
- pandas
- PRISM via `prismtrace-sdk`
- GIDE / Ornith for local code review and optional OpenAI-compatible narration
- pytest

## Run locally

```bash
git clone https://github.com/rezataeb/variance-agent.git
cd variance-agent
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
streamlit run app.py
```

In the app, select **Use realistic demo** and click **Analyze change**.

## Mandatory tool setup

- **PRISM:** Follow [`PRISM_SETUP.md`](PRISM_SETUP.md). You must set your own key/project ID and run `python run_once.py`; the code cannot do that on your behalf.
- **GIDE:** Follow [`GIDE.md`](GIDE.md). You must open this folder in GIDE and complete at least one reviewed/tested iteration yourself.

## Input schema

Summary CSV columns: `category`, `sub_category`, `amount`; optional `account_count`, `mrr`.

Transaction CSV columns: `txn_id`, `date`, `customer_id`, `customer_name`, `tier`, `amount`, `type`, `payment_method`, `region`; optional `plan`, `contact_email`, `notes`.

## Repository map

- `app.py` — Streamlit product
- `analysis.py` — deterministic finance engine
- `llm_narrator.py` — optional GIDE/Ornith-compatible narration
- `prism_observability.py` — PRISM trajectory integration
- `run_once.py` — required first PRISM run
- `data/` — realistic synthetic demo and data guide
- `docs/` — glossary and deeper agent-advantage analysis
- `tests/` — finance reliability tests
- `DEMO_SCRIPT.md` — 75-second pitch

## Reliability design

Calculations are deterministic; an LLM may rewrite the final explanation but never supplies the numbers. The agent checks reconciliation before explaining results, compares complete customer-period totals, and labels correlation as hypothesis. If a required field is missing or a check fails, the run stops or warns rather than manufacturing a conclusion.

## Limitations

The sample does not contain salesperson, campaign, contract-date, acquisition-cohort, or feature-usage fields. Therefore it can identify correlations and missing evidence but cannot prove those causal explanations. See `docs/AGENT_ADVANTAGE.md` for production-grade extensions.

## Demo 

Video: [https://loom.com/share/](https://www.loom.com/share/44fa5f30f5cb42ccba125fe3c8dc4b7c)

## License

MIT
