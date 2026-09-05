# Start here: empty GitHub repo → working submission

Your GitHub repository already exists and is empty. **Do not click “creating a new file,” and do not add a second README.** Use one of the two routes below.

## Route A — easiest: GitHub Desktop

1. Download `variance-agent-github-ready.zip` and unzip it to a temporary folder.
2. On the empty repo page, click **Set up in Desktop** and allow GitHub Desktop to open.
3. Choose a local path and click **Clone**. This creates an empty local `variance-agent` folder linked to your repo.
4. Copy the **contents** of the unzipped bundle into that cloned folder. `README.md` must sit directly inside the cloned folder—not inside another `variance-agent` subfolder.
5. Return to GitHub Desktop. Review the changed files.
6. Summary: `Initial Variance hackathon build`
7. Click **Commit to main**, then **Push origin**.
8. Refresh the GitHub page. You should see `README.md`, `app.py`, `analysis.py`, `data/`, `docs/`, and the other files.

## Route B — terminal

1. Download and unzip the bundle.
2. Open Terminal and clone the empty repository:

```bash
git clone https://github.com/rezataeb/variance-agent.git
cd variance-agent
```

3. Copy the unzipped bundle's **contents** into this folder.
4. Then run:

```bash
git add .
git commit -m "Initial Variance hackathon build"
git push -u origin main
```

GitHub may ask you to sign in. Use the normal browser/GitHub credential flow; do not put credentials in a source file.

## When to push

Push once now after copying the starter bundle. Then use GIDE and PRISM locally. Push a second time after the GIDE-reviewed edit and successful PRISM run:

```bash
git add .
git commit -m "Validate finance guardrails with GIDE and PRISM"
git push
```

Do **not** commit your PRISM key, `.env`, screenshots containing secrets, or local virtual environment.
