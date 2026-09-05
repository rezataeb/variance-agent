"""PRISM integration. Only aggregated evidence is sent; raw CSV rows are not."""
from __future__ import annotations
import os
from prismtrace import PRISMtrace


def prism_configured() -> bool:
    return all(os.getenv(k) for k in ("PRISM_API_KEY", "PRISM_PROJECT_ID"))


def submit_to_prism(result):
    if not prism_configured():
        return {"sent":False, "message":"Set PRISM_API_KEY and PRISM_PROJECT_ID first."}
    client=PRISMtrace(
        api_key=os.environ["PRISM_API_KEY"],
        host=os.getenv("PRISM_HOST", "https://prism.blockconvey.com"),
        project_id=os.environ["PRISM_PROJECT_ID"],
    )
    response=client.submit_trajectory(
        result.trace_steps,
        agent_id="variance-explain-change-v1",
        agent_name="Variance — Explain the Change",
        model=os.getenv("VARIANCE_MODEL", "deterministic-finance-engine"),
        final_status="success",
        async_send=False,
    )
    if response is None:
        return {"sent":False, "message":"PRISM did not confirm receipt. Check terminal warnings, host, key, and project ID."}
    return {"sent":True, "message":"PRISM confirmed the trajectory.", "response":response}
