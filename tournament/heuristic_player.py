"""HeuristicPlayer base class — engine glue + defaults.

The meta-agent subclasses this and overrides the strategy methods
(buy_priority, action_priority, trash_priority, discard_priority, gain_priority).
Everything else in this file is engine plumbing that the meta-agent never touches.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Optional

from rich.console import Console

from dominion import Action, Phase, Piles
from dominion.Card import Card
from dominion.Option import Option
from dominion.Player import Player


# ---------------------------------------------------------------------------
# State dataclasses — these are what the heuristic methods receive
# ---------------------------------------------------------------------------

@dataclass
class SupplyPile:
    name: str
    cost: int
    remaining: int
    card_types: list[str]       # ["Action"], ["Action", "Attack"], etc.
    description: str            # english text of card effect

@dataclass
class BuyState:
    coins: int
    buys: int
    actions_remaining: int
    turn_number: int
    my_deck: dict[str, int]     # ALL owned cards: {"Copper": 4, "Silver": 2, ...}
    my_deck_size: int
    my_hand: list[str]
    my_score: int
    opponent_score: int
    supply: dict[str, SupplyPile]
    trash_contents: dict[str, int]
    provinces_remaining: int
    game_total_turns: int
    buyable: list[str]          # card names legally buyable right now

@dataclass
class ActionState:
    hand: list[str]
    actions: int
    coins: int
    buys: int
    turn_number: int
    my_deck: dict[str, int]
    my_deck_size: int
    my_score: int
    opponent_score: int
    supply: dict[str, SupplyPile]
    playable_actions: list[str]

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
    gainable: list[str]


# ---------------------------------------------------------------------------
# HeuristicPlayer
# ---------------------------------------------------------------------------

class HeuristicPlayer(Player):
    """Base class for agent-written heuristic players.

    Override the ``*_priority`` methods to implement strategy.
    The base class provides BigMoney-ish defaults so a partial
    heuristic still plays legal games.
    """

    def __init__(self, game: Any, name: str = "", quiet: bool = False, **kwargs: Any):
        self.colour = "green on black"
        self.console = Console()
        super().__init__(game, name, quiet, **kwargs)

    # ===================================================================
    # Strategy methods — the meta-agent overrides these
    # ===================================================================

    def buy_priority(self, state: BuyState) -> Optional[str]:
        """Return card name to buy, or None to end buy phase."""
        # Default: BigMoney
        if state.coins >= 8 and "Province" in state.buyable:
            return "Province"
        if state.coins >= 6 and "Gold" in state.buyable:
            return "Gold"
        if state.coins >= 5 and "Duchy" in state.buyable:
            return "Duchy"
        if state.coins >= 3 and "Silver" in state.buyable:
            return "Silver"
        return None

    def action_priority(self, state: ActionState) -> Optional[str]:
        """Return card name to play, or None to end action phase."""
        # Default: play first available action
        if state.playable_actions:
            return state.playable_actions[0]
        return None

    def trash_priority(self, card_names: list[str], num: int, state: TrashState) -> list[str]:
        """Return list of card names to trash (up to num)."""
        # Default: trash Curses, then Estates, then Coppers
        priority = ["Curse", "Estate", "Copper"]
        result: list[str] = []
        available = list(card_names)
        for target in priority:
            while target in available and len(result) < num:
                available.remove(target)
                result.append(target)
        return result

    def discard_priority(self, card_names: list[str], num: int, state: DiscardState) -> list[str]:
        """Return list of card names to discard (exactly num)."""
        # Default: discard victory cards first, then cheapest
        victory = []
        non_victory = []
        for name in card_names:
            card_inst = self.game.card_instances.get(name)
            if card_inst and card_inst.isVictory():
                victory.append(name)
            else:
                non_victory.append(name)
        # Sort non-victory by cost ascending (cheapest first)
        non_victory.sort(key=lambda n: getattr(self.game.card_instances.get(n), "cost", 0))
        ordered = victory + non_victory
        return ordered[:num]

    def gain_priority(self, max_cost: int, state: GainState) -> Optional[str]:
        """Return card name to gain, or None to gain nothing."""
        # Default: gain most expensive treasure available
        best_name = None
        best_cost = -1
        for name in state.gainable:
            pile = state.supply.get(name)
            if pile and pile.cost <= max_cost and pile.cost > best_cost:
                # Prefer treasures, then anything
                if "Treasure" in pile.card_types:
                    best_name = name
                    best_cost = pile.cost
        if best_name:
            return best_name
        # Fall back to most expensive anything
        for name in state.gainable:
            pile = state.supply.get(name)
            if pile and pile.cost <= max_cost and pile.cost > best_cost:
                best_name = name
                best_cost = pile.cost
        return best_name

    # ===================================================================
    # Engine glue — never overridden by meta-agent
    # ===================================================================

    def output(self, msg: str, end: str = "\n") -> None:
        self.messages.append(msg)
        if self.quiet:
            return
        prompt = f"[{self.colour}]{self.name}[/]: "
        current_card_stack = ""
        try:
            for card in self.currcards:
                current_card_stack += f"{card.name}> "
        except IndexError:
            pass
        self.console.print(f"{prompt}{current_card_stack}{msg}", end=end)

    # ------------------------------------------------------------------
    # Internal state builders
    # ------------------------------------------------------------------

    def _build_supply_dict(self) -> dict[str, SupplyPile]:
        supply: dict[str, SupplyPile] = {}
        for name, cp in self.game.card_piles.items():
            card = self.game.card_instances.get(name)
            if card is None:
                continue
            types: list[str] = []
            if card.isAction():
                types.append("Action")
            if card.isTreasure():
                types.append("Treasure")
            if card.isVictory():
                types.append("Victory")
            if card.isAttack():
                types.append("Attack")
            # description() requires a player arg
            try:
                desc = " ".join(card.description(self).split())
            except Exception:
                desc = ""
            supply[name] = SupplyPile(
                name=name,
                cost=card.cost,
                remaining=len(cp),
                card_types=types,
                description=desc,
            )
        return supply

    def _get_deck_counts(self) -> tuple[dict[str, int], int]:
        counts: dict[str, int] = {}
        total = 0
        for pile_key in (Piles.DECK, Piles.DISCARD, Piles.HAND, Piles.PLAYED,
                         Piles.DURATION, Piles.RESERVE, Piles.DEFER, Piles.EXILE):
            for c in self.piles[pile_key]:
                counts[c.name] = counts.get(c.name, 0) + 1
                total += 1
        return counts, total

    def _get_opponent_score(self) -> int:
        for p in self.game.player_list():
            if p is not self:
                return p.get_score()
        return 0

    def _get_trash_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for c in self.game.trash_pile:
            counts[c.name] = counts.get(c.name, 0) + 1
        return counts

    def _get_provinces_remaining(self) -> int:
        pile = self.game.card_piles.get("Province")
        if pile is None:
            return 0
        return len(pile)

    def _find_option(self, options: list[Option], action: Action | str, card_name: str) -> Optional[Option]:
        """Find an Option matching a given action type and card name."""
        for opt in options:
            if opt["action"] == action and opt["card"] is not None and opt["card"].name == card_name:
                return opt
        return None

    def _find_quit(self, options: list[Option]) -> Option:
        """Find the quit/end-phase option."""
        for opt in options:
            if opt["action"] == Action.QUIT:
                return opt
        # Should always exist, but just in case return first option
        return options[0]

    def _find_spendall(self, options: list[Option]) -> Optional[Option]:
        """Find the 'spend all treasures' option."""
        for opt in options:
            if opt["action"] == Action.SPENDALL:
                return opt
        return None

    def _find_payback(self, options: list[Option]) -> Optional[Option]:
        """Find the 'payback debt' option."""
        for opt in options:
            if opt["action"] == Action.PAYBACK:
                return opt
        return None

    # ------------------------------------------------------------------
    # user_input — the main routing method
    # ------------------------------------------------------------------

    def user_input(self, options: list[Option], prompt: str) -> Option:
        """Route engine option prompts to the right heuristic method.

        The engine calls this in a loop. We must return a valid Option
        from the options list every time.
        """
        # ------- BUY PHASE -------
        if self.phase == Phase.BUY:
            # Step 1: always spend all treasures first
            spendall = self._find_spendall(options)
            if spendall is not None:
                return spendall

            # Step 2: pay back debt if we have any
            payback = self._find_payback(options)
            if payback is not None:
                return payback

            # Step 3: if no buys left, quit
            if self.buys.get() <= 0:
                return self._find_quit(options)

            # Step 4: ask the heuristic what to buy
            deck_counts, deck_size = self._get_deck_counts()
            buyable = [opt["card"].name for opt in options
                       if opt["action"] == Action.BUY and opt["card"] is not None]

            state = BuyState(
                coins=self.coins.get(),
                buys=self.buys.get(),
                actions_remaining=self.actions.get(),
                turn_number=self.turn_number,
                my_deck=deck_counts,
                my_deck_size=deck_size,
                my_hand=[c.name for c in self.piles[Piles.HAND]],
                my_score=self.get_score(),
                opponent_score=self._get_opponent_score(),
                supply=self._build_supply_dict(),
                trash_contents=self._get_trash_counts(),
                provinces_remaining=self._get_provinces_remaining(),
                game_total_turns=sum(p.turn_number for p in self.game.player_list()),
                buyable=buyable,
            )

            choice = self.buy_priority(state)
            if choice:
                opt = self._find_option(options, Action.BUY, choice)
                if opt is not None:
                    return opt
            # Nothing to buy or heuristic returned None
            return self._find_quit(options)

        # ------- ACTION PHASE -------
        if self.phase == Phase.ACTION:
            playable = [opt["card"].name for opt in options
                        if opt["action"] == Action.PLAY and opt["card"] is not None]

            if not playable:
                return self._find_quit(options)

            deck_counts, deck_size = self._get_deck_counts()
            state = ActionState(
                hand=[c.name for c in self.piles[Piles.HAND]],
                actions=self.actions.get(),
                coins=self.coins.get(),
                buys=self.buys.get(),
                turn_number=self.turn_number,
                my_deck=deck_counts,
                my_deck_size=deck_size,
                my_score=self.get_score(),
                opponent_score=self._get_opponent_score(),
                supply=self._build_supply_dict(),
                playable_actions=playable,
            )

            choice = self.action_priority(state)
            if choice:
                opt = self._find_option(options, Action.PLAY, choice)
                if opt is not None:
                    return opt
            return self._find_quit(options)

        # ------- NIGHT PHASE -------
        if self.phase == Phase.NIGHT:
            # Default: play night cards if available, else quit
            for opt in options:
                if opt["action"] == Action.PLAY and opt["card"] is not None:
                    return opt
            return self._find_quit(options)

        # ------- FALLBACK -------
        return self._find_quit(options)

    # ------------------------------------------------------------------
    # card_sel — card selection routing (trash, discard, gain, etc.)
    # ------------------------------------------------------------------

    def card_sel(self, num: int = 1, **kwargs: Any) -> list[Card]:
        """Route card selection prompts to the right heuristic method."""
        # Resolve the source cards
        cardsrc = kwargs.get("cardsrc", Piles.HAND)
        if isinstance(cardsrc, Piles):
            cards = list(self.piles[cardsrc])
        else:
            cards = list(cardsrc)

        if not cards:
            return []

        card_names = [c.name for c in cards]
        force = kwargs.get("force", False)
        anynum = kwargs.get("anynum", False)
        verbs = kwargs.get("verbs", ("Select", "Unselect"))
        primary_verb = str(verbs[0]).lower() if verbs else ""

        max_to_select = len(cards) if anynum else min(num, len(cards))
        if max_to_select <= 0:
            return []

        deck_counts, deck_size = self._get_deck_counts()
        selected_names: list[str] = []

        if primary_verb == "trash":
            state = TrashState(
                hand=[c.name for c in self.piles[Piles.HAND]],
                turn_number=self.turn_number,
                my_deck=deck_counts,
                my_deck_size=deck_size,
            )
            selected_names = self.trash_priority(card_names, max_to_select, state)

        elif primary_verb == "discard":
            state = DiscardState(
                hand=[c.name for c in self.piles[Piles.HAND]],
                turn_number=self.turn_number,
                my_deck=deck_counts,
            )
            selected_names = self.discard_priority(card_names, max_to_select, state)

        elif primary_verb in ("get", "gain"):
            supply = self._build_supply_dict()
            gainable = [c.name for c in cards]
            state = GainState(
                coins=self.coins.get(),
                turn_number=self.turn_number,
                my_deck=deck_counts,
                my_deck_size=deck_size,
                supply=supply,
                gainable=gainable,
            )
            # For gain, we only pick one
            choice = self.gain_priority(max(c.cost for c in cards), state)
            if choice:
                selected_names = [choice]

        else:
            # Unknown verb — use a simple default
            if force:
                selected_names = card_names[:max_to_select]
            elif anynum:
                selected_names = []
            else:
                selected_names = card_names[:max_to_select] if force else []

        # If force and heuristic returned too few, fill with remaining cards
        if force and len(selected_names) < max_to_select:
            for name in card_names:
                if name not in selected_names and len(selected_names) < max_to_select:
                    selected_names.append(name)

        # Map names back to Card objects (matching order, no duplicates)
        selected_cards: list[Card] = []
        used_indices: set[int] = set()
        for name in selected_names:
            for i, c in enumerate(cards):
                if i not in used_indices and c.name == name:
                    selected_cards.append(c)
                    used_indices.add(i)
                    break

        return selected_cards

    # ------------------------------------------------------------------
    # card_pile_sel — pile selection (for some gain effects)
    # ------------------------------------------------------------------

    def card_pile_sel(self, num: int = 1, **kwargs: Any) -> list[str] | None:
        """Pick a card pile from the supply."""
        if kwargs.get("cardsrc"):
            piles = [(key, value) for key, value in self.game.get_card_piles()
                     if key in kwargs["cardsrc"]]
        else:
            piles = list(self.game.get_card_piles())

        if not piles:
            return None

        # Simple heuristic: pick highest cost non-curse pile
        best_name = None
        best_cost = -1
        for name, _ in piles:
            card = self.game.card_instances.get(name)
            if card and card.name != "Curse" and card.cost > best_cost:
                best_name = name
                best_cost = card.cost

        if best_name:
            return [best_name]
        # Fallback: first pile
        return [piles[0][0]]

    # ------------------------------------------------------------------
    # plr_choose_options — multiple choice prompts
    # ------------------------------------------------------------------

    def plr_choose_options(self, prompt: str, *choices: tuple[str, Any]) -> Any:
        """Handle multiple-choice prompts from card effects."""
        if not choices:
            return None

        # For boolean choices, prefer "no" / "don't" to avoid risky actions
        lower_prompt = prompt.lower()

        # If asked about trashing, check if we have junk to trash
        if "trash" in lower_prompt:
            junk = [c for c in self.piles[Piles.HAND]
                    if c.name in ("Curse", "Estate", "Copper")]
            desired = bool(junk)
            for desc, val in choices:
                if isinstance(val, bool) and val == desired:
                    return val

        # If asked about discarding, prefer not to
        if "discard" in lower_prompt:
            for desc, val in choices:
                if isinstance(val, bool) and val is False:
                    return val

        # Default: pick the first choice (usually the "safe" option)
        return choices[0][1]

    # ------------------------------------------------------------------
    # pick_to_discard — attack response helper
    # ------------------------------------------------------------------

    def pick_to_discard(self, num_to_discard: int, keepvic: bool = False) -> list[Card]:
        """Discard cards when attacked (e.g. Militia)."""
        if num_to_discard <= 0:
            return []

        to_discard: list[Card] = []

        # Discard non-treasures first
        for card in self.piles[Piles.HAND]:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            to_discard.append(card)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]

        # Then cheapest treasures
        treasures = sorted(
            [c for c in self.piles[Piles.HAND] if c.isTreasure() and c not in to_discard],
            key=lambda c: c.cost,
        )
        to_discard.extend(treasures)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]

        # Shouldn't happen, but return what we have
        return to_discard[:num_to_discard]
