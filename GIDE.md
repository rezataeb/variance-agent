# GIDE workflow — the part you must do yourself

GIDE must be used on your computer; including this file alone is not proof of use.

## Required proof-of-use flow

1. Install/open GIDE and choose **Open Folder**.
2. Select the unzipped `variance-agent` folder.
3. Open GIDE's integrated terminal and run the setup commands from the README.
4. Give GIDE/Ornith this task:

```text
Review analysis.py and tests/test_analysis.py for finance reliability. Preserve exact reconciliation, add no unsupported causal claims, and run pytest. Explain any change before writing it.
```

5. Approve one useful edit only after reviewing the plan, then run `pytest -q` again.
6. Keep the resulting source change in your Git commit. Save one screenshot of GIDE showing the repo and successful test for your submission evidence.

## Optional local narration

Variance can call any OpenAI-compatible endpoint. If GIDE exposes its local Ornith model through such an endpoint, use the base URL and model name shown by GIDE rather than guessing:

```bash
export OPENAI_BASE_URL="value shown by GIDE"
export OPENAI_API_KEY="EMPTY"
export OPENAI_MODEL="model name shown by GIDE"
streamlit run app.py
```

If the endpoint is not enabled, the app remains fully functional using its deterministic evidence engine. In your pitch, distinguish the deterministic calculations from the optional LLM rewrite.
