# pydominion — Project Context for Claude

## What this project is

A Dominion card game simulator (forked from dwagon/pydominion) being extended into a
**language-grounded strategy synthesis environment** — an RL/AI research environment
where LLMs learn to write game-playing heuristics from natural language card descriptions.

## Current state

### Game engine
- Full Dominion simulator in Python. 548+ card implementations across all expansions.
- Core files: `dominion/Game.py`, `dominion/Player.py`, `dominion/Card.py`, `dominion/Prompt.py`
- Card definitions: `dominion/cards/*.py`
- Pre-built kingdoms: `cardset/*`

### Player types
- `TextPlayer.py` — interactive CLI human player
- `BotPlayer.py` — BigMoney greedy baseline (Province > Gold > Silver priority)
- `RandobotPlayer.py` — random legal moves
- `LLMPlayer.py` — LLM-as-policy player with two-tier prompting:
  1. Pre-game strategy generation (one LLM call, produces pseudocode plan)
  2. Turn-by-turn execution (per-decision LLM calls, returns `{"selector":"X"}`)

### LLM integration
- Supports Ollama and OpenRouter backends
- System prompts: `gameengine.prompt` (selector contract), `gameplay.prompt` (Dominion rules)
- Detailed logging via `MatchupLogger.py` — captures every LLM call with prompts,
  thinking traces, responses, token counts, latency
- Logs go to `logs/<timestamp>/`

### Known issues
- `discrepancy_report.md` documents card cost errors (Haven, Leprechaun, Shepherd, etc.)
- LLM player (deepseek-v3.2) loses to BigMoney due to strategic mistakes:
  - Buys duplicate Chapel when one suffices
  - Doesn't buy Silver often enough
  - Buys +action cards without terminal goals

## Project direction

See `AGENT.md` for the full research plan.

**Short version:** Instead of using LLMs to play Dominion directly (slow, bad at
stochastic planning), the goal is to have LLMs **write heuristic players** that play
quickly, then iteratively refine them by analyzing game results. This produces training
data in the form of strategy-reasoning traces that are interesting to AI labs.

### The meta-loop (to be built)
```
Agent receives kingdom (10 cards with English text)
  → writes Python heuristic player
  → harness runs 10,000 fast games vs BigMoney
  → harness reports win rate + example loss traces
  → agent reasons about failures, rewrites heuristic
  → repeat K iterations
  → log everything (code diffs, reasoning, win rate curves)
```

### Key design decisions made
- **One kingdom first**, then generalize to many (train/test split)
- **No Gymnasium/discrete-action-space wrapper** — the point is language-grounded
  reasoning over English card text, not converting to embeddings
- **Heuristics should NOT exception back to LLM during fast evaluation** — if the
  heuristic doesn't know what to do, it does something simple (buy best treasure).
  The agent writes its reasoning as code comments, not structured metadata.
  The meta-loop figures out what went wrong by reading game traces and the code.
- **No confidence tagging** — the heuristic doesn't self-report uncertainty.
  The meta-agent reads game traces to diagnose failures, which is more natural
  and doesn't add complexity to the heuristic interface.

## Code conventions
- Python 3.11+
- Use `uv` for running Python (uv run, uv pip, uv venv)
- Rich library for console output
- Game entry point: `dominion/rungame.py`
