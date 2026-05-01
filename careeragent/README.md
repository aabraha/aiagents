# Career Assistant

A Python application that runs an AI-powered **career chat assistant** in the browser. It uses the OpenAI API with function calling, ingests your resume and profile documents for grounded answers, and can notify you (via [Pushover](https://pushover.net/)) when visitors leave contact details or ask questions the model cannot answer.

## Features

- **Gradio web UI** — Chat interface served locally (default Gradio behavior: accessible URL printed on startup).
- **Context from your materials** — Text is loaded from a short summary and from PDFs (LinkedIn export, resume, behavioral prep). Content is included in the system prompt so replies stay consistent with your background.
- **Tool use** — The model can call:
  - `record_user_details` — Log name, email, and notes (and send a Pushover message).
  - `record_unknown_question` — Log questions the assistant could not answer.
- **Model** — `gpt-4o-mini` via the OpenAI Chat Completions API.

## Requirements

- **Python 3.10+** (3.13 is used in development)
- An **OpenAI API key** with access to the configured model
- Optional: a **Pushover** account and app for mobile/desktop notifications (for the recording tools)

## Install uv

This project uses [`uv`](https://docs.astral.sh/uv/) for Python environment and package management.

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

## Setup

### 1. Clone and create a virtual environment

```bash
cd aiagents
cd careeragent
uv venv
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Environment variables

Create a `.env` file in the project root (this file should not be committed if it contains secrets).

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | **Yes** | Authentication for the OpenAI API. |
| `PUSHOVER_USER` | For notifications | Pushover user key. |
| `PUSHOVER_TOKEN` | For notifications | Pushover application token. |

If Pushover variables are missing, `record_user_details` and `record_unknown_question` may still run but notification requests to Pushover can fail.

**Example `.env`:**

```env
OPENAI_API_KEY=sk-...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

### 4. Resource files

Place the following under `careeragent/resources/` (paths and names must match what `careeragent/career.py` expects):

| File | Role |
|------|------|
| `summary.txt` | High-level background text used in the system prompt. |
| `my-linkedin-profile.pdf` | LinkedIn content as PDF. |
| `Abraha_Assefa_resume.pdf` | Resume. |
| `behavioral.pdf` | Behavioral Q&A (first document). |
| `behv2.pdf` | Additional behavioral content (appended to the first). |

These files often contain personal or proprietary information-keep them out of public repositories or use a private remote and/or `.gitignore` as appropriate.

## Run

With the virtual environment available and `resources/` in place:

```bash
uv run python career.py
```

Gradio will start a local server and print a URL (for example `http://127.0.0.1:7860`). Open that address in a browser to use the chat UI titled **"Assefa Abraha's Career Assistant"**.

## Project layout

```text
aiagents/
  careeragent/
    career.py           # App entry: Career class, tools, Gradio launch
    requirements.txt    # Python dependencies
    resources/          # PDFs and summary.txt (you supply)
  .env                  # API keys and secrets (local only)
```

## Dependencies (see `careeragent/requirements.txt`)

- `openai` - API client
- `gradio` - Web chat UI
- `pypdf` - Read text from PDFs
- `python-dotenv` - Load `.env`
- `requests` - HTTP (Pushover)
- `openai-agents` - Declared for compatibility or future use; the current script does not import it

## License

Add a `LICENSE` file and describe terms here if you distribute this project.

## Author

The assistant is configured in code to represent **Assefa Abraha**; update names, file paths, and `Career` class fields if you adapt this for another person or site.
