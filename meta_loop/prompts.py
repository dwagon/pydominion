"""Prompt templates for the meta-loop."""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# System prompt — identical for every iteration
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert Dominion player and Python programmer. Your task is to
write a heuristic player for the Dominion card game.

You will be given:
1. A kingdom description (cards with English effect text, plus any active
   events, landmarks, or other modifiers)
2. A reference guide for the HeuristicPlayer API

Write a Python file that subclasses HeuristicPlayer and overrides the
strategy methods to play well on this specific kingdom.

DOMINION FUNDAMENTALS:
- The game ends when the Province pile is empty (or Colony pile, if in play),
  or when 3 supply piles are empty.
- Victory cards are dead weight in your deck — they don't do anything when
  drawn during play.
- Deck thinning (trashing weak cards) makes your deck more consistent.
- Action ordering matters: play cards that give +Actions before terminals
  (cards that don't give +Actions).
- Consider both building your deck (engine/economy) and when to transition
  to buying victory points.

RULES:
- Output ONLY the Python code, wrapped in ```python ... ``` markers.
- Your class MUST be named `AgentHeuristic`.
- Import from: `from tournament.heuristic_player import HeuristicPlayer, BuyState, ActionState, TrashState, DiscardState, GainState`
- You may also import `from typing import Optional` if needed.
- Write your strategic reasoning as code comments (docstrings and inline).
- Do not import anything else. Do not use external libraries.
- Do not access self.game, self.piles, or any engine internals — only use
  the state objects passed to each method.
- If you don't override a method, the default BigMoney-ish behavior applies.
  You don't have to override everything — only what your strategy needs.
"""


def _load_author_guide() -> str:
    """Load HEURISTIC_AUTHOR_GUIDE.md from the project root."""
    # Walk up from this file to find the project root
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    guide_path = os.path.join(project_root, "HEURISTIC_AUTHOR_GUIDE.md")
    with open(guide_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# User prompt — iteration 1 (initial write)
# ---------------------------------------------------------------------------

def build_initial_prompt(kingdom_description: str) -> str:
    guide = _load_author_guide()
    return f"""\
{kingdom_description}

---

{guide}

---

Write a heuristic player for this kingdom. Think carefully about:
- What is the strongest strategy on this board?
- Which cards synergize well together?
- When should you transition from building your deck to buying VP cards?
- How do you handle attacks (both using them and defending against them)?

Write your reasoning as comments in the code.
"""


# ---------------------------------------------------------------------------
# User prompt — iteration 2+ (analyze results and rewrite)
# ---------------------------------------------------------------------------

def build_refinement_prompt(
    kingdom_description: str,
    current_code: str,
    feedback: str,
    iteration: int,
) -> str:
    guide = _load_author_guide()
    return f"""\
{kingdom_description}

---

{guide}

---

Here is your current heuristic (iteration {iteration - 1}):

```python
{current_code}
```

Here are the tournament results:

{feedback}

---

IMPORTANT REFINEMENT GUIDELINES:
- If your win rate vs bigmoney is ALREADY HIGH (>60%), be very conservative.
  Do NOT rewrite the strategy from scratch. Only make small, targeted fixes
  to specific weaknesses visible in the traces. Keep what is working.
- If your win rate is LOW (<30%), a bigger rewrite may be warranted, but
  still focus on the most impactful single issue (e.g., not buying Province,
  too many junk cards, wrong action ordering).
- Change ONE OR TWO things per iteration, not six. Changes interact and
  compound unpredictably.

Analyze the game traces. Focus on:
1. What specific decisions cost you games? (Look at the losing traces.)
2. Is there a pattern in the losses? (e.g., never buying Province, deck too
   thick, wrong action order.)
3. What is the SINGLE most impactful fix?

Then write an improved version. Think about:
- Are you buying VP cards (Province/Colony) when you can afford them?
- Is your action ordering correct (non-terminals before terminals)?
- Are you thinning your deck efficiently if a trasher is available?
- When do you transition from building to buying VP?

Output the complete updated Python file. Write your reasoning as comments
explaining WHY you changed each specific thing.
"""


# ---------------------------------------------------------------------------
# Fix prompt — when validation fails
# ---------------------------------------------------------------------------

def build_fix_prompt(code: str, error: str) -> str:
    return f"""\
Your heuristic failed validation with this error:

```
{error}
```

Here is the code that failed:

```python
{code}
```

Please fix the error and output the complete corrected Python file.
Remember:
- Class must be named `AgentHeuristic`
- Must subclass `HeuristicPlayer`
- Import from: `from tournament.heuristic_player import HeuristicPlayer, BuyState, ActionState, TrashState, DiscardState, GainState`
- Do not access engine internals (self.game, self.piles, etc.)
"""
