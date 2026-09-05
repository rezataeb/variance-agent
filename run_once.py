"""Run the demo once and submit a trajectory to PRISM."""
from pathlib import Path
import pandas as pd
from analysis import analyze
from prism_observability import submit_to_prism
D=Path(__file__).parent/"data"
files=["monthly_summary_2026-07.csv","monthly_summary_2026-08.csv","transactions_2026-07.csv","transactions_2026-08.csv"]
result=analyze(*[pd.read_csv(D/f) for f in files])
print(result.memo)
status=submit_to_prism(result)
print("\nPRISM:",status["message"])
if not status.get("sent"): raise SystemExit(1)
