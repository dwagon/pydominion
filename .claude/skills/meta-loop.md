# meta-loop

Runs the meta_loop heuristic evaluation for one or more LLM models.

## When to use
Use when the user says "run meta_loop", "run meta loop", "evaluate model", "run eval", or asks to test models against the Dominion heuristic pipeline.

## How it works
The meta_loop is a single-shot heuristic evaluation pipeline:
1. Builds a kingdom description from card names
2. Calls the LLM to write a HeuristicPlayer subclass
3. Validates & smoke-tests the generated code (10 games)
4. Runs a tournament (default 200 games per side) vs BigMoney + NaiveBotPlayer
5. Logs results to `runs/<timestamp>_<model>/`

## Command
```bash
uv run python -m meta_loop --model <provider/model-name> [options]
```

## Key options
| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `anthropic/claude-sonnet-4-20250514` | Model (provider/name format) |
| `--kingdom` | Chapel kingdom | Space-separated card names |
| `--random` | false | Random kingdom |
| `--games` | 200 | Games per matchup side |
| `--backend` | `openrouter` | `openrouter` or `ollama` |
| `--seed` | None | Random seed |
| `--temperature` | 0.3 | LLM temperature |
| `--max-tokens` | 8192 | Max output tokens |
| `--prosperity` | false | Add Colony/Platinum |
| `--events`, `--landmarks`, `--ways`, `--projects`, `--allies`, `--traits`, `--prophecies` | [] | Extra game components |

## Multiple models
When the user asks to run multiple models, launch them **all in parallel** as background bash commands. Each run takes ~2-10 minutes depending on the model.

Example for 4 models:
```bash
uv run python -m meta_loop --model deepseek/deepseek-v3.2
uv run python -m meta_loop --model deepseek/deepseek-chat-v3.1
uv run python -m meta_loop --model deepseek/deepseek-chat
uv run python -m meta_loop --model deepseek/deepseek-r1
```

## Output
Results go to `runs/<timestamp>_<model>/` containing:
- `config.json` — kingdom, model, parameters
- `kingdom_description.txt` — card text sent to LLM
- `iteration_001/heuristic.py` — generated heuristic code
- `iteration_001/llm_response.txt` — raw LLM output
- `iteration_001/tournament_result.json` — game results
- `iteration_001/metrics.json` — win rates, VP margins
- `summary.json` — overall results

## Checking results
After runs complete, read `summary.json` from each run directory to compare model performance. Key metrics: win rate vs BigMoney, win rate vs NaiveBot, average VP margin.
