# Tournament Engine Spec

## Purpose

Run round-robin 1v1 matchups between multiple bot players on a given kingdom,
fast, and return structured results with Elo/TrueSkill ratings.

This is **not** the meta-loop itself. It's the inner evaluation step:
"here are some player implementations, tell me how they rank."

## Interface

```python
from tournament import run_tournament, TournamentResult

result: TournamentResult = run_tournament(
    players={
        "bigmoney": BotPlayer,             # the existing BigMoney bot
        "random": RandobotPlayer,           # the existing random bot
        "chapel_rush_v1": ChapelRushV1,     # a heuristic the agent wrote
        "chapel_rush_v2": ChapelRushV2,     # a revised heuristic
    },
    kingdom_cards=["Chapel", "Village", "Smithy", "Market", "Militia",
                   "Moat", "Festival", "Laboratory", "Workshop", "Witch"],
    num_games_per_matchup=200,              # games per pair, per side (so 400 total per pair)
    seed=42,                                # optional, for reproducibility
    collect_traces=5,                       # traced games per matchup (worst losses)
)
```

## TournamentResult

```python
@dataclass
class TournamentResult:
    # Ratings
    ratings: dict[str, float]               # {player_name: Elo} or TrueSkill mu
    ratings_detail: dict[str, RatingDetail]  # full rating info per player

    # Head-to-head results for every pair
    matchups: dict[tuple[str, str], MatchupResult]

    # Timing
    total_games: int
    wall_seconds: float
    games_per_second: float

@dataclass
class RatingDetail:
    name: str
    rating: float           # Elo or TrueSkill mu
    uncertainty: float      # TrueSkill sigma, or confidence interval half-width
    games_played: int
    win_rate: float         # overall across all matchups

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

    traces: list[GameTrace]        # sampled game traces (worst losses for player_a)
```

## GameTrace

A structured record of one complete game, readable by the meta-agent.

```python
@dataclass
class GameTrace:
    game_number: int
    player_a: str
    player_b: str
    outcome: str                           # "win_a", "win_b", "draw"
    final_scores: dict[str, int]           # {player_name: VP}
    num_turns: int
    kingdom_cards: list[str]

    # Per-turn log (human-readable, like current spectator log)
    spectator_log: str
```

## HeuristicPlayer base class

The tournament engine needs a player class that:
1. Subclasses `Player` (to plug into the existing game engine)
2. Has a clean interface the meta-agent writes code against
3. Falls back to simple behavior (buy best treasure) when it has no opinion

The meta-agent writes its reasoning as code comments, not structured metadata.

```python
from dominion.Player import Player
from dominion import Piles


class HeuristicPlayer(Player):
    """Base class for agent-written heuristic players.

    Subclass this and override the strategy methods.
    The base class provides sensible defaults (BigMoney-ish fallbacks)
    so a partial heuristic still plays legal games.
    """

    # --- Methods the meta-agent overrides ---

    def buy_priority(self, state: BuyState) -> str | None:
        """Called during buy phase after treasures are spent.

        Args:
            state: structured view of game state (see BuyState)

        Returns:
            Card name to buy, or None to end buy phase.
        """
        # Default: BigMoney fallback
        if state.coins >= 8 and "Province" in state.buyable:
            return "Province"
        if state.coins >= 6 and "Gold" in state.buyable:
            return "Gold"
        if state.coins >= 3 and "Silver" in state.buyable:
            return "Silver"
        return None

    def action_priority(self, state: ActionState) -> str | None:
        """Called during action phase.

        Args:
            state: structured view including hand, actions remaining, etc.

        Returns:
            Card name to play, or None to end action phase.
        """
        # Default: play first playable action, or end phase
        if state.playable_actions:
            return state.playable_actions[0]
        return None

    def trash_priority(self, card_names: list[str], num: int,
                       state: TrashState) -> list[str]:
        """Called when the heuristic must choose cards to trash.

        Returns:
            List of card names to trash (up to num).
        """
        # Default: trash Curses, then Estates, then Coppers
        priority = ["Curse", "Estate", "Copper"]
        result = []
        available = list(card_names)
        for target in priority:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)
        return result

    def discard_priority(self, card_names: list[str], num: int,
                         state: DiscardState) -> list[str]:
        """Called when forced to discard (e.g., Militia attack).

        Returns:
            List of card names to discard (exactly num).
        """
        # Default: discard victory cards first, then cheapest treasures
        ...

    def gain_priority(self, max_cost: int, state: GainState) -> str | None:
        """Called when gaining a card up to a cost (e.g., Workshop).

        Returns:
            Card name to gain, or None to gain nothing.
        """
        # Default: gain most expensive card available up to max_cost
        ...

    # --- Engine glue (not overridden by meta-agent) ---

    def user_input(self, options, prompt):
        """Routes engine option prompts to the right heuristic method.

        Detects current phase, builds state objects, calls the right
        *_priority method, maps the returned card name back to an
        Option selector.
        """
        ...

    def card_sel(self, num=1, **kwargs):
        """Routes card selection prompts (trash, discard, etc.)."""
        ...

    def plr_choose_options(self, prompt, *choices):
        """Routes multi-choice prompts."""
        ...
```

## State objects passed to heuristic methods

Structured, not free-text. The heuristic is code — it can inspect numbers directly.

```python
@dataclass
class BuyState:
    coins: int
    buys: int
    actions_remaining: int
    turn_number: int
    my_deck: dict[str, int]           # {"Copper": 4, "Silver": 2, "Chapel": 1, ...}
    my_deck_size: int
    my_hand: list[str]                # cards currently in hand
    my_score: int
    opponent_score: int
    supply: dict[str, SupplyPile]     # {card_name: SupplyPile}
    trash_contents: dict[str, int]
    provinces_remaining: int
    game_total_turns: int             # opponent's turn count too
    buyable: list[str]                # card names I can legally buy right now

@dataclass
class SupplyPile:
    name: str
    cost: int
    remaining: int
    card_types: list[str]             # ["Action", "Attack"]
    description: str                  # english text of card effect

@dataclass
class ActionState:
    hand: list[str]                   # card names in hand
    actions: int
    coins: int
    buys: int
    turn_number: int
    my_deck: dict[str, int]
    my_deck_size: int
    my_score: int
    opponent_score: int
    supply: dict[str, SupplyPile]
    playable_actions: list[str]       # action card names in hand I can play

@dataclass
class TrashState:
    hand: list[str]
    turn_number: int
    my_deck: dict[str, int]
    my_deck_size: int

@dataclass
class DiscardState:
    hand: list[str]
    turn_number: int
    my_deck: dict[str, int]

@dataclass
class GainState:
    coins: int
    turn_number: int
    my_deck: dict[str, int]
    my_deck_size: int
    supply: dict[str, SupplyPile]
    gainable: list[str]               # card names that can be gained (cost <= max_cost)
```

## How a single game runs

```
1. Create Game(initcards=kingdom_cards, numplayers=2, quiet=True,
               player_classes=[PlayerClassA, PlayerClassB])
2. game.start_game()
3. while not game.game_over and turn < 400:
       game.turn()
4. Collect scores via game.whoWon()
5. If this game is selected for tracing, capture spectator log
```

## Round-robin structure

Given N players, we play every pair (N choose 2 matchups).
Each matchup plays `num_games_per_matchup` games with player A going first,
then `num_games_per_matchup` games with player B going first (to cancel
first-player advantage).

Total games = N*(N-1)/2 * num_games_per_matchup * 2

After all games, compute Elo or TrueSkill ratings from the full set of results.

## Elo / TrueSkill

Use `trueskill` library if available, otherwise implement basic Elo.
TrueSkill is preferred because:
- It converges faster with fewer games
- It provides an uncertainty estimate (sigma)
- It handles the round-robin structure naturally

Initialize all players at the same rating. Update after each game.
Report final ratings sorted by mu (descending).

## Trace sampling

We don't trace all games (too much data). Per matchup, keep the
`collect_traces` most informative games:
- Worst losses (largest negative VP margin) — most useful for debugging
- Closest games (smallest absolute VP margin) — show marginal decisions
- At least one win if any exist — for contrast

## Player injection — engine change required

One small change to `dominion/game_setup.py`:

In `instantiate_player_class()`, add support for a `player_classes` list passed
through the game args. If present, use those classes instead of the Flag-based
logic. This keeps the existing CLI flow working while allowing programmatic
player injection.

```python
def instantiate_player_class(game, name, use_shelters, player_num, the_uuid):
    # NEW: check for explicit player class
    player_classes = getattr(game, '_player_classes', None)
    if player_classes and player_num < len(player_classes):
        plr_class = player_classes[player_num]
    elif INIT_OPTIONS[Flag.BOT]:
        plr_class = BotPlayer
        name = f"{name}Bot"
        INIT_OPTIONS[Flag.BOT] = False
    elif INIT_OPTIONS[Flag.RANDOBOT]:
        plr_class = RandobotPlayer
        name = f"{name}RandoBot"
        INIT_OPTIONS[Flag.RANDOBOT] -= 1
    else:
        plr_class = TextPlayer

    player = plr_class(
        game=game,
        quiet=game.quiet,
        name=name,
        heirlooms=game.heirlooms,
        use_shelters=use_shelters,
        number=player_num,
    )
    player.uuid = the_uuid
    return player
```

Also store `player_classes` on the Game object during `parse_args`:
```python
game._player_classes = args.get("player_classes", None)
```

## Smoke test: verifying the engine works

A coding agent should be able to verify the tournament engine without human
intervention by running this built-in check:

```bash
uv run python -m tournament.smoke_test
```

This runs a small tournament (BigMoney vs Random, 100 games per matchup)
and asserts:
- BigMoney beats Random with >70% win rate (it should be ~85-95%)
- BigMoney Elo is higher than Random Elo
- Game traces are non-empty and parseable
- All games completed (no crashes, no infinite loops)
- Wall time is reasonable (<30 seconds for 200 games)

If any assertion fails, the smoke test prints diagnostics and exits nonzero.

## File layout

```
tournament/
    __init__.py            # run_tournament() entry point
    engine.py              # single-game runner, player injection
    results.py             # TournamentResult, MatchupResult, GameTrace dataclasses
    ratings.py             # Elo/TrueSkill computation
    heuristic_player.py    # HeuristicPlayer base class + state dataclasses
    trace_collector.py     # spectator log capture + trace sampling
    smoke_test.py          # self-verification: BigMoney vs Random
```

## What this does NOT include

- The meta-loop (agent reasoning about results and rewriting heuristics)
- LLM integration of any kind
- Kingdom curation / selection

This is purely: "run games fast, rate players, report results."

## Performance target

With quiet=True and no LLM calls, a game of base-set Dominion should take
~5-20ms on modern hardware (pure Python, no I/O).
Target: 1000 games in <30 seconds.

If too slow, profile and consider multiprocessing (each worker process gets
its own copy of game_setup module globals, so parallelism is safe).
