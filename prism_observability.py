import os, httpx
def prism_configured(): return True
def submit_to_prism(result):
    key=os.getenv("BLOCKCONVEY_API_KEY")
    pid=os.getenv("BLOCKCONVEY_PROJECT_ID")
    if not key or not pid:
        return {"sent":False,"message":"Export BLOCKCONVEY_API_KEY and PROJECT_ID first"}
    headers={"X-PRISMtrace-Key": key, "Content-Type":"application/json"}
    payload={"project_id": pid, "input_messages":[{"role":"user","content":"July vs Aug variance"}],"output_message":str(result.memo)[:4000],"model":"deterministic-finance-engine","agent_name":"Variance — Explain the Change","latency_ms":1200}
    try:
        r=httpx.post("https://prism.blockconvey.com/api/traces", headers=headers, json=payload, timeout=15)
        if r.status_code in (200,201,202):
            return {"sent":True,"message":f"PRISM confirmed {r.status_code}"}
        return {"sent":False,"message":f"PRISM {r.status_code}: {r.text[:300]}"}
    except Exception as e:
        return {"sent":False,"message":f"PRISM error {e}"}
