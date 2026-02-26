"""Smoke test for single-shot heuristic evaluation.

Tests every component WITHOUT calling a real LLM. Uses a mock LLM that
returns a canned Chapel+Witch heuristic.

Usage:
    uv run python -m meta_loop.smoke_test
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile

# ---------------------------------------------------------------------------
# A fake heuristic that the mock LLM will "write"
# ---------------------------------------------------------------------------

MOCK_HEURISTIC = '''\
```python
from tournament.heuristic_player import HeuristicPlayer, BuyState, ActionState, TrashState, DiscardState, GainState
from typing import Optional


class AgentHeuristic(HeuristicPlayer):
    """Simple strategy: Chapel to trash junk, then BigMoney with Witch."""

    def buy_priority(self, state: BuyState) -> Optional[str]:
        coins = state.coins
        deck = state.my_deck
        buyable = state.buyable
        provinces_left = state.provinces_remaining

        # Buy Province when we can
        if coins >= 8 and "Province" in buyable:
            return "Province"

        # Late game duchies
        if coins >= 5 and provinces_left <= 4 and "Duchy" in buyable:
            return "Duchy"

        # Opening: get Chapel
        if state.turn_number <= 2:
            if "Chapel" not in deck and "Chapel" in buyable:
                return "Chapel"
            if coins >= 3 and "Silver" in buyable:
                return "Silver"
            return None

        # Get a Witch for the attack
        if coins >= 5 and "Witch" in buyable and deck.get("Witch", 0) < 1:
            return "Witch"

        # Economy
        if coins >= 6 and "Gold" in buyable:
            return "Gold"
        if coins >= 3 and "Silver" in buyable:
            return "Silver"

        return None

    def action_priority(self, state: ActionState) -> Optional[str]:
        playable = state.playable_actions
        if not playable:
            return None

        hand = state.hand

        # Chapel when we have junk
        if "Chapel" in playable:
            junk = [c for c in hand if c in ("Curse", "Estate", "Copper")]
            if junk:
                return "Chapel"

        # Witch for the attack
        if "Witch" in playable:
            return "Witch"

        # Any other action
        for card in playable:
            return card

        return None

    def trash_priority(self, card_names: list[str], num: int, state: TrashState) -> list[str]:
        # Trash Curses > Estates > Coppers
        priority = ["Curse", "Estate", "Copper"]
        result = []
        available = list(card_names)
        for target in priority:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)
        return result
```
'''


class MockLLMClient:
    """Returns canned responses for testing."""

    def complete(self, system, user, max_tokens=8192, temperature=0.3):
        from meta_loop.llm_client import LLMResponse
        return LLMResponse(
            text=MOCK_HEURISTIC,
            prompt_tokens=1000,
            completion_tokens=500,
            latency_seconds=0.1,
        )


def main():
    print("=" * 60)
    print("Single-Shot Eval Smoke Test")
    print("=" * 60)

    failures: list[str] = []
    output_dir = tempfile.mkdtemp(prefix="eval_smoke_")
    print(f"Output dir: {output_dir}")

    try:
        _test_kingdom_builder(failures)
        _test_code_extractor(failures)
        _test_single_shot_pipeline(failures, output_dir)
    except Exception as e:
        import traceback
        traceback.print_exc()
        failures.append(f"Unexpected exception: {e}")
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

    print()
    if failures:
        print("SMOKE TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("SMOKE TEST PASSED!")


def _test_kingdom_builder(failures: list[str]):
    print("\n--- Testing kingdom_builder ---")
    from meta_loop.kingdom_builder import get_kingdom_description

    kingdom = ["Chapel", "Village", "Smithy", "Market", "Militia",
               "Moat", "Festival", "Laboratory", "Workshop", "Witch"]
    desc = get_kingdom_description(kingdom)

    if "Chapel" not in desc:
        failures.append("Kingdom description missing 'Chapel'")
    if "$2" not in desc or "$5" not in desc:
        failures.append("Kingdom description missing cost info")
    if "Trash up to 4" not in desc:
        failures.append("Kingdom description missing card effect text")
    print(f"  OK: {len(desc)} chars, {desc.count(chr(10))} lines")


def _test_code_extractor(failures: list[str]):
    print("\n--- Testing code_extractor ---")
    from meta_loop.code_extractor import extract_code, validate_and_load, count_lines

    kingdom = ["Chapel", "Village", "Smithy", "Market", "Militia",
               "Moat", "Festival", "Laboratory", "Workshop", "Witch"]

    code = extract_code(MOCK_HEURISTIC)
    if "AgentHeuristic" not in code:
        failures.append("Extracted code missing AgentHeuristic class")

    try:
        cls = validate_and_load(code, kingdom, smoke_games=5)
        if cls.__name__ != "AgentHeuristic":
            failures.append(f"Class name is {cls.__name__}, expected AgentHeuristic")
        print(f"  OK: validated, {count_lines(code)} LOC")
    except Exception as e:
        failures.append(f"Validation failed: {e}")

    try:
        validate_and_load("class Foo: pass", kingdom, smoke_games=1)
        failures.append("Bad code should have raised ValueError")
    except ValueError:
        print("  OK: bad code correctly rejected")


def _test_single_shot_pipeline(failures: list[str], output_dir: str):
    """Run the single-shot pipeline with a mock LLM."""
    print("\n--- Testing single-shot pipeline (mock LLM) ---")

    from dominion.BotPlayer import BotPlayer
    from dominion.NaiveBotPlayer import NaiveBotPlayer
    from tournament import run_agent_matchups
    from meta_loop.kingdom_builder import get_kingdom_description
    from meta_loop.code_extractor import extract_code, validate_and_load, count_lines
    from meta_loop.logger import RunLogger
    from meta_loop.prompts import SYSTEM_PROMPT, build_initial_prompt
    from meta_loop.results import EvalResult

    kingdom = ["Chapel", "Village", "Smithy", "Market", "Militia",
               "Moat", "Festival", "Laboratory", "Workshop", "Witch"]

    mock_llm = MockLLMClient()
    logger = RunLogger(output_dir, kingdom, "mock-model")
    logger.write_config(games_per_eval=20, seed=42, temperature=0.3)

    kingdom_desc = get_kingdom_description(kingdom)
    logger.write_kingdom_description(kingdom_desc)

    # LLM call
    user_prompt = build_initial_prompt(kingdom_desc)
    logger.write_prompt(1, SYSTEM_PROMPT, user_prompt)
    resp = mock_llm.complete("sys", "user")
    logger.write_llm_response(1, resp.text)

    # Extract and validate
    code = extract_code(resp.text)
    cls = validate_and_load(code, kingdom, smoke_games=3)
    logger.write_heuristic(1, code)

    # Evaluate
    agent_name = "agent"
    opponents = {"bigmoney": BotPlayer, "naive": NaiveBotPlayer}
    result = run_agent_matchups(
        agent_name=agent_name,
        agent_class=cls,
        opponents=opponents,
        kingdom_cards=kingdom,
        num_games_per_matchup=20,
        seed=42,
        collect_traces=0,
    )
    logger.write_tournament_result(1, result)

    # Extract win rates
    from meta_loop.driver import _get_win_rate, _get_vp_margin
    vs_bm = _get_win_rate(result, agent_name, "bigmoney")
    vs_naive = _get_win_rate(result, agent_name, "naive")
    margin = _get_vp_margin(result, agent_name, "bigmoney")

    detail = result.ratings_detail.get(agent_name)
    mu = detail.rating if detail else 0.0
    sigma = detail.uncertainty if detail else 0.0

    eval_result = EvalResult(
        kingdom=kingdom, model="mock-model",
        vs_bigmoney_win_rate=vs_bm,
        vs_bigmoney_avg_vp_margin=margin,
        vs_all_win_rates={"bigmoney": vs_bm, "naive": vs_naive},
        trueskill_mu=mu, trueskill_sigma=sigma,
        total_games=result.total_games,
        eval_seconds=result.wall_seconds,
        llm_prompt_tokens=resp.prompt_tokens,
        llm_completion_tokens=resp.completion_tokens,
        llm_latency_seconds=resp.latency_seconds,
        validation_attempts=1, heuristic_loc=count_lines(code),
        estimated_cost_usd=0.0,
        total_wall_time_seconds=0.0,
        output_dir=output_dir, success=True,
    )
    logger.write_metrics(1, eval_result)
    logger.write_summary(eval_result)

    # Check artifacts
    if not os.path.exists(os.path.join(output_dir, "config.json")):
        failures.append("Missing config.json")
    if not os.path.exists(os.path.join(output_dir, "kingdom_description.txt")):
        failures.append("Missing kingdom_description.txt")
    if not os.path.exists(os.path.join(output_dir, "summary.json")):
        failures.append("Missing summary.json")

    d = os.path.join(output_dir, "iteration_001")
    for fname in ["heuristic.py", "llm_response.txt", "tournament_result.json", "metrics.json"]:
        if not os.path.exists(os.path.join(d, fname)):
            failures.append(f"Missing {fname}")

    print(f"  OK: vs BigMoney {vs_bm:.0%}, vs Naive {vs_naive:.0%}, margin {margin:+.1f}")


if __name__ == "__main__":
    main()
