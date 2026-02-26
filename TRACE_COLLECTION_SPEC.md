# Trace Collection Fix — Spec

## Problem

`GameTrace.spectator_log` comes back empty because:
1. Games run `quiet=True` — `Player.output()` buffers to `self.messages` but
   doesn't print. `Game.output()` does nothing.
2. `self.messages` is cleared every turn (`Player.end_turn` resets it).
3. The stdout redirect in `engine.py` doesn't catch Rich console output anyway.
4. `collect_trace=True` runs on ALL games — wasteful.

## Approach

Build the game log ourselves at the engine level by inspecting game state
after each turn. No engine changes needed.

### Two-pass strategy

**All games (fast path):** Run with `quiet=True`, no tracing overhead.
Only record outcome, scores, turn count. After all games finish, the
TraceCollector identifies which games to trace (worst losses, closest, etc.)
by VP margin.

**Traced games (slow path):** Re-run only the ~5 selected games with their
original seeds, this time with a `TracingGame` wrapper that hooks into
the turn loop and records events.

This means:
- 99.5% of games run at full speed with zero overhead
- Only ~5 games per matchup are re-run with tracing
- Traces are 100% accurate (same seed = same game)

### TracingGame wrapper

Don't subclass or modify `Game`. Instead, wrap the turn loop:

```python
def run_traced_game(kingdom_cards, player_classes, seed) -> str:
    """Re-run a game with the given seed and capture a structured log."""
    random.seed(seed)
    game = Game(initcards=kingdom_cards, numplayers=2, quiet=True,
                player_classes=player_classes)
    game.start_game()

    log_lines = []
    turn = 0

    while not game.game_over and turn < 400:
        # Record state BEFORE the turn
        current = game.current_player
        next_player = game.player_to_left(current)

        # Snapshot pre-turn state
        pre_hand = [c.name for c in next_player.piles[Piles.HAND]]
        pre_coins = next_player.coins.get()

        game.turn()
        turn += 1

        # Now next_player just finished their turn.
        # Read what happened from stats (bought, gained, trashed)
        player = next_player
        turn_num = player.turn_number

        log_lines.append(f"Turn {turn_num} - {player.name}")
        log_lines.append(f"  Hand: {', '.join(pre_hand)}")

        if player.stats["bought"]:
            buys = ', '.join(c.name for c in player.stats["bought"])
            log_lines.append(f"  Bought: {buys}")

        if player.stats["gained"]:
            # Exclude cards that were also bought (gain_card is called by buy)
            bought_names = {c.name for c in player.stats["bought"]}
            pure_gains = [c for c in player.stats["gained"]
                          if c.name not in bought_names]
            if pure_gains:
                gains = ', '.join(c.name for c in pure_gains)
                log_lines.append(f"  Gained: {gains}")

        if player.stats["trashed"]:
            trashed = ', '.join(c.name for c in player.stats["trashed"])
            log_lines.append(f"  Trashed: {trashed}")

        # Also capture played cards from the played pile
        # (these get discarded in cleanup but we read before that)
        # Actually, stats["bought"] etc. are the main signal.
        # We can also read messages that were buffered this turn.
        if player.messages:
            for msg in player.messages:
                log_lines.append(f"  > {msg}")

    # Final scores
    log_lines.append("")
    for p in game.player_list():
        score = p.get_score()
        cards = p.get_cards()
        deck_str = ', '.join(f"{k}={v}" for k, v in sorted(cards.items()))
        log_lines.append(f"{p.name}: {score} VP  [{deck_str}]")

    return '\n'.join(log_lines)
```

Wait — `player.stats` is reset at `start_turn()`, not `end_turn()`:

```python
# Player.py line 823
self.stats = {"gained": [], "bought": [], "trashed": []}
```

That's in `start_turn()`. And `messages` is cleared in `end_turn()` (line 916).
The turn flow is: `start_turn() → do_turn() → end_turn()`.

So by the time `game.turn()` returns, `stats` still has this turn's data
(cleared at next `start_turn()`), but `messages` is already cleared.

**Fix for messages:** We need to capture messages BEFORE `end_turn` clears them.
But we can't hook into the turn loop without modifying Player.

**Simpler approach:** Forget messages. The `stats` dict (bought/gained/trashed)
plus the pre-turn hand is enough for the meta-agent. The meta-agent doesn't
need "JoshuaBot gets +$1" per-copper-play detail — it needs to know what was
bought, what was trashed, what the hand was.

Actually — `messages` is cleared in the `do_turn` method before `end_turn`:

```python
# Player.py line 916 (in end_turn):
self.messages = []
```

But `game.turn()` calls `player.turn()` which calls `start_turn() → do_turn() → end_turn()`.
So after `game.turn()` returns, messages are cleared.

**Revised approach: capture messages by monkey-patching output().**

For traced games only, replace each player's `output` method with one that
appends to a shared log. This is clean because:
- Only done for ~5 re-run games, not all 10,000
- The monkey-patch is local to the traced game
- We get the full message stream including "Bought Gold for 6 coin", etc.

## Spec

### Changes to `engine.py`

1. **All games:** Run with `collect_trace=False`. Only store outcome, scores,
   turn count, and the **seed** used for that game.

2. **After all games in a matchup:** TraceCollector identifies which games
   to trace (by VP margin, same as now).

3. **Re-run traced games:** For each selected game, re-run with the same seed
   and `_run_traced_game()` which captures a full log.

### `_run_traced_game()`

```python
def _run_traced_game(kingdom_cards, player_classes, seed) -> str:
    random.seed(seed)
    game = Game(initcards=kingdom_cards, numplayers=2, quiet=True,
                player_classes=player_classes)
    game.start_game()

    # Shared log buffer
    log_lines = []

    # Monkey-patch output on all players and the game
    def make_player_output(player, log):
        def patched_output(msg, end="\n"):
            log.append(f"{player.name}: {msg}")
            player.messages.append(msg)
        return patched_output

    def make_game_output(log):
        def patched_output(msg):
            log.append(f"ALL: {msg}")
        return patched_output

    for p in game.player_list():
        p.output = make_player_output(p, log_lines)
    game.output = make_game_output(log_lines)

    turn = 0
    while not game.game_over and turn < 400:
        game.turn()
        turn += 1

    # Final scores
    for p in game.player_list():
        score = p.get_score()
        cards = p.get_cards()
        deck_str = ', '.join(f"{k}={v}" for k, v in sorted(cards.items()))
        log_lines.append(f"FINAL: {p.name}: {score} VP  [{deck_str}]")

    return '\n'.join(log_lines)
```

### Changes to TraceCollector

Add a `get_games_to_retrace()` method that returns the seeds/game numbers
of selected games, before the full GameTrace is built. The flow becomes:

```
1. Run all games fast (no tracing) → collect (outcome, scores, turns, seed)
2. TraceCollector picks which games to retrace by VP margin
3. Re-run those games with _run_traced_game() → get spectator_log
4. Build GameTrace objects with the log populated
```

### Changes to results.py

Keep `GameTrace` as-is. The `spectator_log` field gets populated by the
re-run, not by the fast pass.

### Performance impact

- Fast games: no change (no trace overhead)
- Per matchup: ~5 extra games re-run with output capture
- Total overhead: ~5 * 2 * (N_matchups) extra games ≈ negligible

### What the trace looks like

```
OliviaBot: ************ Action Phase ************
OliviaBot: | Hand (5): Copper, Copper, Silver, Chapel, Estate
OliviaBot: ************ Buy Phase ************
OliviaBot: Bought Gold for 6 coin
OliviaBot: draws 3 Coppers and 2 Estates.
JoshuaBot: ************ Action Phase ************
JoshuaBot: | Hand (5): Copper, Copper, Copper, Estate, Estate
JoshuaBot: ************ Buy Phase ************
JoshuaBot: Have 3 coins
JoshuaBot: Bought Silver for 3 coin
...
FINAL: OliviaBot: 34 VP  [Copper=2, Gold=4, Province=4, Silver=3]
FINAL: JoshuaBot: 22 VP  [Copper=5, Duchy=2, Estate=3, Gold=2, Province=1, Silver=4]
```

This gives the meta-agent everything it needs: what each player's hand was,
what they bought/played, and the final deck composition.
