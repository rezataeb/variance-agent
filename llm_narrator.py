"""Optional OpenAI-compatible narrator for GIDE/Ornith or a cloud model."""
from __future__ import annotations
import json, os

def configured():
    return bool(os.getenv("OPENAI_BASE_URL") and os.getenv("OPENAI_MODEL"))

def rewrite_with_llm(result):
    """Rewrite only; calculations stay deterministic. Returns memo, model name."""
    if not configured():
        return result.memo, "deterministic-finance-engine"
    from openai import OpenAI
    client=OpenAI(base_url=os.environ["OPENAI_BASE_URL"], api_key=os.getenv("OPENAI_API_KEY","EMPTY"))
    evidence=result.trace_summary()
    prompt=("Write a concise CFO memo (max 130 words) from the JSON evidence. "
            "Use only supplied numbers. Separate facts from hypotheses. Mention any failed/warning checks. JSON:\n"+json.dumps(evidence,default=str))
    response=client.chat.completions.create(model=os.environ["OPENAI_MODEL"], temperature=0, messages=[
      {"role":"system","content":"You are a careful finance analyst. Never invent a cause or number."},
      {"role":"user","content":prompt},
    ])
    return response.choices[0].message.content, os.environ["OPENAI_MODEL"]
