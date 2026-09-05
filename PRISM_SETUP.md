# PRISM setup — the part you must do yourself

The code is integrated, but **no trace has been sent yet** because your API key and project ID must stay private.

## 1. Find your credentials

Open the PRISM dashboard at `https://prism.blockconvey.com`. Create or select a project. Copy its API key and project ID from the project/settings area. If the labels differ in your dashboard, use PRISM's hackathon support channel rather than guessing.

## 2. Set credentials only in the terminal

macOS/Linux:

```bash
export PRISM_API_KEY="paste-your-key"
export PRISM_PROJECT_ID="paste-your-project-id"
export PRISM_HOST="https://prism.blockconvey.com"
```

Windows PowerShell:

```powershell
$env:PRISM_API_KEY="paste-your-key"
$env:PRISM_PROJECT_ID="paste-your-project-id"
$env:PRISM_HOST="https://prism.blockconvey.com"
```

Never paste a real key into the source files, README, screenshots, demo video, or GitHub. `.env` is ignored by Git.

## 3. Produce the required first trace

With the virtual environment activated:

```bash
python run_once.py
```

Success means the terminal prints `PRISM confirmed the trajectory.` Then open PRISM and verify the trajectory named **Variance — Explain the Change** appears. The script exits with an error if PRISM did not confirm receipt.

## 4. Use PRISM in the live demo

Run `streamlit run app.py`. Because the credentials are present, **Send run to PRISM** will be enabled and checked. Analyze the demo, then show the PRISM confirmation line at the bottom. If PRISM is temporarily unavailable, the finance analysis still completes and reports that tracing was not confirmed.

## What gets sent

Only aggregate metrics, ranked-driver summaries, quality-check results, and the final memo are sent. Raw CSV rows and contact emails are not included in the trajectory.

## Observe → Improve → Prove demo

1. **Observe:** Run once and inspect the warning about unstable region labels.
2. **Improve:** In GIDE, add or refine a guardrail that prevents regional attribution when labels drift.
3. **Prove:** Run again and compare PRISM trajectories; show that the final answer now separates evidence from unsupported causation.
