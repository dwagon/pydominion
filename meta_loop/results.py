"""Result dataclasses for single-shot heuristic evaluation."""

from dataclasses import dataclass


@dataclass
class EvalResult:
    """Result of a single-shot heuristic generation + evaluation."""
    kingdom: list[str]
    model: str
    vs_bigmoney_win_rate: float
    vs_bigmoney_avg_vp_margin: float
    vs_all_win_rates: dict[str, float]    # {opponent_name: win_rate}
    trueskill_mu: float
    trueskill_sigma: float
    total_games: int
    eval_seconds: float
    llm_prompt_tokens: int
    llm_completion_tokens: int
    llm_latency_seconds: float
    validation_attempts: int
    heuristic_loc: int
    estimated_cost_usd: float
    total_wall_time_seconds: float
    output_dir: str
    success: bool  # False if all validation attempts failed
    avg_game_length: float | None = None  # avg turns per game across all matchups; None if not evaluated
    crashes_by_opponent: dict[str, int] | None = None  # {opponent: crash_count}; None if not evaluated
