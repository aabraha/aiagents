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

## Projects

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
  careeragent/              # Career assistant project
  requirements.txt          # Root-level Python dependencies (shared/global)
  .gitignore                # Ignore rules for repo
  .env                      # Local environment variables (not for commit)
  .venv/                    # Local virtual environment (generated)
  .gradio/                  # Local Gradio runtime files (generated)
```

## Quick Navigation

- Open project docs: `careeragent/README.md`
- Run app code: `careeragent/career.py`
- Install project deps (with uv): `uv pip install -r careeragent/requirements.txt`

## Getting Started (Career Agent)

From repository root:

```bash
uv venv
uv pip install -r careeragent/requirements.txt
uv run python careeragent/career.py
```

For full setup details (environment variables, required resource files, and usage), see:
`careeragent/README.md`

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
