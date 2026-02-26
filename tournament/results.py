from dataclasses import dataclass

@dataclass
class GameTrace:
    game_number: int
    player_a: str
    player_b: str
    outcome: str                           # "win_a", "win_b", "draw"
    final_scores: dict[str, int]           # {player_name: VP}
    num_turns: int
    kingdom_cards: list[str]
    seed: int                              # Random seed for retracing
    spectator_log: str

@dataclass
class MatchupResult:
    player_a: str
    player_b: str
    wins_a: int
    wins_b: int
    draws: int
    num_games: int
    win_rate_a: float

    avg_vp_a: float
    avg_vp_b: float
    avg_vp_margin: float           # a minus b
    avg_game_length: float         # in turns

    crashes: int                   # games where agent threw an exception (counted as losses)
    traces: list[GameTrace]        # sampled game traces

@dataclass
class RatingDetail:
    name: str
    rating: float           # Elo or TrueSkill mu
    uncertainty: float      # TrueSkill sigma, or confidence interval half-width
    games_played: int
    win_rate: float         # overall across all matchups

@dataclass
class TournamentResult:
    ratings: dict[str, float]               # {player_name: Elo} or TrueSkill mu
    ratings_detail: dict[str, RatingDetail]  # full rating info per player
    matchups: dict[tuple[str, str], MatchupResult]
    total_games: int
    wall_seconds: float
    games_per_second: float
