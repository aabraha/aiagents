# AI Agents Monorepo

This repository contains AI-related projects and shared setup files.
Use this guide to quickly find the right project and get started.

## Install uv (First Step)

This repository uses [`uv`](https://docs.astral.sh/uv/) for Python environment and package management.

Install `uv`:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```bash
uv --version
```

**Python:** `pyproject.toml` targets **Python 3.12+**. Install shared deps from repo root with `uv sync` (uses `pyproject.toml` and `uv.lock`). The root `requirements.txt` is a compiled export from that manifest (`uv pip compile …`), not a second source of truth.

## Projects

### `deep_research/`
Multi-agent research flow (OpenAI Agents SDK) with a Gradio UI: plan searches, web search, write a report, optional email via SendGrid.

- Entry: `deep_research/deep_research.py` (run with that directory as the working directory so local imports resolve)
- Env: `OPENAI_API_KEY` (required); `SENDGRID_API_KEY` (for the email step). Configure sender/recipient in `deep_research/email_agent.py` as needed.

### `careeragent/`
An AI-powered career chat assistant with a Gradio web UI.

- Main app entry point: `careeragent/career.py`
- Project-specific docs: `careeragent/README.md`
- Project dependencies: `careeragent/requirements.txt`

What it does (high level):
- Uses OpenAI for chat responses
- Loads resume/profile documents for grounded answers
- Can record user contact details and unknown questions

## Repository Structure

```text
aiagents/
  deep_research/            # Deep research Gradio app
  careeragent/              # Career assistant project
  pyproject.toml            # Shared package deps (agents)
  uv.lock                   # Lockfile for uv
  requirements.txt          # Compiled from pyproject.toml (optional pip workflow)
  .gitignore                # Ignore rules for repo
  .env                      # Local environment variables (not for commit)
  .venv/                    # Local virtual environment (generated)
  .gradio/                  # Local Gradio runtime files (generated)
```

## Quick Navigation

- Deep research: `deep_research/deep_research.py`
- Career agent docs: `careeragent/README.md`
- Career app: `careeragent/career.py`
- Career-only deps (with uv): `uv pip install -r careeragent/requirements.txt`

## Getting Started (Deep Research)

From repository root:

```bash
uv sync
cd deep_research
uv run python deep_research.py
```

## Getting Started (Career Agent)

From repository root:

```bash
uv venv
uv pip install -r careeragent/requirements.txt
uv run python careeragent/career.py
```

For full setup details (environment variables, required resource files, and usage), see individual project's 
`README.md`

## Notes

- Keep secrets in `.env` only.
- Avoid committing personal documents or API credentials.
- Each project folder should maintain its own detailed README; this root README is an index for navigation.

## How to Add a New Project

1. Create a new folder at the repository root (for example, `mynewagent/`).
2. Add a project-specific `README.md` inside that folder with setup and usage instructions.
3. Add a project-specific `requirements.txt` (or other dependency manifest) inside that folder.
4. Add the project to the **Projects** section in this root `README.md` with:
   - a one-line description
   - main entry file path
   - link/reference to the internal project README
5. Update `.gitignore` if the new project introduces generated files, local caches, or secrets.

Recommended minimal structure:

```text
mynewagent/
  README.md
  requirements.txt
  main.py
  resources/   # optional
```
