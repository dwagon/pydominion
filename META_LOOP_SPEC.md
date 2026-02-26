# Meta-Loop Spec

## What this is

The meta-loop is the core research apparatus. It orchestrates:

```
LLM receives kingdom + guide
  -> writes a Python heuristic player
  -> tournament evaluates it (fast, no LLM in the loop)
  -> LLM receives results + game traces
  -> LLM analyzes failures, rewrites heuristic
  -> repeat K iterations
  -> log everything
```

This spec covers the driver that coordinates these steps. It uses the
tournament engine (already built) and produces the artifacts described
in AGENT.md.

## Interface

```python
from meta_loop import run_meta_loop, MetaLoopResult

result: MetaLoopResult = run_meta_loop(
    kingdom_cards=["Chapel", "Village", "Smithy", "Market", "Militia",
                   "Moat", "Festival", "Laboratory", "Workshop", "Witch"],
    max_iterations=10,
    games_per_eval=200,           # per matchup side (400 total per pair)
    collect_traces=3,             # traced games per matchup
    llm_backend="openrouter",     # or "ollama"
    model="anthropic/claude-sonnet-4-20250514",
    seed=42,                      # optional, for reproducible tournament evals
    output_dir="runs/chapel_kingdom_001",
)
```

## The loop in detail

### Step 0: Prepare kingdom context (once)

Build a text block describing the 10 kingdom cards. This is passed to
the LLM at every iteration so it always has the card text available.

```
Kingdom Cards:
  Chapel ($2) [Action] — Trash up to 4 cards
  Village ($3) [Action] — +1 cards, +2 actions
  Smithy ($4) [Action] — +3 cards
  Market ($5) [Action] — +1 cards, +1 action, +1 coin, +1 buys
  Militia ($4) [Action, Attack] — +2 coin, Every other player discards down to 3
  Moat ($2) [Action] — +2 cards, defense
  Festival ($5) [Action] — +2 actions, +1 buys, +2 coin
  Laboratory ($5) [Action] — +2 cards, +1 action
  Workshop ($3) [Action] — Gain a card costing up to 4
  Witch ($5) [Action, Attack] — +2 cards; Each other player gains a Curse card.

Standard supply also includes: Copper, Silver, Gold, Estate, Duchy, Province, Curse.
```

To generate this programmatically, spin up a temporary game with the
kingdom cards and read `game.card_instances[name].desc` and
`card.cost` for each card. Don't use `card.description(player)` since
that requires an active player — use the static `card.desc` attribute
directly, which is set in each card's `__init__`.

**Implementation:**

```python
def get_kingdom_description(kingdom_cards: list[str]) -> str:
    """Build a text block describing the kingdom cards.

    Spins up a temporary game just to read card metadata.
    Returns a formatted string for the LLM prompt.
    """
    import random
    from dominion.Game import Game
    from dominion.BotPlayer import BotPlayer

    # Create a throwaway game to access card instances
    random.seed(0)
    game = Game(initcards=kingdom_cards, numplayers=2, quiet=True,
                player_classes=[BotPlayer, BotPlayer])
    game.start_game()

    lines = ["Kingdom Cards:"]
    for name in kingdom_cards:
        card = game.card_instances.get(name)
        if card is None:
            lines.append(f"  {name} — (not found)")
            continue
        types = []
        if card.isAction(): types.append("Action")
        if card.isTreasure(): types.append("Treasure")
        if card.isVictory(): types.append("Victory")
        if card.isAttack(): types.append("Attack")
        type_str = ", ".join(types)
        lines.append(f"  {name} (${card.cost}) [{type_str}] — {card.desc}")

    lines.append("")
    lines.append("Standard supply also includes: "
                 "Copper, Silver, Gold, Estate, Duchy, Province, Curse.")
    return "\n".join(lines)
```

### Step 1: Initial prompt — ask LLM to write a heuristic

**System prompt:**

```
You are an expert Dominion player and Python programmer. Your task is to
write a heuristic player for the Dominion card game.

You will be given:
1. A kingdom description (10 cards with English effect text)
2. A reference guide for the HeuristicPlayer API

Write a Python file that subclasses HeuristicPlayer and overrides the
strategy methods to play well on this specific kingdom.

RULES:
- Output ONLY the Python code, wrapped in ```python ... ``` markers
- Your class MUST be named `AgentHeuristic`
- Import from: `from tournament.heuristic_player import HeuristicPlayer, BuyState, ActionState, TrashState, DiscardState, GainState`
- Write your strategic reasoning as code comments (docstrings and inline)
- Do not import anything else. Do not use external libraries.
- Do not access self.game, self.piles, or any engine internals — only use
  the state objects passed to each method.
```

**User prompt (iteration 1):**

```
{kingdom_description}

---

{HEURISTIC_AUTHOR_GUIDE.md contents}

---

Write a heuristic player for this kingdom. Think carefully about:
- What is the strongest strategy on this board?
- Which cards synergize?
- When should you transition from building to buying VP?
- How do you handle attacks?

Write your reasoning as comments in the code.
```

### Step 2: Extract and validate the heuristic

Parse the LLM response to extract the Python code block. Then validate:

1. **Syntax check:** `compile(code, "<agent>", "exec")` — catches syntax errors
2. **Import check:** `exec` the code in a sandboxed namespace that provides
   only the allowed imports
3. **Class check:** Verify the namespace contains `AgentHeuristic` and it
   subclasses `HeuristicPlayer`
4. **Smoke run:** Play 10 fast games vs BotPlayer to catch runtime errors
   (crashes, infinite loops, illegal returns). Use a 30-second timeout.

If validation fails:

- Feed the error back to the LLM: "Your heuristic failed validation:
  {error}. Please fix it and resubmit the complete file."
- Allow up to 3 fix attempts per iteration before giving up on that
  iteration (log the failure and use the previous working heuristic).

**Implementation:**

```python
def extract_code(llm_response: str) -> str:
    """Extract Python code from markdown code block."""
    import re
    match = re.search(r'```python\s*\n(.*?)```', llm_response, re.DOTALL)
    if match:
        return match.group(1)
    # Fallback: try without language marker
    match = re.search(r'```\s*\n(.*?)```', llm_response, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No code block found in LLM response")


def validate_heuristic(code: str, kingdom_cards: list[str]) -> type:
    """Validate and load a heuristic. Returns the class, or raises."""
    # 1. Syntax check
    compile(code, "<agent_heuristic>", "exec")

    # 2. Execute in restricted namespace
    namespace = {}
    exec(code, namespace)

    # 3. Class check
    cls = namespace.get("AgentHeuristic")
    if cls is None:
        raise ValueError("Code must define a class named 'AgentHeuristic'")

    from tournament.heuristic_player import HeuristicPlayer
    if not issubclass(cls, HeuristicPlayer):
        raise ValueError("AgentHeuristic must subclass HeuristicPlayer")

    # 4. Smoke run — 10 games, 30s timeout
    _smoke_test_heuristic(cls, kingdom_cards)

    return cls


def _smoke_test_heuristic(cls: type, kingdom_cards: list[str]):
    """Play 10 quick games to catch runtime errors."""
    from tournament.engine import _run_single_game
    from dominion.BotPlayer import BotPlayer

    for i in range(10):
        try:
            _run_single_game(kingdom_cards, [cls, BotPlayer], seed=i)
        except Exception as e:
            raise ValueError(
                f"Heuristic crashed during smoke test game {i}: {e}"
            ) from e
```

### Step 3: Run tournament evaluation

Run the heuristic through the tournament engine against the baseline
players. The opponent pool is:

| Name | Class | Purpose |
|------|-------|---------|
| `bigmoney` | `BotPlayer` | The baseline to beat |
| `random` | `RandobotPlayer` | Floor check |
| `naive` | `NaiveBotPlayer` | Intermediate reference |
| `prev_best` | previous best `AgentHeuristic` | Self-play progression |

On iteration 1 there is no `prev_best`, so it's omitted. From iteration
2 onward, the best-performing AgentHeuristic so far is included.

```python
from tournament import run_tournament
from dominion.BotPlayer import BotPlayer
from dominion.RandobotPlayer import RandobotPlayer
from dominion.NaiveBotPlayer import NaiveBotPlayer

players = {
    f"agent_v{iteration}": agent_cls,
    "bigmoney": BotPlayer,
    "random": RandobotPlayer,
    "naive": NaiveBotPlayer,
}
if prev_best_cls is not None:
    players["prev_best"] = prev_best_cls

result = run_tournament(
    players=players,
    kingdom_cards=kingdom_cards,
    num_games_per_matchup=games_per_eval,
    seed=seed,
    collect_traces=collect_traces,
)
```

### Step 4: Format results for the LLM

Build a structured feedback message that the LLM can reason about.
This has three sections: summary stats, head-to-head details, and
sample game traces.

**Format:**

```
== Tournament Results (Iteration {N}) ==

Ratings (TrueSkill mu):
  agent_v3:     28.4  (win rate: 78.2%)
  bigmoney:     25.1  (win rate: 55.0%)
  naive:        22.3  (win rate: 41.5%)
  random:        8.9  (win rate:  8.3%)

Head-to-head vs BigMoney:
  Record: 164-36-0 (82.0% win rate)
  Avg VP: 31.2 vs 22.8 (margin: +8.4)
  Avg game length: 16.3 turns

Head-to-head vs Naive:
  Record: 172-28-0 (86.0% win rate)
  ...

{total_games} games played in {wall_seconds:.1f}s

== Sample Game Traces (losses and close games vs BigMoney) ==

--- Game #247: agent_v3 LOST (26 vs 31 VP, 18 turns) ---
OliviaBot: ************ Action Phase ************
OliviaBot: | Hand (5): Copper, Copper, Silver, Chapel, Estate
...
FINAL: OliviaBot: 26 VP  [Copper=2, Gold=3, Province=3, Silver=2, Village=1]
FINAL: JoshuaBot: 31 VP  [Copper=5, Gold=2, Province=4, Silver=3]

--- Game #412: agent_v3 WON by 1 VP (closest game) ---
...
```

**Implementation:**

```python
def format_feedback(
    result: TournamentResult,
    agent_name: str,
    iteration: int,
) -> str:
    lines = [f"== Tournament Results (Iteration {iteration}) ==", ""]

    # Ratings table
    lines.append("Ratings (TrueSkill mu):")
    sorted_ratings = sorted(result.ratings_detail.items(),
                            key=lambda x: -x[1].rating)
    for name, detail in sorted_ratings:
        lines.append(f"  {name:20s}  {detail.rating:6.1f}  "
                     f"(win rate: {detail.win_rate:.1%})")
    lines.append("")

    # Head-to-head details (agent vs each opponent)
    for (p1, p2), matchup in result.matchups.items():
        # Find the matchup involving the agent
        if agent_name not in (p1, p2):
            continue

        opponent = p2 if p1 == agent_name else p1
        if p1 == agent_name:
            wins, losses = matchup.wins_a, matchup.wins_b
            wr = matchup.win_rate_a
            avg_vp, opp_vp = matchup.avg_vp_a, matchup.avg_vp_b
        else:
            wins, losses = matchup.wins_b, matchup.wins_a
            wr = 1 - matchup.win_rate_a
            avg_vp, opp_vp = matchup.avg_vp_b, matchup.avg_vp_a

        lines.append(f"Head-to-head vs {opponent}:")
        lines.append(f"  Record: {wins}-{losses}-{matchup.draws} "
                     f"({wr:.1%} win rate)")
        lines.append(f"  Avg VP: {avg_vp:.1f} vs {opp_vp:.1f} "
                     f"(margin: {avg_vp - opp_vp:+.1f})")
        lines.append(f"  Avg game length: {matchup.avg_game_length:.1f} turns")
        lines.append("")

    lines.append(f"{result.total_games} games in {result.wall_seconds:.1f}s")
    lines.append("")

    # Game traces — prioritize losses vs bigmoney, then closest games
    lines.append("== Sample Game Traces ==")
    lines.append("")

    for (p1, p2), matchup in result.matchups.items():
        if agent_name not in (p1, p2):
            continue
        if not matchup.traces:
            continue

        opponent = p2 if p1 == agent_name else p1
        for trace in matchup.traces:
            score_a = trace.final_scores.get(trace.player_a, 0)
            score_b = trace.final_scores.get(trace.player_b, 0)
            lines.append(
                f"--- Game #{trace.game_number}: "
                f"{trace.outcome} ({score_a} vs {score_b} VP, "
                f"{trace.num_turns} turns) vs {opponent} ---"
            )
            if trace.spectator_log:
                lines.append(trace.spectator_log)
            else:
                lines.append("(no trace available)")
            lines.append("")

    return "\n".join(lines)
```

### Step 5: Ask LLM to analyze and rewrite

**User prompt (iterations 2+):**

```
{kingdom_description}

---

{HEURISTIC_AUTHOR_GUIDE.md contents}

---

Here is your current heuristic (iteration {N-1}):

```python
{current_heuristic_code}
```

Here are the tournament results:

{formatted_feedback}

---

Analyze the game traces carefully. What patterns do you see in the losses?
What decisions led to falling behind?

Then write an improved version of the heuristic. Think about:
- Are you buying the right cards at the right time?
- Is your action ordering correct?
- Are you trashing efficiently?
- When do you transition to greening (buying VP)?
- Are there card interactions you're not exploiting?

Output the complete updated Python file. Write your reasoning as comments
in the code — explain WHY you changed each thing.
```

### Step 6: Repeat from Step 2

Loop back to Step 2 (extract, validate, evaluate). Each iteration
produces a new heuristic version and a new set of results.

## What gets logged

Every run produces a directory:

```
runs/chapel_kingdom_001/
    config.json                    # kingdom, model, params
    kingdom_description.txt        # the card text block
    iteration_001/
        prompt.txt                 # full prompt sent to LLM
        llm_response.txt           # raw LLM response
        llm_reasoning.txt          # extracted reasoning (if LLM uses <thinking>)
        heuristic.py               # extracted code
        validation_errors.txt      # if any (empty if clean)
        tournament_result.json     # serialized TournamentResult
        feedback.txt               # formatted feedback string
        metrics.json               # key numbers for easy parsing
    iteration_002/
        ...
    iteration_010/
        ...
    summary.json                   # final results across all iterations
    win_rate_curve.json            # [{iter: 1, vs_bigmoney: 0.45}, ...]
```

### metrics.json (per iteration)

```json
{
    "iteration": 3,
    "vs_bigmoney_win_rate": 0.82,
    "vs_bigmoney_avg_vp_margin": 8.4,
    "vs_naive_win_rate": 0.86,
    "trueskill_mu": 28.4,
    "trueskill_sigma": 1.2,
    "total_games": 1600,
    "eval_seconds": 12.3,
    "llm_prompt_tokens": 4200,
    "llm_completion_tokens": 1800,
    "llm_latency_seconds": 8.5,
    "validation_attempts": 1,
    "heuristic_loc": 120,
    "code_diff_lines": 34
}
```

### summary.json (per run)

```json
{
    "kingdom": ["Chapel", "Village", ...],
    "model": "anthropic/claude-sonnet-4-20250514",
    "iterations": 10,
    "best_iteration": 7,
    "best_vs_bigmoney_win_rate": 0.91,
    "win_rate_curve": [0.45, 0.62, 0.74, 0.82, 0.85, 0.88, 0.90, 0.91, 0.90, 0.91],
    "total_llm_tokens": 58000,
    "total_wall_time_seconds": 340.0
}
```

## LLM backend

Use a thin wrapper that supports both Ollama (local) and OpenRouter (cloud).
The wrapper needs to:

1. Send a system prompt + user prompt
2. Return the raw text response
3. Track token counts and latency for logging

```python
class LLMClient:
    """Thin wrapper over LLM APIs."""

    def __init__(self, backend: str, model: str):
        self.backend = backend
        self.model = model

    def complete(self, system: str, user: str) -> LLMResponse:
        """Send a prompt and return the response."""
        ...

@dataclass
class LLMResponse:
    text: str
    prompt_tokens: int
    completion_tokens: int
    latency_seconds: float
```

For OpenRouter, use the OpenAI-compatible API:

```python
import httpx

resp = httpx.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    timeout=120,
)
```

For Ollama, use its OpenAI-compatible endpoint at `localhost:11434`.

Store the API key in environment variable `OPENROUTER_API_KEY`.

## Error handling

| Error | Response |
|-------|----------|
| LLM returns no code block | Log error, retry with "Please output Python code in a ```python code block" |
| Syntax error in code | Feed error to LLM for fix (up to 3 attempts) |
| Runtime crash in smoke test | Feed traceback to LLM for fix (up to 3 attempts) |
| All fix attempts fail | Log failure, keep previous heuristic, continue to next iteration |
| LLM API timeout/error | Retry with exponential backoff (3 attempts, then fail iteration) |
| Tournament engine crash | Fatal error — stop the run, log everything |

## Concurrency

The meta-loop is inherently sequential (each iteration depends on
the previous one's results). But within an iteration:

- Tournament evaluation can be parallelized (future optimization —
  use multiprocessing for game simulation)
- LLM calls are single-threaded (one call per iteration)

For the initial implementation, everything runs single-threaded.
The bottleneck is LLM latency (~5-15s per call), not game simulation
(~10s for 1600 games).

## File layout

```
meta_loop/
    __init__.py                # run_meta_loop() entry point
    driver.py                  # main loop logic
    llm_client.py              # LLM backend wrapper
    code_extractor.py          # extract + validate heuristic code
    feedback_formatter.py      # format TournamentResult for LLM
    kingdom_builder.py         # build kingdom description text
    logger.py                  # write iteration artifacts to disk
    prompts.py                 # system and user prompt templates
```

## Smoke test

```bash
uv run python -m meta_loop.smoke_test
```

Runs 2 iterations on the Chapel kingdom with a cheap/fast model.
Asserts:
- Both iterations produce valid heuristics
- Both heuristics beat Random (>60% win rate)
- All artifacts are written to disk
- Win rate curve is parseable

## What this does NOT include

- Multi-kingdom runs (Phase 2) — that's a wrapper over this
- Fine-tuning / training (Phase 3) — that's the lab's job
- Web UI or visualization — command-line only
- Async / parallel game simulation — future optimization

## Design decisions

### Why `AgentHeuristic` fixed class name?

Simplifies dynamic loading. The meta-loop always knows the class
is `AgentHeuristic` — no need to parse `class Foo(HeuristicPlayer)`
and discover the name dynamically.

### Why include the full HEURISTIC_AUTHOR_GUIDE in every prompt?

The guide is ~3KB. Including it in every prompt costs ~1000 tokens
but ensures the LLM always has the complete API reference. This
prevents drift or hallucinated method signatures across iterations.
At 10 iterations, that's 10K extra tokens — negligible vs the
reasoning content.

### Why `prev_best` instead of `prev_iteration`?

Including the best-so-far heuristic as a tournament opponent (not
just the immediately previous one) lets us detect regressions. If
iteration 7 was the best and iteration 8 is worse, the tournament
results will show `agent_v8` losing to `prev_best` — clear signal
for the LLM that the change was bad.

### Why 3 fix attempts?

Empirically, most LLM coding errors are caught on the first fix
attempt (missing import, wrong method signature). If the code
still doesn't work after 3 attempts, the error is likely
fundamental (wrong understanding of the API) and burning more
tokens won't help.

### Why temperature 0.7?

We want some diversity across iterations — the LLM shouldn't
converge to the same code every time. But we don't want random
gibberish. 0.7 is a reasonable starting point. This should be
tunable.

### Why not show the LLM ALL opponent matchups' traces?

Token budget. With 4 opponents and 3 traces each, that's 12 game
logs. Each trace is ~2-4KB. At 48KB of traces per iteration, we'd
blow through context quickly. Instead, prioritize traces vs bigmoney
(the target baseline) and include a summary table for other matchups.

In practice, show traces for the matchup the agent is losing or
winning narrowly. If it's already beating bigmoney 90%+, show the
losses to `prev_best` instead — that's where the marginal
improvement comes from.

**Trace selection rule:** Show traces from the matchup with the
lowest win rate for the agent. If all win rates are >85%, show
traces from the closest matchup (smallest VP margin). Cap at 5
traces total.
