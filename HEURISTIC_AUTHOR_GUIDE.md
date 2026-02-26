# Heuristic Author Guide

You are writing a Dominion heuristic player. You subclass `HeuristicPlayer`
and override strategy methods. The base class handles all engine integration
(treasure spending, option routing, card selection mapping). You only write
the decision logic.

## What you write

A single Python file that subclasses `HeuristicPlayer`:

```python
from tournament.heuristic_player import HeuristicPlayer

class MyHeuristic(HeuristicPlayer):
    """Chapel-based engine strategy for Village/Smithy kingdom."""

    def buy_priority(self, state):
        # Early game: get one Chapel, then Silver
        if state.turn_number <= 2:
            if "Chapel" not in state.my_deck and "Chapel" in state.buyable:
                return "Chapel"
            if "Silver" in state.buyable:
                return "Silver"

        # Mid game: build economy
        if state.coins >= 8 and "Province" in state.buyable:
            return "Province"
        if state.coins >= 6 and "Gold" in state.buyable:
            return "Gold"
        if state.coins >= 3 and "Silver" in state.buyable:
            return "Silver"
        return None  # end buy phase

    def action_priority(self, state):
        # Always play Chapel when we have junk to trash
        if "Chapel" in state.playable_actions:
            junk = [c for c in state.hand if c in ("Copper", "Estate", "Curse")]
            if junk:
                return "Chapel"

        # Play Village before Smithy (need actions)
        if "Village" in state.playable_actions:
            return "Village"
        if "Smithy" in state.playable_actions:
            return "Smithy"
        return None  # end action phase

    def trash_priority(self, card_names, num, state):
        # Trash Curses > Estates > Coppers, keep at most 3 Coppers
        priority = ["Curse", "Estate"]
        coppers_in_deck = state.my_deck.get("Copper", 0)
        if coppers_in_deck > 3:
            priority.append("Copper")

        result = []
        available = list(card_names)
        for target in priority:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)
        return result
```

## Methods you can override

### `buy_priority(self, state: BuyState) -> str | None`

Called each time you can buy a card (may be called multiple times per turn
if you have +Buys). Treasures are already spent before this is called.

**Return:** Card name to buy (e.g. `"Silver"`), or `None` to stop buying.

**Default:** BigMoney (Province ≥8, Gold ≥6, Duchy ≥5, Silver ≥3).

---

### `action_priority(self, state: ActionState) -> str | None`

Called each time you can play an action card. Called repeatedly until you
return `None` or run out of actions.

**Return:** Card name to play (e.g. `"Village"`), or `None` to end action phase.

**Default:** Play the first playable action card found.

---

### `trash_priority(self, card_names: list[str], num: int, state: TrashState) -> list[str]`

Called when you must/may choose cards to trash (e.g. Chapel says "trash up to 4").

- `card_names` — names of cards you *can* trash (usually your hand)
- `num` — max cards to trash

**Return:** List of card names to trash (can be shorter than `num` if trashing
is optional, i.e. "up to N").

**Default:** Trash Curses, then Estates, then Coppers.

---

### `discard_priority(self, card_names: list[str], num: int, state: DiscardState) -> list[str]`

Called when you must discard cards (e.g. Militia forces discard down to 3).

- `card_names` — names of cards you can discard
- `num` — how many you must discard

**Return:** List of card names to discard (exactly `num`).

**Default:** Discard victory cards first, then cheapest cards.

---

### `gain_priority(self, max_cost: int, state: GainState) -> str | None`

Called when you gain a card up to a cost (e.g. Workshop: "gain a card costing
up to 4").

- `max_cost` — maximum cost of card you can gain

**Return:** Card name to gain, or `None` to gain nothing (if optional).

**Default:** Gain the most expensive card available.

---

## State objects you receive

### BuyState

```python
state.coins: int                  # coins available after spending treasures
state.buys: int                   # buys remaining this turn
state.actions_remaining: int      # actions left (usually 0 in buy phase)
state.turn_number: int            # current turn (1-indexed)
state.my_deck: dict[str, int]     # ALL your cards: {"Copper": 4, "Silver": 2, ...}
state.my_deck_size: int           # total cards you own
state.my_hand: list[str]          # cards currently in hand
state.my_score: int               # your current VP
state.opponent_score: int         # opponent's current VP
state.supply: dict[str, SupplyPile]  # all supply piles (see below)
state.trash_contents: dict[str, int] # shared trash pile contents
state.provinces_remaining: int    # Provinces left in supply
state.game_total_turns: int       # total turns played by all players
state.buyable: list[str]          # card names you can legally buy right now
```

### ActionState

```python
state.hand: list[str]             # card names in your hand
state.actions: int                # action plays remaining
state.coins: int                  # coins accumulated so far this turn
state.buys: int                   # buys available
state.turn_number: int
state.my_deck: dict[str, int]     # all your cards
state.my_deck_size: int
state.my_score: int
state.opponent_score: int
state.supply: dict[str, SupplyPile]
state.playable_actions: list[str] # action cards in hand you can play right now
```

### TrashState

```python
state.hand: list[str]             # your full hand
state.turn_number: int
state.my_deck: dict[str, int]     # all your cards
state.my_deck_size: int
```

### DiscardState

```python
state.hand: list[str]
state.turn_number: int
state.my_deck: dict[str, int]
```

### GainState

```python
state.coins: int
state.turn_number: int
state.my_deck: dict[str, int]
state.my_deck_size: int
state.supply: dict[str, SupplyPile]
state.gainable: list[str]         # card names you can gain (cost ≤ max_cost)
```

### SupplyPile (nested in supply dicts)

```python
pile.name: str                    # "Village", "Smithy", etc.
pile.cost: int                    # coin cost
pile.remaining: int               # cards left in pile
pile.card_types: list[str]        # ["Action"], ["Action", "Attack"], ["Treasure"], etc.
pile.description: str             # English text of card effect when played
```

## What you do NOT need to handle

- **Treasure spending** — the engine auto-spends all treasures before calling `buy_priority`
- **Option/selector routing** — the engine maps your card name return to the right game option
- **Illegal moves** — if you return a card name that's not in `buyable`/`playable_actions`/etc., the engine falls back to the default behavior
- **Night phase** — handled by default (plays night cards if available)
- **Debt payback** — handled by engine automatically
- **Game engine API** — you never touch `self.game`, `self.piles`, `Option` objects, or `Action` enums directly

## Tips

- `state.my_deck` counts ALL your cards (hand + deck + discard + played). Use this
  to track what you've bought and plan future purchases.
- Check `state.provinces_remaining` to decide when to switch from building to buying VP.
- `state.supply["Card Name"].description` gives you the English text of any card's effect.
- Return `None` from `buy_priority` to stop buying, even if you have buys and coins left.
  Don't buy cards just because you can afford them.
- The default behavior is BigMoney. If your heuristic doesn't override a method,
  it does something reasonable. You can start by only overriding `buy_priority` and
  iterate from there.
