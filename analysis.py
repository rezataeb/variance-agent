"""Deterministic financial analysis core for Variance."""
from __future__ import annotations
import json
from dataclasses import dataclass
import pandas as pd

REQUIRED_SUMMARY = {"category", "sub_category", "amount"}
REQUIRED_TXNS = {"txn_id", "date", "customer_id", "customer_name", "tier", "amount", "type", "payment_method", "region"}

@dataclass
class AnalysisResult:
    metrics: dict
    variances: pd.DataFrame
    customer_drivers: pd.DataFrame
    quality_checks: list[dict]
    memo: str
    trace_steps: list[dict]

    def trace_summary(self) -> dict:
        """PRISM-safe summary: no raw rows, emails, or uploaded file contents."""
        return {
            "metrics": self.metrics,
            "drivers": self.customer_drivers.head(5).to_dict("records"),
            "checks": self.quality_checks,
            "memo": self.memo,
        }


def _validate(summary: pd.DataFrame, txns: pd.DataFrame, label: str) -> None:
    missing_s = REQUIRED_SUMMARY - set(summary.columns)
    missing_t = REQUIRED_TXNS - set(txns.columns)
    if missing_s or missing_t:
        raise ValueError(f"{label}: missing summary columns {sorted(missing_s)}; missing transaction columns {sorted(missing_t)}")
    summary["amount"] = pd.to_numeric(summary["amount"], errors="raise")
    txns["amount"] = pd.to_numeric(txns["amount"], errors="raise")
    txns["date"] = pd.to_datetime(txns["date"], errors="raise")


def _money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def _pct(x: float) -> str:
    return "n/m" if pd.isna(x) else f"{x:+.1f}%"


def analyze(prior_summary, current_summary, prior_txns, current_txns) -> AnalysisResult:
    ps, cs, pt, ct = [x.copy() for x in (prior_summary, current_summary, prior_txns, current_txns)]
    _validate(ps, pt, "Prior period")
    _validate(cs, ct, "Current period")

    p = ps.groupby(["category","sub_category"], as_index=False)["amount"].sum().rename(columns={"amount":"prior"})
    c = cs.groupby(["category","sub_category"], as_index=False)["amount"].sum().rename(columns={"amount":"current"})
    var = p.merge(c, how="outer", on=["category","sub_category"]).fillna(0)
    var["change"] = var.current - var.prior
    var["change_pct"] = var.apply(lambda r: (r.change / abs(r.prior) * 100) if r.prior else float("nan"), axis=1)
    var["abs_change"] = var.change.abs()
    var = var.sort_values("abs_change", ascending=False).drop(columns="abs_change")

    def total(df, cat): return float(df.loc[df.category.eq(cat), "amount"].sum())
    p_rev, c_rev = total(ps,"Revenue"), total(cs,"Revenue")
    rev_change = c_rev-p_rev
    rev_pct = rev_change/p_rev*100 if p_rev else float("nan")
    p_cogs, c_cogs = total(ps,"COGS"), total(cs,"COGS")
    p_opex, c_opex = total(ps,"OPEX"), total(cs,"OPEX")
    p_gm = (p_rev-p_cogs)/p_rev*100 if p_rev else float("nan")
    c_gm = (c_rev-c_cogs)/c_rev*100 if c_rev else float("nan")

    # Customer-period deltas are more defensible than summing growth-tagged events.
    pg = pt.groupby(["customer_id","customer_name","tier"], as_index=False).amount.sum().rename(columns={"amount":"prior"})
    cg = ct.groupby(["customer_id","customer_name","tier"], as_index=False).amount.sum().rename(columns={"amount":"current"})
    drivers = pg.merge(cg, how="outer", on=["customer_id","customer_name","tier"]).fillna(0)
    drivers["change"] = drivers.current-drivers.prior
    drivers["share_of_total_change_pct"] = drivers.change / rev_change * 100 if rev_change else 0
    drivers = drivers.sort_values("change", ascending=False)

    p_tier = ps[ps.category.eq("Revenue")].set_index("sub_category").amount
    c_tier = cs[cs.category.eq("Revenue")].set_index("sub_category").amount
    tiers = sorted(set(p_tier.index)|set(c_tier.index))
    tier_lines=[]
    for tier in tiers:
        a=float(p_tier.get(tier,0)); b=float(c_tier.get(tier,0)); d=b-a
        tier_lines.append((tier,a,b,d,(d/a*100 if a else float('nan'))))
    lead=max(tier_lines,key=lambda x:abs(x[3])) if tier_lines else ("Revenue",0,0,0,float('nan'))

    churn = ct[ct.type.astype(str).str.lower().eq("churn")]
    churn_amt=float(churn.amount.sum())
    top3=drivers[drivers.change.gt(0)].head(3)
    top3_delta=float(top3.change.sum())
    concentration=top3_delta/rev_change*100 if rev_change else 0

    txn_p=float(pt.amount.sum()); txn_c=float(ct.amount.sum())
    checks=[
      {"check":"Prior transactions reconcile to Revenue", "status":"PASS" if abs(txn_p-p_rev)<0.01 else "FAIL", "detail":f"{_money(txn_p)} vs {_money(p_rev)}"},
      {"check":"Current transactions reconcile to Revenue", "status":"PASS" if abs(txn_c-c_rev)<0.01 else "FAIL", "detail":f"{_money(txn_c)} vs {_money(c_rev)}"},
      {"check":"Transaction IDs are unique", "status":"PASS" if pt.txn_id.is_unique and ct.txn_id.is_unique else "FAIL", "detail":f"{len(pt)+len(ct):,} rows tested"},
    ]

    # Stable-dimension test: compare one modal region per customer across periods.
    pm=pt.groupby("customer_id").region.agg(lambda s:s.mode().iloc[0] if not s.mode().empty else "")
    cm=ct.groupby("customer_id").region.agg(lambda s:s.mode().iloc[0] if not s.mode().empty else "")
    matched=pm.index.intersection(cm.index); drift=int((pm.loc[matched] != cm.loc[matched]).sum()) if len(matched) else 0
    drift_rate=drift/len(matched)*100 if len(matched) else 0
    checks.append({"check":"Region labels stable across matched customers", "status":"PASS" if drift==0 else "WARN", "detail":f"{drift}/{len(matched)} changed ({drift_rate:.1f}%)"})

    names=", ".join(top3.customer_name.tolist()) or "No positive customer drivers"
    memo=(
      f"Revenue changed by {_money(rev_change)} ({_pct(rev_pct)}) to {_money(c_rev)}. "
      f"{lead[0]} was the largest tier driver at {_money(lead[3])} ({_pct(lead[4])}). "
      f"The top three positive customer deltas—{names}—contributed {_money(top3_delta)}, "
      f"or {concentration:.1f}% of the total net change. "
      f"Current-period churn contains {len(churn)} transactions totaling {_money(churn_amt)}. "
      f"COGS changed {_pct((c_cogs-p_cogs)/p_cogs*100 if p_cogs else float('nan'))}; gross margin moved "
      f"from {p_gm:.1f}% to {c_gm:.1f}% ({c_gm-p_gm:+.1f} points). "
      + (f"Caution: region changed for {drift_rate:.1f}% of matched customers, so regional conclusions are not decision-grade." if drift else "Customer region labels were stable across periods.")
    )
    metrics={
      "prior_revenue":round(p_rev,2), "current_revenue":round(c_rev,2), "revenue_change":round(rev_change,2),
      "revenue_change_pct":round(rev_pct,2), "prior_cogs":round(p_cogs,2), "current_cogs":round(c_cogs,2),
      "prior_opex":round(p_opex,2), "current_opex":round(c_opex,2), "prior_gross_margin_pct":round(p_gm,2),
      "current_gross_margin_pct":round(c_gm,2), "gross_margin_point_change":round(c_gm-p_gm,2),
      "churn_count":int(len(churn)), "churn_amount":round(churn_amt,2), "top3_concentration_pct":round(concentration,2),
      "region_drift_pct":round(drift_rate,2), "transaction_rows":int(len(pt)+len(ct)),
    }
    steps=[
      {"step_type":"tool_call","label":"Validate and reconcile inputs","tool_name":"pandas","output_summary":json.dumps(checks),"status":"success"},
      {"step_type":"reasoning","label":"Rank variances","output_summary":f"Revenue {_money(rev_change)}; largest tier {lead[0]} {_money(lead[3])}","status":"success"},
      {"step_type":"reasoning","label":"Attribute customer drivers","output_summary":f"Top 3 contribute {concentration:.1f}% of net revenue change","status":"success"},
      {"step_type":"reasoning","label":"Test reliability risks","output_summary":f"Region drift {drift_rate:.1f}% across matched customers","status":"success" if drift==0 else "warning"},
      {"step_type":"final_answer","label":"Produce evidence-backed memo","output_summary":memo,"status":"success"},
    ]
    return AnalysisResult(metrics,var,drivers,checks,memo,steps)
