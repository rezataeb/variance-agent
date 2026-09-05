from pathlib import Path
import pandas as pd
import streamlit as st
from analysis import analyze
from llm_narrator import rewrite_with_llm, configured as llm_configured
from prism_observability import submit_to_prism, prism_configured

st.set_page_config(page_title="Variance", page_icon="∆", layout="wide")
st.markdown("""<style>
.block-container{max-width:1120px;padding-top:2rem}.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(135deg,#0b1f36,#123d4f);color:#f7fbff;margin-bottom:1rem}.hero h1{margin:0;font-size:2.4rem}.hero p{color:#cce5ee;margin:.35rem 0 0}.pill{display:inline-block;padding:.25rem .65rem;border-radius:999px;background:#1b6b75;color:white;font-size:.8rem;margin-right:.35rem}
[data-testid="stMetric"]{border:1px solid #dbe6e8;padding:1rem;border-radius:14px}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="pill">Money Operations</span><span class="pill">PRISM traced</span><h1>Variance</h1><p>Explain what changed, why it changed, and which claims are safe to trust.</p></div>',unsafe_allow_html=True)

DATA=Path(__file__).parent/'data'
with st.sidebar:
    st.subheader("Data source")
    mode=st.radio("Choose input",["Use realistic demo","Upload four CSVs"])
    send_trace=st.checkbox("Send run to PRISM",value=prism_configured(),disabled=not prism_configured())
    st.caption("PRISM configured ✓" if prism_configured() else "PRISM needs API key + project ID")
    st.caption("GIDE/Ornith narrator configured ✓" if llm_configured() else "Deterministic memo mode")

if mode=="Upload four CSVs":
    a=st.file_uploader("Prior summary",type="csv"); b=st.file_uploader("Current summary",type="csv")
    c=st.file_uploader("Prior transactions",type="csv"); d=st.file_uploader("Current transactions",type="csv")
    ready=all([a,b,c,d])
else:
    ready=True

if st.button("Analyze change",type="primary",disabled=not ready,use_container_width=True):
    try:
      if mode=="Use realistic demo":
        frames=[pd.read_csv(DATA/f) for f in ["monthly_summary_2026-07.csv","monthly_summary_2026-08.csv","transactions_2026-07.csv","transactions_2026-08.csv"]]
      else: frames=[pd.read_csv(x) for x in [a,b,c,d]]
      result=analyze(*frames)
      memo, model=rewrite_with_llm(result)
      if model!="deterministic-finance-engine":
        result.trace_steps[-1]["output_summary"]=memo
      st.session_state["result"]=(result,memo,model)
      st.session_state["trace_status"]=submit_to_prism(result) if send_trace else {"sent":False,"message":"Trace not requested for this run."}
    except Exception as e: st.error(f"Analysis stopped safely: {e}")

if "result" in st.session_state:
    r,memo,model=st.session_state["result"]; m=r.metrics
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Current revenue",f"${m['current_revenue']:,.0f}",f"{m['revenue_change_pct']:+.1f}%")
    c2.metric("Revenue change",f"${m['revenue_change']:,.0f}")
    c3.metric("Gross margin",f"{m['current_gross_margin_pct']:.1f}%",f"{m['gross_margin_point_change']:+.1f} pts")
    c4.metric("Top-3 concentration",f"{m['top3_concentration_pct']:.1f}%")
    st.subheader("Executive explanation")
    st.info(memo); st.caption(f"Narrator: {model}")
    left,right=st.columns([1.15,1])
    with left:
      st.subheader("Ranked variances")
      show=r.variances.copy(); show["change_pct"]=show.change_pct.map(lambda x:f"{x:+.1f}%" if pd.notna(x) else "n/m")
      st.dataframe(show,hide_index=True,use_container_width=True)
    with right:
      st.subheader("Top customer drivers")
      st.dataframe(r.customer_drivers[["customer_name","tier","prior","current","change","share_of_total_change_pct"]].head(8),hide_index=True,use_container_width=True)
    st.subheader("Evidence controls")
    for q in r.quality_checks:
      icon={"PASS":"✅","WARN":"⚠️","FAIL":"❌"}[q["status"]]
      st.write(f"{icon} **{q['check']}** — {q['detail']}")
    ts=st.session_state.get("trace_status",{})
    st.caption(("PRISM: " if ts.get("sent") else "PRISM status: ")+ts.get("message","Not run"))
    st.download_button("Download analysis JSON",data=str(r.trace_summary()),file_name="variance-analysis.txt")
else:
    st.markdown("### Demo path")
    st.write("Use the preloaded two-month SaaS dataset, run the agent, then show the revenue lift, concentrated drivers, margin gain, and regional data-quality warning.")
