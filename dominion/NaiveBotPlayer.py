"""Player is a non-interactive bot with simple Dominion heuristics."""

from __future__ import annotations

import random
import sys
from typing import Any, Callable, Optional, cast

from rich.console import Console

from dominion import Action, Piles
from dominion.Card import Card
from dominion.Option import Option
from dominion.Player import Player


###############################################################################
###############################################################################
###############################################################################
class NaiveBotPlayer(Player):
    """A simple heuristic bot based on move scoring."""

    def __init__(self, game, name: str = "", quiet: bool = False, **kwargs: Any):
        self.colour = "bright_white on black"
        self.console = Console()
        Player.__init__(self, game, name, quiet, **kwargs)

    ###########################################################################
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

    ###########################################################################
    def user_input(self, options: list[Option], prompt: str) -> Option:
        del prompt
        legal = [opt for opt in options if self._option_is_legal(opt)]
        legal = [opt for opt in legal if opt["action"] != Action.SPENDALL]

        action_moves: list[Option] = []
        treasure_moves: list[Option] = []
        buy_moves: list[Option] = []

        for move in legal:
            if move["action"] in (Action.PLAY, Action.WAY):
                card = move["card"]
                if move["action"] == Action.PLAY and isinstance(card, Card) and card.isTreasure():
                    treasure_moves.append(move)
                else:
                    action_moves.append(move)
            elif move["action"] == Action.SPEND:
                treasure_moves.append(move)
            elif move["action"] in (Action.BUY, Action.EVENT, Action.PROJECT, Action.QUIT):
                buy_moves.append(move)

        if action_moves:
            return self._find_best(action_moves, self._score_action_option)
        if treasure_moves:
            return self._find_best(treasure_moves, self._score_treasure_option)
        if buy_moves:
            return self._find_best(buy_moves, self._score_buy_option)
        if legal:
            return random.choice(legal)

        if not options:
            raise NotImplementedError("No options passed to user_input")
        return options[0]

    ###########################################################################
    @classmethod
    def _option_is_legal(cls, option: Option) -> bool:
        if option["selector"] == "-":
            return False
        if option["action"] in ("", None, Action.NONE):
            return False
        return True

    ###########################################################################
    @classmethod
    def _card_plus_action_count(cls, card: Card) -> int:
        return card.actions

    ###########################################################################
    @classmethod
    def _card_plus_card_count(cls, card: Card) -> int:
        return card.cards

    ###########################################################################
    @classmethod
    def _is_curse(cls, card: Card) -> bool:
        return card.name == "Curse"

    ###########################################################################
    def _score_action_card(self, card: Card) -> int:
        if card.name == "Throne Room":
            return 14
        if self._card_plus_action_count(card) >= 1:
            return 13
        if self.actions.get() >= 2 and self._card_plus_card_count(card):
            return 12
        return card.cost

    ###########################################################################
    def _score_action_option(self, move: Option) -> int:
        card = move["card"]
        if not isinstance(card, Card):
            return 0
        return self._score_action_card(card)

    ###########################################################################
    def _score_treasure_option(self, move: Option) -> int:
        card = move["card"]
        if card is None:
            return 0
        return cast(int, getattr(card, "cost", 0))

    ###########################################################################
    def _score_buy_option(self, move: Option) -> int:
        if move["action"] == Action.QUIT:
            return 0
        card = move["card"]
        if isinstance(card, Card) and self._is_curse(card):
            return -1
        return cast(int, getattr(card, "cost", 0))

    ###########################################################################
    def _score_discard_card(self, card: Card) -> int:
        if self._is_curse(card):
            return 1
        if card.isVictory():
            return 2
        return -card.cost

    ###########################################################################
    def _score_trash_card(self, card: Card) -> int:
        if self._is_curse(card):
            return 1
        return -card.cost

    ###########################################################################
    def _score_gain_card(self, card: Card) -> int:
        if self._is_curse(card):
            return -1
        return card.cost

    ###########################################################################
    @classmethod
    def _find_best(cls, values: list[Any], score_fn: Callable[[Any], float]) -> Any:
        if not values:
            raise ValueError("Need at least one value")

        best_values = [values[0]]
        best_score = score_fn(values[0])
        for value in values[1:]:
            this_score = score_fn(value)
            if this_score > best_score:
                best_values = [value]
                best_score = this_score
            elif this_score == best_score:
                best_values.append(value)
        return random.choice(best_values)

    ###########################################################################
    def _card_sel_source(self, **kwargs: Any) -> list[Card]:
        if "cardsrc" in kwargs:
            if isinstance(kwargs["cardsrc"], Piles):
                select_from = self.piles[kwargs["cardsrc"]]
            else:
                select_from = kwargs["cardsrc"]
        else:
            select_from = self.piles[Piles.HAND]
        return list(select_from)

    ###########################################################################
    def _scored_card_selection(
        self,
        cards: list[Card],
        max_to_select: int,
        score_fn: Callable[[Card], int],
        force: bool,
    ) -> list[Card]:
        available = cards[:]
        selected: list[Card] = []
        while available and len(selected) < max_to_select:
            best_card = self._find_best(available, score_fn)
            score = score_fn(best_card)
            if not force and score <= 0:
                break
            selected.append(best_card)
            available.remove(best_card)
        return selected

    ###########################################################################
    def _default_card_selection(
        self, cards: list[Card], max_to_select: int, force: bool, any_num: bool
    ) -> list[Card]:
        if any_num and not force:
            return []
        if not force and max_to_select == 1:
            return [random.choice(cards)]

        available = cards[:]
        selected = []
        while available and len(selected) < max_to_select:
            card = random.choice(available)
            selected.append(card)
            available.remove(card)
        return selected

    ###########################################################################
    def card_sel(self, num: int = 1, **kwargs: Any) -> list[Card]:
        cards = self._card_sel_source(**kwargs)
        if not cards:
            return []

        any_num = kwargs.get("anynum", False)
        force = kwargs.get("force", False)
        verbs = kwargs.get("verbs", ("Select", "Unselect"))
        primary_verb = str(verbs[0]).lower() if verbs else ""

        max_to_select = len(cards) if any_num else min(num, len(cards))
        if max_to_select <= 0:
            return []

        if primary_verb == "discard":
            score_fn = self._score_discard_card
        elif primary_verb == "trash":
            score_fn = self._score_trash_card
        elif primary_verb in ("get", "gain", "buy"):
            score_fn = self._score_gain_card
        else:
            return self._default_card_selection(cards, max_to_select, force, any_num)

        return self._scored_card_selection(cards, max_to_select, score_fn, force)

    ###########################################################################
    def card_pile_sel(self, num: int = 1, **kwargs: Any) -> list[str] | None:
        del num
        if kwargs.get("cardsrc"):
            piles = [(key, value) for key, value in self.game.get_card_piles() if key in kwargs["cardsrc"]]
        else:
            piles = self.game.get_card_piles()

        if not piles:
            return None

        force = kwargs.get("force", False)
        names = [name for name, _ in piles]
        best_name = self._find_best(names, lambda name: self._score_gain_card(self.game.card_instances[name]))
        if not force and self._score_gain_card(self.game.card_instances[best_name]) <= 0:
            return None
        return [best_name]

    ###########################################################################
    @classmethod
    def _pick_bool_choice(cls, choices: tuple[tuple[str, Any], ...], desired: bool) -> Optional[bool]:
        for _, value in choices:
            if isinstance(value, bool) and value == desired:
                return value
        return None

    ###########################################################################
    def _score_choice(self, choice: tuple[str, Any], prompt: str) -> float:
        desc, value = choice
        del prompt
        if isinstance(value, Card):
            return float(self._score_action_card(value))
        if value is False or value is None:
            return 0
        if isinstance(value, bool):
            return 1
        if isinstance(value, (int, float)):
            return float(value)
        text = desc.lower()
        if text.startswith(("don't", "do not", "no ", "skip")):
            return 0
        return 0.5

    ###########################################################################
    def plr_choose_options(self, prompt: str, *choices: tuple[str, Any]) -> Any:
        if not choices:
            return None

        lower_prompt = prompt.lower()
        if "trash" in lower_prompt:
            should_trash = any(self._score_trash_card(card) > 0 for card in self.piles[Piles.HAND])
            choice = self._pick_bool_choice(choices, should_trash)
            if choice is not None:
                return choice
        if "discard" in lower_prompt:
            should_discard = any(self._score_discard_card(card) > 0 for card in self.piles[Piles.HAND])
            choice = self._pick_bool_choice(choices, should_discard)
            if choice is not None:
                return choice

        best_choice = self._find_best(list(choices), lambda choice: self._score_choice(choice, prompt))
        return best_choice[1]

    ###########################################################################
    def pick_to_discard(self, num_to_discard: int, keepvic: bool = False) -> list[Card]:
        """Many attacks require this sort of response. Return num cards to discard."""
        if num_to_discard <= 0:
            return []
        to_discard = []

        for card in self.piles[Piles.HAND]:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            to_discard.append(card)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]

        while len(to_discard) < num_to_discard:
            for treas in ("Copper", "Silver", "Gold"):
                for card in self.piles[Piles.HAND]:
                    if card.name == treas:
                        to_discard.append(card)
        if len(to_discard) >= num_to_discard:
            return to_discard[:num_to_discard]

        hand = ", ".join([_.name for _ in self.piles[Piles.HAND]])
        sys.stderr.write(f"Couldn't find cards to discard {num_to_discard} from {hand}")
        sys.stderr.write(f"Managed to get {(', '.join([_.name for _ in to_discard]))} so far\n")
        return []


# EOF
