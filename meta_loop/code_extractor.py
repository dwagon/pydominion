"""Extract and validate heuristic code from LLM responses."""

from __future__ import annotations

import re
import traceback
from typing import Optional


def extract_code(llm_response: str) -> str:
    """Extract Python code from a markdown code block in the LLM response.

    Looks for ```python ... ``` first, then bare ``` ... ```.
    Raises ValueError if no code block is found.
    """
    # Try ```python block first
    match = re.search(r"```python\s*\n(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Try bare ``` block
    match = re.search(r"```\s*\n(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()

    raise ValueError("No code block found in LLM response")


def validate_and_load(
    code: str,
    kingdom_cards: list[str],
    smoke_games: int = 10,
) -> type:
    """Validate heuristic code and return the AgentHeuristic class.

    Steps:
    1. Syntax check (compile)
    2. Execute in namespace
    3. Verify AgentHeuristic class exists and subclasses HeuristicPlayer
    4. Run smoke test games to catch runtime errors

    Raises ValueError with a descriptive message on failure.
    """
    # 1. Syntax check
    try:
        compile(code, "<agent_heuristic>", "exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error at line {e.lineno}: {e.msg}") from e

    # 2. Execute in namespace
    namespace: dict = {}
    try:
        exec(code, namespace)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from e

    # 3. Class check
    cls = namespace.get("AgentHeuristic")
    if cls is None:
        raise ValueError(
            "Code must define a class named 'AgentHeuristic'. "
            f"Found names: {[k for k in namespace if not k.startswith('_')]}"
        )

    from tournament.heuristic_player import HeuristicPlayer

    if not isinstance(cls, type) or not issubclass(cls, HeuristicPlayer):
        raise ValueError(
            "AgentHeuristic must be a class that subclasses HeuristicPlayer"
        )

    # 4. Smoke run
    _smoke_test(cls, kingdom_cards, smoke_games)

    return cls


def _smoke_test(cls: type, kingdom_cards: list[str], num_games: int) -> None:
    """Play a few fast games to catch runtime errors."""
    from tournament.engine import _run_single_game

    from dominion.BotPlayer import BotPlayer

    for i in range(num_games):
        try:
            _run_single_game(
                kingdom_cards=kingdom_cards,
                player_classes=[cls, BotPlayer],
                seed=90000 + i,  # distinct seed range from tournament evals
            )
        except Exception as e:
            tb = traceback.format_exc()
            raise ValueError(
                f"Heuristic crashed during smoke test game {i + 1}/{num_games}:\n"
                f"{tb}"
            ) from e


def count_lines(code: str) -> int:
    """Count non-blank, non-comment lines of code."""
    count = 0
    for line in code.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def compute_diff_lines(old_code: Optional[str], new_code: str) -> int:
    """Count changed lines between two code strings (simple diff)."""
    if old_code is None:
        return count_lines(new_code)

    import difflib

    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))
    # Count lines starting with + or - (excluding header lines)
    changed = sum(1 for line in diff if line.startswith(("+", "-")) and not line.startswith(("+++", "---")))
    return changed
