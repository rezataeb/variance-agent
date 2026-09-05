from pathlib import Path
import pandas as pd
from analysis import analyze
D=Path(__file__).parents[1]/"data"
def test_demo_reconciles_and_finds_signal():
 f=["monthly_summary_2026-07.csv","monthly_summary_2026-08.csv","transactions_2026-07.csv","transactions_2026-08.csv"]
 r=analyze(*[pd.read_csv(D/x) for x in f])
 assert r.metrics["revenue_change"]==62350
 assert round(r.metrics["revenue_change_pct"],1)==18.2
 assert all(x["status"]=="PASS" for x in r.quality_checks[:3])
 assert r.metrics["transaction_rows"]==390
 assert r.metrics["region_drift_pct"]>0
