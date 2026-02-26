"""Artifact logger — writes iteration outputs to disk."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Optional

from tournament.results import TournamentResult
from .results import EvalResult


class RunLogger:
    """Manages the output directory and writes artifacts per iteration."""

    def __init__(self, output_dir: str, kingdom: list[str], model: str):
        self.output_dir = output_dir
        self.kingdom = kingdom
        self.model = model
        os.makedirs(output_dir, exist_ok=True)

    def write_config(self, **extra: object) -> None:
        """Write run config to config.json."""
        config = {
            "kingdom": self.kingdom,
            "model": self.model,
            **extra,
        }
        self._write_json("config.json", config)

    def write_kingdom_description(self, text: str) -> None:
        self._write_text("kingdom_description.txt", text)

    # ------------------------------------------------------------------
    # Per-iteration artifacts
    # ------------------------------------------------------------------

    def iteration_dir(self, iteration: int) -> str:
        d = os.path.join(self.output_dir, f"iteration_{iteration:03d}")
        os.makedirs(d, exist_ok=True)
        return d

    def write_prompt(self, iteration: int, system: str, user: str) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "prompt_system.txt"), "w", encoding="utf-8") as f:
            f.write(system)
        with open(os.path.join(d, "prompt_user.txt"), "w", encoding="utf-8") as f:
            f.write(user)

    def write_llm_response(self, iteration: int, text: str) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "llm_response.txt"), "w", encoding="utf-8") as f:
            f.write(text)

    def write_llm_reasoning(self, iteration: int, reasoning: str) -> None:
        """Save thinking/reasoning trace (DeepSeek, Kimi, etc.). No-op if empty."""
        if not reasoning:
            return
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "llm_reasoning.txt"), "w", encoding="utf-8") as f:
            f.write(reasoning)

    def write_heuristic(self, iteration: int, code: str) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "heuristic.py"), "w", encoding="utf-8") as f:
            f.write(code)

    def write_validation_errors(self, iteration: int, errors: list[str]) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "validation_errors.txt"), "w", encoding="utf-8") as f:
            f.write("\n\n---\n\n".join(errors) if errors else "(none)")

    def write_feedback(self, iteration: int, feedback: str) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "feedback.txt"), "w", encoding="utf-8") as f:
            f.write(feedback)

    def write_tournament_result(self, iteration: int, result: TournamentResult) -> None:
        """Serialize TournamentResult to JSON (best-effort)."""
        d = self.iteration_dir(iteration)
        # Convert to a JSON-safe dict
        data = {
            "ratings": result.ratings,
            "total_games": result.total_games,
            "wall_seconds": result.wall_seconds,
            "games_per_second": result.games_per_second,
            "matchups": {},
        }
        for (p1, p2), m in result.matchups.items():
            key = f"{p1}_vs_{p2}"
            data["matchups"][key] = {
                "player_a": m.player_a,
                "player_b": m.player_b,
                "wins_a": m.wins_a,
                "wins_b": m.wins_b,
                "draws": m.draws,
                "num_games": m.num_games,
                "win_rate_a": m.win_rate_a,
                "avg_vp_a": m.avg_vp_a,
                "avg_vp_b": m.avg_vp_b,
                "avg_vp_margin": m.avg_vp_margin,
                "avg_game_length": m.avg_game_length,
                "crashes": m.crashes,
                "num_traces": len(m.traces),
            }
        self._write_json(os.path.join(f"iteration_{iteration:03d}", "tournament_result.json"), data)

    def write_metrics(self, iteration: int, metrics: EvalResult) -> None:
        d = self.iteration_dir(iteration)
        with open(os.path.join(d, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def write_summary(self, result: EvalResult) -> None:
        self._write_json("summary.json", asdict(result))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _write_json(self, relpath: str, data: object) -> None:
        path = os.path.join(self.output_dir, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def _write_text(self, relpath: str, text: str) -> None:
        path = os.path.join(self.output_dir, relpath)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
