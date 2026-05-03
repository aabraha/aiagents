# Deep Research

An automated research assistant that turns a natural-language topic into a structured, multi-section report. The application combines the **OpenAI Agents SDK** (orchestration, structured outputs, and hosted web search) with a **Gradio** interface for interactive use.

## Overview

You submit a research question or topic. The system:

1. **Plans** a fixed set of complementary web searches tuned to your query.
2. **Executes** those searches in parallel via the model’s web search tool.
3. **Synthesizes** a long-form Markdown report with summary and follow-up suggestions.
4. **Delivers** the report by email (SendGrid), in addition to showing progress and the final report in the UI.

Each run is associated with an **OpenAI trace** so you can inspect agent behavior in the OpenAI platform when debugging or tuning prompts.

## Architecture

| Component | Role |
|-----------|------|
| `deep_research.py` | Gradio app: loads environment, validates input, streams pipeline output to the UI. |
| `research_manager.py` | Coordinates the pipeline: tracing, planning, parallel search, writing, email. |
| `planner_agent.py` | Produces a typed search plan (`WebSearchPlan`: queries + rationale). |
| `search_agent.py` | Runs hosted **web search** and returns concise summaries per query. |
| `writer_agent.py` | Produces structured `ReportData` (summary, Markdown body, follow-ups). |
| `email_agent.py` | Formats and sends HTML email via SendGrid. |

**Execution flow**

```text
User query → Planner (structured plan) → N parallel search agents → Writer (report) → Email agent → UI
```

Search breadth is configured in `planner_agent.py` (`HOW_MANY_SEARCHES`, currently five distinct queries per run).

## Requirements

- **Python 3.12+** (aligned with the parent repository’s `pyproject.toml`).
- **OpenAI API access** for the models and tools used by the Agents SDK (including web search).
- **SendGrid** API key if you use the email step (see below).

Dependencies are declared at the **repository root** (`pyproject.toml` / `uv.lock`). This folder does not ship a separate `requirements.txt`.

## Configuration

### Environment variables

Create a `.env` file in the repository root or export variables in your shell:

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | Authenticates OpenAI API and Agents SDK usage. |
| `SENDGRID_API_KEY` | For email | Used by `email_agent.py` to send the report. |

The app calls `load_dotenv(override=True)` from `deep_research.py`, so standard `.env` loading applies when you run from the monorepo layout described below.

### Email sender and recipient

Verified sender address, recipient, and any copy logic should be adjusted in `email_agent.py` to match your SendGrid setup and policies. The pipeline assumes email delivery is desired on every successful report; if you need optional email or different routing, extend `ResearchManager.send_email` accordingly.

## Installation and run

From the **repository root** (parent of this directory):

```bash
uv sync
cd deep_research
uv run python deep_research.py
```

**Important:** Run with `deep_research` as the current working directory so imports such as `research_manager` resolve correctly.

The Gradio app launches in your browser. Submit a non-empty topic string; the report area will stream status messages, the trace URL, and finally the Markdown report.

## Observability

On each run, `research_manager.py` prints and surfaces a link of the form:

`https://platform.openai.com/traces/trace?trace_id=…`

Use this to review steps, tool calls, and latency inside the OpenAI trace viewer.

## Project layout

```text
deep_research/
  README.md              # This file
  deep_research.py       # Gradio entrypoint
  research_manager.py    # Pipeline orchestration
  planner_agent.py       # Search planning agent + schemas
  search_agent.py        # Web search agent
  writer_agent.py        # Report generation agent + schemas
  email_agent.py         # SendGrid email agent + tool
```

## Notes and limitations

- Failed individual searches are skipped (`search` returns `None` on error); the writer still runs on whatever results were collected.
- Report length and tone are governed by `writer_agent.py` instructions; adjust there for shorter outputs or different formats.
- Web search behavior and quotas are subject to OpenAI’s current Agents / tool policies and your account limits.

For monorepo-wide setup and other projects, see the root `README.md`.
