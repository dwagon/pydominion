#!/usr/bin/env python3
""" All the Player based stuff """
# pylint: disable=too-many-instance-attributes, too-many-public-methods
from __future__ import annotations

import contextlib
import json
import operator
import sys
from collections import defaultdict
from typing import Any, Optional, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from dominion.Game import Game

from dominion import Piles, Phase, Limits, NoCardException
from dominion.Card import Card, CardType
from dominion.CardPile import CardPile
from dominion.Counter import Counter
from dominion.Event import Event
from dominion.Option import Option
from dominion.PlayArea import PlayArea
from dominion.Way import Way
from dominion.Hex import Hex
from dominion.Boon import Boon
from dominion.Artifact import Artifact
from dominion.Project import Project
from dominion.State import State


###############################################################################
###############################################################################
###############################################################################
class Player:
    """All things player - generally subclassed for interface reasons"""

    def __init__(
        self,
        game: "Game",
        name: str,
        heirlooms: None | list[str] = None,
        use_shelters: bool = False,
    ) -> None:
        self.game = game
        self.name = name
        self.currcards: list[Card] = []
        self.score: dict[str, int] = {}
        self.had_cards: list[Card] = []
        self.messages: list[str] = []
        self.hooks: dict[str, Any] = {}
        self.piles = {
            Piles.HAND: PlayArea(Piles.HAND, game=self.game),
            Piles.EXILE: PlayArea(Piles.EXILE, game=self.game),
            Piles.DURATION: PlayArea(Piles.DURATION, game=self.game),
            Piles.DEFER: PlayArea(Piles.DEFER, game=self.game),
            Piles.DECK: PlayArea(Piles.DECK, game=self.game),
            Piles.PLAYED: PlayArea(Piles.PLAYED, game=self.game),
            Piles.DISCARD: PlayArea(Piles.DISCARD, game=self.game),
            Piles.RESERVE: PlayArea(Piles.RESERVE, game=self.game),
        }
        self.projects: list[Project] = []
        self.states: list[State] = []
        self.artifacts: list[Artifact] = []

        self.buys = Counter("Buys", 1)
        self.actions = Counter("Actions", 1)
        self.coins = Counter("Coins", 0)
        self.potions = Counter("Potions", 0)
        self.villagers = Counter("Villager", 0)
        self.debt = Counter("Debt", 0)
        self.coffers = Counter("Coffers", 0)
        self.favors = Counter("Favors", 0)
        self.newhandsize = 5
        self.specials: dict[str, Any] = {}  # Used by cards for special reasons
        self.limits: dict[Limits, Optional[int]] = {Limits.PLAY: None, Limits.BUY: 999}
        self.card_token: bool = False
        self.coin_token: bool = False
        self.journey_token: bool = True
        self.test_input: list[str] = []
        self.forbidden_to_buy: list[Card] = []
        self.played_events = PlayArea("played_events", game=self.game)
        self.played_ways: list[tuple[Way, Card]] = []
        self.once: dict[str, bool] = {}
        self.turn_number = 0
        self.stats: dict[str, list[Card]] = {"gained": [], "bought": [], "trashed": []}
        self.secret_count = 0  # Hack to count cards that aren't anywhere normal
        self.end_of_game_cards: list[Card] = []
        self.phase: Phase = Phase.NONE
        self.misc = {"is_start": False, "cleaned": False}
        self.skip_turn: bool = False
        self.uuid: str = ""
        self._initial_deck(heirlooms, use_shelters)
        self._initial_tokens()
        self.pick_up_hand()
        game.output(f"Player {name} is at the table")

    ###########################################################################
    def print_state(self) -> None:
        """Print the player state for debugging"""
        print(f"\n{self.name} {self.turn_number} --------------------------")
        print(f"  state: {', '.join([_.name for _ in self.states])}")
        print(f"  artifacts: {', '.join([_.name for _ in self.artifacts])}")
        print(f"  projects: {', '.join([_.name for _ in self.projects])}")
        for pile in self.piles:
            self.piles[pile].dump(f"  {pile.name}")
        print(f"  score: {self.get_score()} {self.get_score_details()}")
        print(f"  tokens: {self.tokens}")
        print(f"  phase: {self.phase}")
        print(
            f"  coin={self.coins.get()} debt={self.debt.get()} actions={self.actions.get()}"
            f" buys={self.buys.get()} favors={self.favors.get()}"
            f" coffers={self.coffers.get()}"
            f" villagers={self.villagers.get()} potions={self.potions.get()}"
        )
        print("  messages:")
        for msg in self.messages:
            print(f"\t{msg}")

    ###########################################################################
    def _initial_deck(
        self, heirlooms: Optional[list[str]] = None, use_shelters: bool = False
    ) -> None:
        """Provide the initial deck"""
        if heirlooms is None:
            heirlooms = []

        self.piles[Piles.DECK].empty()

        for _ in range(7 - len(heirlooms)):
            card = self.game.get_card_from_pile("Copper")
            self.add_card(card, Piles.DECK)

        for heirloom in heirlooms:
            card = self.game.get_card_from_pile(heirloom)
            self.add_card(card, Piles.DECK)

        if use_shelters:
            self._use_shelters()
        else:
            for _ in range(3):
                card = self.game.get_card_from_pile("Estate")
                self.add_card(card, Piles.DECK)

        for card in self.piles[Piles.DECK]:
            card.player = self

        self.piles[Piles.DECK].shuffle()

    ###########################################################################
    def _use_shelters(self) -> None:
        """Pick shelters out of the pile until we have one of each type"""
        shelters = ["Overgrown Estate", "Hovel", "Necropolis"]
        for shelter in shelters:
            card = self.game.get_card_from_pile("Shelters", shelter)
            self.add_card(card, Piles.DECK)

    ###########################################################################
    def _initial_tokens(self) -> None:
        self.tokens: dict[str, Optional[str]] = {
            "Trashing": None,
            "Estate": None,
            "+1 Card": None,
            "+1 Action": None,
            "+1 Buy": None,
            "+1 Coin": None,
            "-2 Cost": None,
            # '-1 Card': Handled by card_token
            # 'Journey': Handled by journey_token
            # '-1 Coin': Handled by coin_token
        }

    ###########################################################################
    def replace_traveller(self, src: Card, dst: str) -> None:
        """For traveller cards replace the src card with a copy of the
        dst card"""
        assert isinstance(src, Card)
        assert isinstance(dst, str)

        if src not in self.piles[Piles.PLAYED]:
            self.output(f"Not activating {src.name} traveller as not played")
            return

        choice = self.plr_choose_options(
            "Replace Traveller",
            (f"Keep {src.name}", "keep"),
            (f"Replace with a {dst}?", "replace"),
        )
        if choice == "keep":
            return
        if choice == "replace":
            self.replace_card(src, dst, destination=Piles.HAND)

    ###########################################################################
    def replace_card(self, src: Card, dst: str, **kwargs: Any) -> None:
        """Replace the {src} card with the {dst} card"""
        # New card goes into hand as it is about to be discarded
        destination = kwargs.get("destination", Piles.DISCARD)
        assert isinstance(src, Card), f"replace_card {src=} {type(src)=}"
        assert isinstance(dst, str), f"replace_card {dst=} {type(dst)=}"

        if newcard := self.gain_card(
            card_name=dst, destination=destination, callhook=False
        ):
            card_pile = self.game.card_piles[src.name]
            card_pile.add(src)
            self.piles[Piles.PLAYED].remove(src)

    ###########################################################################
    def flip_journey_token(self) -> bool:
        """Flip a journey token - and return its new state"""
        self.journey_token = not self.journey_token
        return self.journey_token

    ###########################################################################
    def receive_hex(self, hx: Optional[Hex] = None) -> None:
        """Receive a hex"""
        if hx is None:
            hx = self.game.receive_hex()
        if hx is None:
            self.output("No more hexes")
            return
        self.output(f"Received {hx} as a hex")
        self.output(hx.description(self))
        for _ in range(hx.cards):
            with contextlib.suppress(NoCardException):
                self.pickup_card()
        self.add_actions(hx.actions)
        self.buys += hx.buys
        self.coins += self.hook_spend_value(hx, actual=True)
        hx.special(game=self.game, player=self)
        self.game.discard_hex(hx)

    ###########################################################################
    def receive_boon(
        self, boon: Optional[Boon] = None, discard: bool = True
    ) -> Optional[Boon]:
        """Receive a boon"""
        if boon is None:
            boon = self.game.receive_boon()
        if boon is None:
            self.output("No more boons")
            return None
        self.output(f"Received {boon} as a boon")
        self.output(boon.description(self))
        for _ in range(boon.cards):
            with contextlib.suppress(NoCardException):
                self.pickup_card()
        self.add_actions(boon.actions)
        self.buys += boon.buys
        self.coins += self.hook_spend_value(boon, actual=True)
        boon.special(game=self.game, player=self)
        if discard:
            self.game.discard_boon(boon)
        return boon

    ###########################################################################
    def do_once(self, name: str) -> bool:
        """Allow a player to do something once per turn"""
        if name in self.once:
            return False
        self.once[name] = True
        return True

    ###########################################################################
    def place_token(self, token: str, pilename: str) -> None:
        """Place a token on the specified pile"""
        self.tokens[token] = pilename

    ###########################################################################
    def which_token(self, pilename: str) -> list[str]:
        """Return which token(s) are on a cardstack"""
        assert isinstance(pilename, str)
        onstack: list[str] = [
            token_name for token_name, token in self.tokens.items() if token == pilename
        ]
        return onstack

    ###########################################################################
    def call_reserve(self, card: str | Card) -> Optional[Card]:
        """Call a card from the reserve"""
        if isinstance(card, str):
            card = self.piles[Piles.RESERVE][card]
            if not card:
                return None
        assert isinstance(card, Card)
        self.output(f"Calling {card} from Reserve")
        self.currcards.append(card)
        card.hook_call_reserve(game=self.game, player=self)
        self.currcards.pop()
        self.piles[Piles.RESERVE].remove(card)
        self.add_card(card, Piles.PLAYED)
        return card

    ###########################################################################
    def reveal_card(self, card: Card) -> None:
        """Reveal a card to everyone"""
        if not card:
            return
        self.game.output(f"{self.name} reveals {card}")
        card.hook_reveal_this_card(game=self.game, player=self)

    ###########################################################################
    def trash_card(self, card: Card, **kwargs: Any) -> None:
        """Take a card out of the game"""
        assert isinstance(card, Card)
        self.stats["trashed"].append(card)
        trash_opts = {}
        if rc := card.hook_trash_this_card(game=self.game, player=self):
            trash_opts.update(rc)
        if trash_opts.get("trash", True):
            if card.location and card.location != Piles.TRASH:
                self.remove_card(card)
            self.game.trash_pile.add(card)
            card.player = None
            card.location = Piles.TRASH
        for crd in self.relevant_cards():
            if crd.name not in kwargs.get("exclude_hook", []):
                rc = crd.hook_trash_card(game=self.game, player=self, card=card)
                if rc:
                    trash_opts.update(rc)

    ###########################################################################
    def next_card(self) -> Card:
        """Pick up and return the next card from the deck"""
        if not self.piles[Piles.DECK]:
            self.refill_deck()
        if not self.piles[Piles.DECK]:
            self.output("No more cards in deck")
            raise NoCardException
        crd = self.piles[Piles.DECK].next_card()
        crd.location = None  # We don't know where it is going yet
        return crd

    ###########################################################################
    def top_card(self) -> Card:
        """Return the top card from the deck but don't pick it up"""
        if not self.piles[Piles.DECK]:
            self.refill_deck()
        if not self.piles[Piles.DECK]:
            self.output("No more cards in deck")
            raise NoCardException
        return self.piles[Piles.DECK].top_card()

    ###########################################################################
    def refill_deck(self) -> None:
        """Refill the player deck - shuffling if required"""
        self._shuffle_discard()
        while self.piles[Piles.DISCARD]:
            self.add_card(self.piles[Piles.DISCARD].next_card(), Piles.DECK)
        for card in self.relevant_cards():
            if hasattr(card, "hook_post_shuffle"):
                card.hook_post_shuffle(game=self.game, player=self)

    ###########################################################################
    def pickup_cards(
        self, num: int, verbose: bool = True, verb: str = "Picked up"
    ) -> list[Card]:
        """Pickup multiple cards into players hand"""
        cards: list[Card] = []
        for _ in range(num):
            try:
                if card := self.pickup_card(verbose=verbose, verb=verb):
                    cards.append(card)
            except NoCardException:
                break
        return cards

    ###########################################################################
    def pickup_card(
        self, card: Optional[Card] = None, verbose: bool = True, verb: str = "Picked up"
    ) -> Card:
        """Pick a card from the deck and put it into the players hand"""
        if card is None:
            card = self.next_card()
            if not card:
                self.output("No more cards to pickup")
                raise NoCardException
        assert isinstance(card, Card)
        self.add_card(card, Piles.HAND)
        if verbose:
            self.output(f"{verb} {card}")
        return card

    ###########################################################################
    def _shuffle_discard(self) -> None:
        num_cards = len(self.piles[Piles.DISCARD])
        self.output(f"Shuffling Pile of {num_cards} cards")
        for card in self.projects:
            if hasattr(card, "hook_pre_shuffle"):
                card.hook_pre_shuffle(game=self.game, player=self)
        self.piles[Piles.DISCARD].shuffle()

    ###########################################################################
    def pick_up_hand(self, hand_size: Optional[int] = None) -> None:
        """Replenish hand from deck"""
        if hand_size is None:
            hand_size = self.newhandsize
        if self.card_token:
            self.output("-Card token reduce draw by one")
            hand_size -= 1
            self.card_token = False
        while self.piles[Piles.HAND].size() < hand_size:
            try:
                self.pickup_card(verb="Dealt")
            except NoCardException:
                self.output("Not enough cards to fill hand")
                break

    ###########################################################################
    def remove_card(self, card: Card) -> None:
        """Remove a card from wherever it is"""
        if card.location in self.piles:
            self.piles[card.location].remove(card)
        elif card.location == Piles.CARDPILE:
            pass
        elif card.location == Piles.TRASH:
            self.game.trash_pile.remove(card)
        else:
            raise AssertionError(
                f"Trying to remove_card {card} from unknown location: {card.location}"
            )

    ###########################################################################
    def move_card(self, card: Card, dest: Piles) -> Card:
        """Move a card to {dest} card pile"""
        self.remove_card(card)
        return self.add_card(card, dest)

    ###########################################################################
    def add_card(self, card: Card, pile: Piles | str = Piles.DISCARD) -> Card:
        """Add an existing card to a new location"""
        assert isinstance(card, Card), f"{card=} {type(card)=}"
        card.player = self

        # There can be custom PlayAreas (such as part of  card)
        if isinstance(pile, PlayArea):
            card.location = pile
            pile.add(card)
            return card

        # Return card to a card pile
        if pile == Piles.CARDPILE or isinstance(pile, CardPile):
            self.game.card_piles[card.pile].add(card)
            return card

        if pile in self.piles:
            self.piles[pile].add(card)
            card.location = pile
        elif pile == "topdeck":
            card.location = Piles.DECK
            self.piles[Piles.DECK].addToTop(card)
        else:
            raise AssertionError(f"Adding card to unknown location: {pile}")
        return card

    ###########################################################################
    def discard_card(
        self, card: Card, source: Optional[Piles] = None, hook: bool = True
    ) -> None:
        """Discard a card"""
        assert isinstance(card, Card)
        if card in self.piles[Piles.HAND]:
            self.piles[Piles.HAND].remove(card)
        self.add_card(card, Piles.DISCARD)
        if hook:
            self.hook_discard_this_card(card, source)
            for way, crd in self.played_ways:
                if crd != card:
                    continue
                way.hook_way_discard_this_card(game=self.game, player=self, card=crd)

    ###########################################################################
    def discard_hand(self) -> None:
        # Activate hooks first, so they can still access contents of the
        # players hand etc. before they get discarded
        for card in self.piles[Piles.HAND]:
            self.hook_discard_this_card(card, Piles.HAND)
        for card in self.piles[Piles.PLAYED]:
            self.hook_discard_this_card(card, Piles.PLAYED)
        for way, card in self.played_ways:
            way.hook_way_discard_this_card(game=self.game, player=self, card=card)
        while self.piles[Piles.HAND]:
            card = self.piles[Piles.HAND].next_card()
            self.discard_card(card, Piles.HAND, hook=False)
        while self.piles[Piles.PLAYED]:
            card = self.piles[Piles.PLAYED].next_card()
            self.discard_card(card, Piles.PLAYED, hook=False)

    ###########################################################################
    def _playable_selection(self, index: int) -> tuple[list[Option], int]:
        options = []
        playable = [c for c in self.piles[Piles.HAND] if c.playable and c.isAction()]
        if self.villagers:
            o = Option(
                selector="1",
                verb="Spend Villager (1 action)",
                card=None,
                action="villager",
            )
            options.append(o)

        for p in playable:
            sel = chr(ord("a") + index)
            details = p.get_cardtype_repr()
            o = Option(
                verb="Play",
                selector=sel,
                name=p.name,
                desc=p.description(self).strip(),
                action="play",
                card=p,
                details=details,
            )
            notes = ""
            for tkn in self.which_token(p.name):
                notes += f"[Tkn: {tkn}]"
            o["notes"] = notes
            options.append(o)
            index += 1
            for way in self.game.ways.values():
                sel = chr(ord("a") + index)
                o = Option(
                    verb="Play",
                    selector=sel,
                    name=way.name,
                    desc=f"{p.name}: {way.description(self)}",
                    action="way",
                    card=p,
                    way=way,
                )
                options.append(o)
                index += 1
        return options, index

    ###########################################################################
    def _night_selection(self, index: int) -> tuple[list[Option], int]:
        options = []
        nights = [c for c in self.piles[Piles.HAND] if c.isNight()]
        if nights:
            for n in nights:
                sel = chr(ord("a") + index)
                details = n.get_cardtype_repr()
                o = Option(
                    verb="Play",
                    selector=sel,
                    name=n.name,
                    details=details,
                    card=n,
                    action="play",
                    desc=n.description(self),
                )
                options.append(o)
                index += 1
        return options, index

    ###########################################################################
    def _spendable_selection(self) -> list[Option]:
        options = []
        spendable = [_ for _ in self.piles[Piles.HAND] if _.isTreasure()]
        spendable.sort(key=lambda x: x.name)
        total_coin = sum(self.hook_spend_value(_) for _ in spendable)
        numpots = sum(1 for _ in spendable if _.name == "Potion")
        potstr = f", {numpots} potions" if numpots else ""
        details = f"{total_coin} coin{potstr}"
        if spendable:
            o = Option(
                selector="1",
                verb="Spend all treasures",
                details=details,
                card=None,
                action="spendall",
            )
            options.append(o)

        if self.coffers:
            o = Option(
                selector="2", verb="Spend Coffer (1 coin)", card=None, action="coffer"
            )
            options.append(o)

        if self.debt and self.coins:
            o = Option(selector="3", verb="Payback Debt", card=None, action="payback")
            options.append(o)

        index = 4
        for card in spendable:
            tp = f"{self.hook_spend_value(card)} coin; {card.get_cardtype_repr()}"
            o = Option(
                selector=str(index),
                name=card.name,
                details=tp,
                verb="Spend",
                card=card,
                action="spend",
                desc=card.description(self),
            )
            options.append(o)
            index += 1

        return options

    ###########################################################################
    def _get_whens(self) -> list[str]:
        """Return when we are for calling reserve cards"""
        whens: list[str] = ["any"]
        for c in self.piles[Piles.PLAYED]:
            if c.isAction():
                whens.append("postaction")
        if self.misc["is_start"]:
            whens.append("start")
        return whens

    ###########################################################################
    def _reserve_selection(self, index: int) -> tuple[Optional[list[Option]], int]:
        whens = self._get_whens()
        options = []
        for card in self.piles[Piles.RESERVE]:
            if not card.callable:
                continue
            if card.when not in whens:
                continue
            index += 1
            sel = chr(ord("a") + index)
            details = card.get_cardtype_repr()
            o = Option(
                selector=sel,
                name=card.name,
                verb="Call",
                details=details,
                card=card,
                action="reserve",
                desc=card.description(self),
            )
            options.append(o)

        return options, index

    ###########################################################################
    def _project_selection(self, index: int) -> tuple[Optional[list[Option]], int]:
        """Allow player to select projects"""
        if not self.game.projects:
            return None, index
        # Can only have two projects
        if len(self.projects) == 2:
            return None, index
        options = []
        for op in self.game.projects.values():
            index += 1
            if (op.cost <= self.coins.get() and self.buys) and (
                op not in self.projects
            ):
                sel = chr(ord("a") + index)
                action = "project"
            else:
                sel = "-"
                action = None
            details = f"Project; {self._cost_string(op)}"
            o = Option(
                selector=sel,
                verb="Buy",
                desc=op.description(self),
                name=op.name,
                details=details,
                card=op,
                action=action,
            )
            options.append(o)

        return options, index

    ###########################################################################
    def _event_selection(self, index: int) -> tuple[list[Option], int]:
        """Generate player options for selecting events"""
        options = []
        for op in self.game.events.values():
            index += 1
            if op.cost <= self.coins.get() and self.buys:
                sel = chr(ord("a") + index)
                action = "event"
            else:
                sel = "-"
                action = None
            details = f"Event; {self._cost_string(op)}"
            o = Option(
                selector=sel,
                verb="Use",
                desc=op.description(self),
                name=op.name,
                details=details,
                card=op,
                action=action,
            )
            options.append(o)

        return options, index

    ###########################################################################
    def _card_check(self) -> None:
        for pile in self.piles:
            for card in self.piles[pile]:
                assert (
                    card.location == pile
                ), f"{self.name} {card=} {pile=} {card.location=}"

    ###########################################################################
    def _get_all_purchasable(self) -> PlayArea:
        """Return all potentially purchasable cards"""
        all_cards = PlayArea("all_purchasable")
        for name, pile in self.game.get_card_piles():
            if pile.is_empty():
                continue
            card = pile.get_top_card()
            if card is None:
                continue
            if not card.purchasable:
                continue
            all_cards.add(card)
        all_cards.sort(key=self.card_cost)
        all_cards.sort(key=lambda x: x.basecard)
        return all_cards

    ###########################################################################
    def _buyable_selection(self, index: int) -> tuple[list[Option], int]:
        options = []
        all_cards = self._get_all_purchasable()
        buyable = self.cards_under(
            coin=self.coins.get(), num_potions=self.potions.get()
        )
        for card in all_cards:
            if not self.hook_allowed_to_buy(card):
                if card in buyable:
                    buyable.remove(card)
            sel = chr(ord("a") + index)
            if (
                not self.debt
                and self.buys
                and card in buyable
                and card not in self.forbidden_to_buy
            ):
                action = "buy"
                verb = "Buy"
            else:
                sel = "-"
                verb = ""
                action = None
            details = [self._cost_string(card)]
            if self.game.card_piles[card.pile].embargo_level:
                details.append(
                    f"Embargo {self.game.card_piles[card.pile].embargo_level}"
                )
            if self.game.card_piles[card.pile].getVP():
                details.append(f"Gathered {self.game.card_piles[card.name].getVP()} VP")
            details.append(card.get_cardtype_repr())
            details.append(f"{len(self.game.card_piles[card.pile])} left")
            for tkn in self.which_token(card.name):
                details.append(f"[Tkn: {tkn}]")
            o = Option(
                selector=sel,
                verb=verb,
                desc=card.description(self),
                name=card.name,
                details="; ".join(details),
                card=card,
                action=action,
            )
            options.append(o)
            index += 1
        return options, index

    ###########################################################################
    def _choice_selection(self) -> list[Option]:
        index = 0
        o = Option(selector="0", verb="End Phase", card=None, action="quit")
        options: list[Option] = [o]

        if self.phase == Phase.ACTION:
            if self.actions or self.villagers:
                op, index = self._playable_selection(index)
                options.extend(op)

        if self.phase == Phase.BUY:
            op = self._spendable_selection()
            options.extend(op)
            op, index = self._buyable_selection(index)
            options.extend(op)
            op, index = self._event_selection(index)
            options.extend(op)
            op, index = self._project_selection(index)
            if op:
                options.extend(op)

        if self.phase == Phase.NIGHT:
            op, index = self._night_selection(index)
            options.extend(op)

        if self.piles[Piles.RESERVE].size():
            op, index = self._reserve_selection(index)
            options.extend(op)

        return options

    ###########################################################################
    def _generate_prompt(self) -> str:
        """Return the prompt to give to the user"""
        status = f"Actions={self.actions.get()} Buys={self.buys.get()}"
        if self.coins:
            status += f" Coins={self.coins.get()}"
        if self.debt:
            status += f" Debt={self.debt.get()}"
        if self.potions:
            status += " Potion"
        if self.favors:
            status += f" Favours={self.favors.get()}"
        if self.coffers:
            status += f" Coffer={self.coffers.get()}"
        if self.villagers:
            status += f" Villager={self.villagers.get()}"
        if self.limits[Limits.PLAY] is not None:
            status += f" Play Limit={self.limits[Limits.PLAY]}"
        prompt = f"What to do ({status})?"
        return prompt

    ###########################################################################
    def turn(self) -> None:
        """Have a turn as the player"""
        self.turn_number += 1
        self.output(f"\n{'#' * 30} Turn {self.turn_number} {'#' * 30}")
        stats = f"({self.get_score()} points, {self.count_cards()} cards)"
        if self.skip_turn:
            self.skip_turn = False
            return
        self.output(f"{self.name}'s Turn {stats}")
        self.phase = Phase.ACTION
        # This bizarre loop is so cards can change player phases
        while True:
            self._card_check()  # DEBUG
            match self.phase:
                case Phase.ACTION:
                    self.action_phase()
                    if self.phase == Phase.ACTION:
                        self.phase = Phase.BUY
                case Phase.BUY:
                    self.buy_phase()
                    if self.phase == Phase.BUY:
                        self.phase = Phase.NIGHT
                case Phase.NIGHT:
                    self.night_phase()
                    if self.phase == Phase.NIGHT:
                        self.phase = Phase.CLEANUP
                case Phase.CLEANUP:
                    self.cleanup_phase()
                    break
        self._card_check()  # DEBUG

    ###########################################################################
    def night_phase(self) -> None:
        """Do the Night Phase"""
        nights = [_ for _ in self.piles[Piles.HAND] if _.isNight()]
        if not nights:
            return
        self.output("************ Night Phase ************")
        while True:
            self._display_overview()
            options = self._choice_selection()
            prompt = self._generate_prompt()

            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                return

    ###########################################################################
    def action_phase(self) -> None:
        self.output("************ Action Phase ************")
        while True:
            self._display_overview()
            options = self._choice_selection()
            prompt = self._generate_prompt()

            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                return

    ###########################################################################
    def buy_phase(self) -> None:
        self.output("************ Buy Phase ************")
        self.hook_pre_buy()
        while True:
            self._display_overview()
            options = self._choice_selection()
            prompt = self._generate_prompt()

            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                break
        self.hook_end_buy_phase()

    ###########################################################################
    def hook_end_buy_phase(self) -> None:
        for card in self.piles[Piles.PLAYED] + self.projects:
            card.hook_end_buy_phase(game=self.game, player=self)

    ###########################################################################
    def cleanup_phase(self) -> None:
        # Save the cards we had so that the hook_end_turn has something to apply against
        self.had_cards = (
            self.piles[Piles.PLAYED]
            + self.piles[Piles.RESERVE]
            + self.played_events
            + self.game.landmarks
            + self.piles[Piles.DURATION]
        )
        self.game.cleanup_boons()
        for card in (
            self.piles[Piles.PLAYED] + self.piles[Piles.RESERVE] + self.artifacts
        ):
            card.hook_cleanup(self.game, self)
        self.discard_hand()
        self.pick_up_hand()
        self.hooks = {}
        self.misc["cleaned"] = True

    ###########################################################################
    def payback(self) -> None:
        payback = min(self.coins.get(), self.debt.get())
        self.output(f"Paying back {payback} debt")
        self.coins -= payback
        self.debt -= payback

    ###########################################################################
    def _perform_action(self, opt) -> None:
        if opt["action"] == "buy":
            self.buy_card(opt["name"])
        elif opt["action"] == "event":
            self.perform_event(opt["card"])
        elif opt["action"] == "project":
            self.buy_project(opt["card"])
        elif opt["action"] == "reserve":
            self.call_reserve(opt["card"])
        elif opt["action"] == "coffer":
            self.spend_coffer()
        elif opt["action"] == "villager":
            self.spend_villager()
        elif opt["action"] == "play":
            self.play_card(opt["card"])
        elif opt["action"] == "spend":
            self.play_card(opt["card"])
        elif opt["action"] == "payback":
            self.payback()
        elif opt["action"] == "spendall":
            self._spend_all_cards()
        elif opt["action"] == "quit":
            return
        elif opt["action"] == "way":
            self.perform_way(opt["way"], opt["card"])
        elif opt["action"] is None:
            return
        else:  # pragma: no cover
            print(f"ERROR: Unhandled action {opt['action']}", file=sys.stderr)
            sys.exit(1)
        self.misc["is_start"] = False

    ###########################################################################
    def _display_tokens(self) -> str:
        """Generate the overview display for tokens"""
        token_output = []
        for tkn, tkv in self.tokens.items():
            if tkv:
                token_output.append(f"{tkn}: {tkv}")
        if self.card_token:
            token_output.append("-1 Card")
        if self.coin_token:
            token_output.append("-1 Coin")
        if self.journey_token:
            token_output.append("Journey Faceup")
        else:
            token_output.append("Journey Facedown")
        return "; ".join(token_output)

    ###########################################################################
    def _display_overview(self) -> None:
        """Display turn summary overview to player"""
        self.output("")
        self.output("-" * 50)
        self.output(f"| Phase: {self.phase.name.title()}")
        for landmark in self.game.landmarks.values():
            self.output(f"| Landmark {landmark.name}: {landmark.description(self)}")
        self.output(f"| Tokens: {self._display_tokens()}")
        if self.states:
            self.output(f"| States: {', '.join([_.name for _ in self.states])}")
        if self.piles[Piles.DEFER]:
            self.output(
                f"| Defer: {', '.join([str(_) for _ in self.piles[Piles.DEFER]])}"
            )
        if self.piles[Piles.DURATION]:
            self.output(
                f"| Duration: {', '.join([str(_) for _ in self.piles[Piles.DURATION]])}"
            )
        if self.projects:
            self.output(f"| Project: {', '.join([p.name for p in self.projects])}")
        if self.piles[Piles.RESERVE]:
            self.output(
                f"| Reserve: {', '.join([str(_) for _ in self.piles[Piles.RESERVE]])}"
            )
        if self.piles[Piles.HAND]:
            self.output(
                f"| Hand ({len(self.piles[Piles.HAND])}): {', '.join([str(_) for _ in self.piles[Piles.HAND]])}"
            )
        else:
            self.output("| Hand: <EMPTY>")
        if self.artifacts:
            self.output(f"| Artifacts: {', '.join([_.name for _ in self.artifacts])}")
        for trait_name, trait in self.game.traits.items():
            self.output(f"| Trait {trait_name} on {trait.card_pile}: {trait.desc}")
        if self.piles[Piles.EXILE]:
            self.output(
                f"| Exile: {', '.join([str(_) for _ in self.piles[Piles.EXILE]])}"
            )
        if self.piles[Piles.PLAYED]:
            self.output(
                f"| Played ({len(self.piles[Piles.PLAYED])}): {', '.join([str(_) for _ in self.piles[Piles.PLAYED]])}"
            )
        else:
            self.output("| Played: <NONE>")
        self.output(f"| Deck Size: {len(self.piles[Piles.DECK])}")
        if self.game.ally:
            self.output(
                f"| Ally: {self.game.ally.name}: {self.game.ally.description(self)}"
            )
        self.output(
            f"| Discard ({len(self.piles[Piles.DISCARD])}): {', '.join([str(_) for _ in self.piles[Piles.DISCARD]])}"
        )  # Debug
        self.output(
            f"| Trash ({len(self.game.trash_pile)}): {', '.join([str(_) for _ in self.game.trash_pile])}"
        )  # Debug
        self.output(f"| {self.piles[Piles.DISCARD].size()} cards in discard pile")
        self.output("-" * 50)

    ###########################################################################
    def add_score(self, reason: str, points: int = 1) -> None:
        """Add score to the player"""
        if reason not in self.score:
            self.score[reason] = 0
        self.score[reason] += points

    ###########################################################################
    def all_cards(self) -> PlayArea:
        """Return all the cards that the player has"""
        x = PlayArea("all")
        x += self.piles[Piles.DISCARD]
        x += self.piles[Piles.HAND]
        x += self.piles[Piles.DECK]
        x += self.piles[Piles.PLAYED]
        x += self.piles[Piles.DURATION]
        x += self.piles[Piles.DEFER]
        x += self.piles[Piles.RESERVE]
        x += self.piles[Piles.EXILE]
        return x

    ###########################################################################
    def get_score_details(self) -> dict[str, int]:
        """Calculate score of the player from all factors"""
        score: dict[str, int] = {}
        for card in self.all_cards():
            score[card.name] = (
                score.get(card.name, 0)
                + card.victory
                + card.special_score(self.game, self)
            )
        for state in self.states:
            score[state.name] = score.get(state.name, 0) + state.victory
        if self.game.ally:
            score[self.game.ally.name] = self.game.ally.special_score(self.game, self)
        score.update(self.score)
        return score

    ###########################################################################
    def get_score(self, verbose: bool = False) -> int:
        """Return the scores - print them if {verbose} is True"""
        scr = self.get_score_details()
        vp = sum(scr.values())
        if verbose:
            self.game.output(
                f"{self.name} (Turn {self.turn_number}): {json.dumps(scr, indent=2)}"
            )
        return vp

    ###########################################################################
    def hook_pre_buy(self) -> None:
        """Hook that fires off before the buy phase"""
        for card in self.relevant_cards():
            card.hook_pre_buy(game=self.game, player=self)

    ###########################################################################
    def hook_allowed_to_buy(self, card: Card) -> bool:
        """Hook to check if you are allowed to buy a card"""
        return card.hook_allowed_to_buy(game=self.game, player=self)

    ###########################################################################
    def hook_buy_card(self, card: Card) -> None:
        """Hook for after purchasing a card"""
        for c in self.relevant_cards():
            c.hook_buy_card(game=self.game, player=self, card=card)

    ###########################################################################
    def start_turn(self) -> None:
        self.phase = Phase.START
        self.buys.set(1)
        self.actions.set(1)
        self.coins.set(0)
        self.potions.set(0)
        self.played_ways = []
        self.misc = {"is_start": True, "cleaned": False}
        self.stats = {"gained": [], "bought": [], "trashed": []}
        self._display_overview()
        self._hook_start_turn()
        self._duration_start_turn()
        self._defer_start_turn()

    ###########################################################################
    def _defer_start_turn(self) -> None:
        """Perform the defer-pile cards at the start of the turn"""
        for card in self.piles[Piles.DEFER]:
            self.output(f"Playing deferred {card}")
            self.currcards.append(card)
            self.move_card(card, Piles.HAND)
            self.play_card(card, cost_action=False)
            self.currcards.pop()

    ###########################################################################
    def _duration_start_turn(self) -> None:
        """Perform the duration pile at the start of the turn"""
        for card in self.piles[Piles.DURATION]:
            options: dict[str, Any] = {"dest": Piles.PLAYED}
            if not card.permanent:
                self.output(f"Playing {card} from duration pile")
            self.currcards.append(card)
            upd_opts = card.duration(game=self.game, player=self)
            if isinstance(upd_opts, dict):
                options.update(upd_opts)
            self.currcards.pop()
            if not card.permanent:
                # Handle case where cards move themselves elsewhere
                if card.location != Piles.DURATION:
                    continue
                self.move_card(card, options["dest"])
        for event in self.game.events.values():
            event.duration(game=self.game, player=self)

    ###########################################################################
    def _hook_start_turn(self) -> None:
        """Start of turn hooks"""
        for card_name in self.game.card_instances:
            self.game.card_instances[card_name].hook_start_every_turn(self.game, self)
        for card in self.relevant_cards():
            card.hook_start_turn(self.game, self)

    ###########################################################################
    def spend_coffer(self) -> None:
        """Spend a coffer to gain a coin"""
        if self.coffers.get() <= 0:
            return
        self.coffers -= 1
        self.coins += 1
        self.output("Spent a coffer")

    ###########################################################################
    def spend_villager(self) -> None:
        """Spend a villager to gain an action"""
        if self.villagers.get() <= 0:
            return
        self.villagers -= 1
        self.add_actions(1)
        self.output("Spent a villager")

    ###########################################################################
    def exile_card(self, card: str | Card) -> None:
        """Send a card to the exile pile; if the card is a name then take it
        from supply"""
        if isinstance(card, str):
            card = self.game.get_card_from_pile(card)
            if card is None:
                self.output(f"No more {card} in supply")
                return
        self.move_card(card, Piles.EXILE)

    ###########################################################################
    def end_turn(self) -> None:
        """End of turn"""
        if not self.misc["cleaned"]:
            self.cleanup_phase()
        self.limits[Limits.PLAY] = None
        self.limits[Limits.BUY] = 999
        for card in self.had_cards:
            self.currcards.append(card)
            card.hook_end_turn(game=self.game, player=self)
            self.currcards.pop()
        self.newhandsize = 5
        self.played_events = PlayArea("played_events")
        self.messages = []
        self.forbidden_to_buy = []
        self.once = {}
        self.phase = Phase.NONE
        self.had_cards = []

    ###########################################################################
    def hook_discard_this_card(self, card: Card, source=None) -> None:
        """A card has been discarded"""
        self.currcards.append(card)
        card.hook_discard_this_card(game=self.game, player=self, source=source)
        self.currcards.pop()

    ###########################################################################
    def hook_spend_value(self, card: Card, actual: bool = False) -> int:
        """How much do you get for spending the card
        If actual is True then we are spending the coin rather than
        just working out what we would get for spending it
        """
        val = card.hook_coinvalue(game=self.game, player=self)
        for c in self.piles[Piles.PLAYED]:
            val += c.hook_spend_value(game=self.game, player=self, card=card)
        for s in self.states:
            val += s.hook_spend_value(game=self.game, player=self, card=card)
        if val and self.coin_token:
            val -= 1
            if actual:
                self.coin_token = False
        return val

    ###########################################################################
    def _spend_all_cards(self) -> None:
        """Spend all treasure cards in hand"""
        for card in self.piles[Piles.HAND]:
            # Contents of hand can change as they are played
            if card.isTreasure() and card in self.piles[Piles.HAND]:
                self.play_card(card, cost_action=False)

    ###########################################################################
    def _play_card_tokens(self, card: Card) -> None:
        tkns = self.which_token(card.name)
        if "+1 Action" in tkns:
            self.output("Gaining action from +1 Action token")
            self.add_actions(1)
        if "+1 Card" in tkns:
            try:
                if c := self.pickup_card():
                    self.output(f"Picked up {c} from +1 Card token")
            except NoCardException:
                pass
        if "+1 Coin" in tkns:
            self.output("Gaining coin from +1 Coin token")
            self.coins += 1
        if "+1 Buy" in tkns:
            self.output("Gaining buy from +1 Buy token")
            self.buys += 1

    ###########################################################################
    def _hook_pre_play(self, card: Card) -> dict[str, str]:
        """Hook before an action card is played"""
        options: dict[str, str] = {}
        for crd in self.piles[Piles.DURATION] + self.piles[Piles.PLAYED]:
            if ans := crd.hook_pre_play(game=self.game, player=self, card=card):
                options |= ans
        return options

    ###########################################################################
    def hook_all_players_pre_play(self, card: Card) -> dict[str, str]:
        options: dict[str, str] = {}
        for player in self.game.player_list():
            for crd in player.piles[Piles.DURATION]:
                if ans := crd.hook_all_players_pre_play(
                    game=self.game, player=self, owner=player, card=card
                ):
                    options |= ans
        return options

    ###########################################################################
    def hook_all_players_post_play(self, card: Card) -> dict[str, Any]:
        options: dict[str, str] = {}
        for player in self.game.player_list():
            for crd in player.piles[Piles.DURATION]:
                if answer := crd.hook_all_players_post_play(
                    game=self.game, player=self, owner=player, card=card
                ):
                    options |= answer
        return options

    ###########################################################################
    def defer_card(self, card: Card) -> None:
        """Set a non-duration card to be played in its entirety next turn"""
        self.move_card(card, Piles.DEFER)

    ###########################################################################
    def move_after_play(self, card: Card, force: bool = False) -> None:
        """Move the card to its next location after it has been played"""
        if not force and card.isDuration():
            self.move_card(card, Piles.DURATION)
        elif not force and card.isReserve():
            self.move_card(card, Piles.RESERVE)
        else:
            self.move_card(card, Piles.PLAYED)

    ###########################################################################
    def _play_limit(self) -> bool:
        """Did we hit limits on number of cards we can play - False if we can't play"""
        if self.limits[Limits.PLAY] is not None:
            if self.limits[Limits.PLAY] <= 0:
                return False
            self.limits[Limits.PLAY] -= 1
        return True

    ###########################################################################
    def _play_enough_actions(self, card: Card, cost_action: bool) -> bool:
        """Do we have enough actions to play this card"""
        if not card.isTreasure() and self.phase != Phase.BUY:
            if card.isAction() and cost_action and self.phase != Phase.NIGHT:
                self.actions -= 1
            if self.actions.get() < 0:  # pragma: no cover
                self.actions.set(0)
                return False
        return True

    ###########################################################################
    def play_card(
        self,
        card: Card,
        discard: bool = True,
        cost_action: bool = True,
        post_action_hook: bool = True,
    ) -> None:
        """Play the card {card}"""
        options: dict[str, Any] = {"skip_card": False, "discard": discard}
        if card not in self.piles[Piles.HAND] and options["discard"]:
            raise AssertionError(f"Playing {card} which is not in hand")
        if not self._play_limit():
            self.output(f"Can't play {card} due to limits in number of plays")
            return
        self.output(f"Playing {card}")
        self.currcards.append(card)
        options |= self._hook_pre_play(card)
        options |= self.hook_all_players_pre_play(card)

        self._play_card_tokens(card)

        if not self._play_enough_actions(card, cost_action):
            self.currcards.pop()
            self.output("Not enough actions")
            return

        if options["discard"]:
            self.move_after_play(card, options["skip_card"])

        if not options["skip_card"]:
            self.card_benefits(card)
        self.currcards.pop()
        if post_action_hook:
            self._post_play_hooks(card)

    ###########################################################################
    def _post_play_hooks(self, card: Card) -> None:
        """Do all the post play hooks"""
        self.hook_all_players_post_play(card)
        for other_card in self.relevant_cards():
            other_card.hook_post_play(game=self.game, player=self, card=card)

    ###########################################################################
    def perform_way(self, way: Way, card: Card) -> None:
        """Perform a way"""
        opts = {"discard": True}
        self.currcards.append(way)
        self.actions -= 1
        if self.actions.get() < 0:
            self.actions.set(0)
            self.currcards.pop()
            self.output("Not enough actions")
            return
        self.output(f"Playing {way.name} instead of {card}")
        self.card_benefits(way)
        new_opts = way.special_way(game=self.game, player=self, card=card)
        if isinstance(new_opts, dict):
            opts |= new_opts
        if opts["discard"]:
            self.move_card(card, Piles.PLAYED)
        self.played_ways.append((way, card))
        self.currcards.pop()

    ###########################################################################
    def card_benefits(self, card: Card) -> None:
        """Gain the benefits of the card being played - including special()"""
        self.add_actions(card.actions)
        self.coins += self.hook_spend_value(card, actual=True)
        self.buys += card.buys
        self.favors += card.favors
        self.potions += card.potion

        modifier = 0
        if self.card_token and card.cards:
            self.output("-1 Card token reduces cards drawn")
            self.card_token = False
            modifier = -1

        for _ in range(card.cards + modifier):
            with contextlib.suppress(NoCardException):
                self.pickup_card()

        if self.phase == Phase.NIGHT:
            card.night(game=self.game, player=self)
        else:
            card.special(game=self.game, player=self)

    ###########################################################################
    def card_cost(self, card: Card) -> int:
        assert isinstance(card, (Card, Project, Event)), f"Card{card=} {type(card)=}"
        cost = card.cost
        if "-Cost" in self.which_token(card.name):
            cost -= 2
        for crd in self.relevant_cards():
            cost += crd.hook_card_cost(game=self.game, player=self, card=card)
        cost += card.hook_this_card_cost(game=self.game, player=self)
        return max(0, cost)

    ###########################################################################
    def gain_card(
        self,
        card_name: Optional[str] = None,
        destination: Piles = Piles.DISCARD,
        new_card: Optional[Card] = None,
        callhook: bool = True,
    ) -> Optional[Card]:
        """Add a new card to the players set of cards from a card pile, return the card gained"""
        # Options:
        #   dontadd: True - adding card handled elsewhere
        #   replace: <new_card> - Replace the gained card with <new_card>
        #   destination: <dest> - Move the new card to <dest> rather than discard pile
        #   trash: True - trash the new card
        #   shuffle: True - shuffle the deck after gaining new card
        options: dict[str, Any] = {}
        if new_card is None:
            assert card_name is not None
            if card_name == "Loot":
                pile = "Loot"
            else:
                pile = self.game.card_instances[card_name].pile
            if not pile:
                pile = card_name
            new_card = self.game.get_card_from_pile(pile)

        if new_card is None:
            self.output(f"No more {card_name}")
            return None
        self.output(f"Gained a {new_card}")
        if callhook:
            if rc := self._hook_gain_card(new_card):
                options |= rc
            if rc := new_card.hook_gain_this_card(game=self.game, player=self):
                options |= rc

        # check for un-exiling
        if new_card.name in self.piles[Piles.EXILE]:
            self.check_unexile(new_card.name)

        # Replace is to gain a different card
        if options.get("replace"):
            self.game.card_piles[new_card.name].add(new_card)
            new_card = self.game.get_card_from_pile(options["replace"])
            if not new_card:
                self.output(f"No more {options['replace']}")
            else:
                new_card.player = self
        if new_card is None:
            return None
        self.stats["gained"].append(new_card)
        destination = options.get("destination", destination)
        if callhook:
            options |= self.hook_all_players_gain_card(new_card)
        if options.get("trash", False):
            self.trash_card(new_card)
            return new_card
        if not options.get("dontadd", False):
            self.add_card(new_card, destination)
        if options.get("shuffle", False):
            self.piles[Piles.DECK].shuffle()
        return new_card

    ###########################################################################
    def check_unexile(self, card_name: str) -> None:
        """Give players option to un-exile card"""
        num = sum(1 for _ in self.piles[Piles.EXILE] if _.name == card_name)
        choices = [
            (f"Unexile {num} x {card_name}", True),
            ("Do nothing", False),
        ]
        if self.plr_choose_options(f"Un-exile {card_name}", *choices):
            self.unexile(card_name)

    ###########################################################################
    def unexile(self, cardname: str) -> int:
        """Un-exile cards
        Return number un-exiled"""
        count = 0
        if not self.piles[Piles.EXILE]:
            return 0
        for card in self.piles[Piles.EXILE]:
            if card is None:
                break
            if card.name == cardname:
                self.move_card(card, Piles.DISCARD)
                count += 1
        return count

    ###########################################################################
    def overpay(self, card: Card) -> None:
        """http://wiki.dominionstrategy.com/index.php/Overpay"""
        options = [(f"Spend {i} more", i) for i in range(self.coins.get() + 1)]
        ans = self.plr_choose_options("How much do you wish to overpay?", *options)
        if ans > 0:
            card.hook_overpay(game=self.game, player=self, amount=ans)
            self.coins -= ans

    ###########################################################################
    def buy_card(self, card_name: str) -> None:
        """Buy a card"""
        assert isinstance(card_name, str), f"buy_card({card_name=}) {type(card_name)=}"
        if not self.buys:  # pragma: no cover
            return
        if not self.limits[Limits.BUY]:
            self.output("Buy limit stops buying")
            return
        if self.debt:
            self.output("Must pay off debt first")
            return
        self.buys -= 1
        self.limits[Limits.BUY] -= 1
        card = self.game.card_instances[card_name]
        cost = self.card_cost(card)
        if card.isDebt():
            self.debt += card.debtcost
        if self.coins.get() < cost:
            self.output("You can't afford this")
            return
        self.coins -= cost
        if card.overpay and self.coins.get():
            self.overpay(card)
        new_card = self.gain_card(card.name)
        if not new_card:
            self.output("Couldn't buy card")
            return
        if self.game.card_piles[new_card.pile].embargo_level:
            for _ in range(self.game.card_piles[new_card.pile].embargo_level):
                self.gain_card("Curse")
                self.output("Gained a Curse from embargo")
        self.stats["bought"].append(new_card)
        self.output(f"Bought {new_card} for {cost} coin")
        if "Trashing" in self.which_token(new_card.name):
            self.output("Trashing token allows you to trash a card")
            self.plr_trash_card()
        self.hook_buy_card(new_card)
        new_card.hook_buy_this_card(game=self.game, player=self)
        self.hook_all_players_buy_card(new_card)

    ###########################################################################
    def hook_all_players_buy_card(self, card) -> None:
        for player in self.game.player_list():
            for crd in player.piles[Piles.DURATION]:
                crd.hook_all_players_buy_card(
                    game=self.game, player=self, owner=player, card=card
                )
        for crd in self.game.landmarks.values():
            crd.hook_all_players_buy_card(
                game=self.game, player=self, owner=self, card=card
            )

    ###########################################################################
    def hook_all_players_gain_card(self, card) -> dict[str, str]:
        options: dict[str, str] = {}
        for player in self.game.player_list():
            for crd in player.relevant_cards():
                if opts := crd.hook_all_players_gain_card(
                    game=self.game, player=self, owner=player, card=card
                ):
                    options |= opts
        return options

    ###########################################################################
    def add_hook(self, hook_name: str, hook) -> None:
        self.hooks[hook_name] = hook

    ###########################################################################
    def relevant_cards(self) -> list[Card]:
        """Return a list of all cards whose hooks we should look at"""
        return (
            self.piles[Piles.HAND]
            + self.piles[Piles.PLAYED]
            + self.piles[Piles.DURATION]
            + self.piles[Piles.RESERVE]
            + self.game.landmarks
            + self.projects
            + self.game.ways
            + self.played_events
            + self.states
            + self.artifacts
            + self.game.ally
            + self.game.traits
        )

    ###########################################################################
    def _hook_gain_card(self, gained_card: Card) -> dict[str, Any]:
        """Hook which is fired by a card being obtained by a player"""
        assert isinstance(gained_card, Card)
        options: dict[str, Any] = {}
        if self.hooks.get("gain_card"):
            opts = self.hooks["gain_card"](
                game=self.game, player=self, card=gained_card
            )
            options |= opts

        for card in self.relevant_cards():
            self.currcards.append(card)
            opts = card.hook_gain_card(game=self.game, player=self, card=gained_card)
            self.currcards.pop()
            if opts:
                options.update(opts)
        return options

    ###########################################################################
    def has_defense(self, attacker: "Player", verbose: bool = True) -> bool:
        """Does this player have a defense against attack"""
        for crd in self.piles[Piles.HAND]:
            if crd.has_defense():
                if verbose:
                    attacker.output(f"Player {self.name} is defended")
                return True
        return False

    ###########################################################################
    def add_actions(self, num: int = 1) -> None:
        assert isinstance(num, int)
        if self.misc.get("no_actions"):
            self.output("No more additional actions allowed")
        else:
            self.actions += num

    ###########################################################################
    def gain_prize(self) -> None:
        """Pickup a Prize"""
        prizes = [self.game.card_piles[_] for _ in self.game.getPrizes()]
        options = []
        for prize_pile in prizes:
            if prize_pile.is_empty():
                continue
            prize = prize_pile.top_card()
            options.append((f"Gain {prize}", prize))
        if options:
            self.output("Gain a prize")
            if option := self.plr_choose_options("Gain a Prize", *options):
                prize = self.game.get_card_from_pile(option)
                self.add_card(prize)
        else:
            self.output("No prizes available")

    ###########################################################################
    def __str__(self) -> str:
        return f"<Player {self.name}>"

    ###########################################################################
    def buy_project(self, project: Project) -> bool:
        assert issubclass(project.__class__, Project)
        if not self.buys:
            self.output("Need a buy to buy a project")
            return False
        if self.debt:
            self.output("Must pay off debt first")
            return False
        if self.coins.get() < project.cost:
            self.output(f"Need {project.cost} coins to buy this project")
            return False
        self.buys -= 1
        self.coins -= project.cost
        self.debt += project.debtcost
        self.buys += project.buys
        self.assign_project(project.name)
        return True

    ###########################################################################
    def perform_event(self, event: Event) -> bool:
        """Perform an event"""
        try:
            assert isinstance(event, Event)
        except AssertionError:
            print(f"Event={event} ({type(event)})")
            raise

        if not self.buys:
            self.output("Need a buy to perform an event")
            return False
        if self.debt:
            self.output("Must pay off debt first")
        if self.coins < event.cost:
            self.output(f"Need {event.cost} coins to perform this event")
            return False
        self.buys -= 1
        self.coins -= event.cost
        self.debt += event.debtcost
        self.buys += event.buys
        self.output(f"Using event {event}")
        self.currcards.append(event)
        event.special(game=self.game, player=self)
        self.currcards.pop()
        self.played_events.add(event)
        return True

    ###########################################################################
    @classmethod
    def select_by_type(cls, card: Card, types) -> bool:
        assert isinstance(card, Card), f"select_by_type {card=} {type(card)=}"
        if card.isAction() and not types[CardType.ACTION]:
            return False
        if card.isVictory() and not types[CardType.VICTORY]:
            return False
        if card.isTreasure() and not types[CardType.TREASURE]:
            return False
        if card.isNight() and not types[CardType.NIGHT]:
            return False
        return True

    ###########################################################################
    def cards_affordable(
        self,
        oper: Callable[[int, int], bool],
        coin: int,
        num_potions: int,
        types: Optional[dict[CardType, bool]],
    ) -> list[Card]:
        """Return the list of cards for under cost
        {coin} {num_potions} are the resources constraints we have
        """
        affordable = PlayArea("affordable")
        for name, pile in self.game.get_card_piles():
            if not pile:
                continue
            card = pile.get_top_card()
            assert card is not None
            cost = self.card_cost(card)
            if not self.select_by_type(card, types):
                continue
            if not card.purchasable:
                continue
            if card.always_buyable:
                affordable.add(card)
                continue
            if coin is None:
                affordable.add(card)
                continue
            if card.debtcost and not card.cost:
                affordable.add(card)
                continue
            if oper(cost, coin) and oper(card.potcost, num_potions):
                affordable.add(card)
                continue
        affordable.sort(key=self.card_cost)
        affordable.sort(key=lambda x: x.basecard)
        return list(affordable)

    ###########################################################################
    def cards_under(
        self,
        coin: int,
        num_potions: int = 0,
        types: Optional[dict[CardType, bool]] = None,
    ) -> list[Card]:
        """Return the list of cards for under cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.le, coin, num_potions, types)

    ###########################################################################
    def cards_worth(
        self,
        coin: int,
        num_potions: int = 0,
        types: Optional[dict[CardType, bool]] = None,
    ) -> list[Card]:
        """Return the list of cards that are exactly cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.eq, coin, num_potions, types)

    ###########################################################################
    def get_cards(self) -> dict[str, int]:
        """Return a list of all the cards owned"""
        cards: defaultdict[str, int] = defaultdict(int)
        for _, stack in self.piles.items():
            for card in stack:
                cards[card.name] += 1
        return dict(cards)

    ###########################################################################
    def count_cards(self) -> int:
        """How many cards does the player have"""
        count: dict[str, int] = {}
        for name, stack in self.piles.items():
            count[name] = len(stack)
        total = sum(count.values())
        total += self.secret_count
        return total

    ###########################################################################
    @classmethod
    def _type_selector(
        cls, types: Optional[dict[CardType, bool]] = None
    ) -> dict[CardType, bool]:
        if types is None:
            types = {}
        assert set(types.keys()) <= {
            CardType.ACTION,
            CardType.VICTORY,
            CardType.TREASURE,
            CardType.NIGHT,
        }
        if not types:
            return {
                CardType.ACTION: True,
                CardType.VICTORY: True,
                CardType.TREASURE: True,
                CardType.NIGHT: True,
            }
        _types = {
            CardType.ACTION: False,
            CardType.VICTORY: False,
            CardType.TREASURE: False,
            CardType.NIGHT: False,
        }
        _types.update(types)
        return _types

    ###########################################################################
    def attack_victims(self) -> list[Player]:
        """Return list of other players who don't have defences"""
        victims: list[Player] = []
        for plr in list(self.game.players.values()):
            if plr == self:
                continue
            for crd in plr.piles[Piles.HAND]:
                crd.hook_under_attack(game=self.game, player=plr, attacker=self)
            if plr.has_defense(self):
                continue
            victims.append(plr)
        return victims

    ###########################################################################
    def _cost_string(self, card: Card) -> str:
        """Generate the string showing the cost of the card"""
        assert isinstance(card, (Card, Event, Project))
        cost = [f"{self.card_cost(card)} Coins"]
        if card.debtcost:
            cost.append(f"{card.debtcost} Debt")
        if card.potcost:
            cost.append("Potion")
        if card.overpay:
            cost.append("Overpay")
        cost_str = ", ".join(cost)
        return cost_str.strip()

    ###########################################################################
    def plr_trash_card(
        self, num=1, anynum=False, cardsrc=Piles.HAND, **kwargs
    ) -> Optional[list[Card]]:
        """Ask player to trash num cards"""
        if "prompt" not in kwargs:
            kwargs["prompt"] = "Trash any cards" if anynum else f"Trash {num} cards"
        if isinstance(cardsrc, str):
            for pname, pile in self.piles.items():
                if pname.lower() == cardsrc.lower():
                    if len(pile) == 0:
                        self.output(f"No cards to trash from {cardsrc}")
                        return None
        if isinstance(cardsrc, PlayArea) and len(cardsrc) == 0:
            self.output("No cards to trash")
            return None
        trash = self.card_sel(
            num=num,
            cardsrc=cardsrc,
            anynum=anynum,
            verbs=("Trash", "Untrash"),
            **kwargs,
        )
        if trash is None:
            return None
        for crd in trash:
            self.trash_card(crd, **kwargs)
        return trash

    ###########################################################################
    def plr_gain_card(
        self,
        cost: int,
        modifier="less",
        recipient=None,
        destination=Piles.DISCARD,
        **kwargs,
    ) -> Optional[Card]:
        """Gain a card up to cost coin
        if recipient defined then that player gets the card
        kwargs:
            prompt = prompt
            ignore_debt - normally you can't gain a card with a debt cost
            ignore_potcost - normally you can't gain a card with a potion cost
        """
        if recipient is None:
            recipient = self

        kwargs["prompt"] = kwargs.get(
            "prompt", self._get_buyable_prompt(cost, modifier)
        )

        if "cardsrc" in kwargs:
            cardsrc = kwargs["cardsrc"]
            del kwargs["cardsrc"]
        else:
            cardsrc = self._get_buyable(cost, modifier, **kwargs)
            if not cardsrc:
                self.output("Nothing suitable to gain")
                return None
        if cards := self.card_sel(
            cardsrc=cardsrc,
            recipient=recipient,
            verbs=("Get", "Unget"),
            **kwargs,
        ):
            card_name = cards[0].name
            new_card = recipient.gain_card(card_name, destination)
            recipient.output(f"Got a {new_card}")
            return new_card
        return None

    ###########################################################################
    def _get_buyable_prompt(self, cost: int, modifier: str) -> str:
        """Return the prompt for buying cards"""
        prompt = "Gain a card "
        assert modifier in ("less", "equal")
        if cost:
            if modifier == "less":
                prompt += f"costing up to {cost}"
            elif modifier == "equal":
                prompt += f"costing exactly {cost}"
        return prompt

    ###########################################################################
    def _get_buyable(self, cost: int, modifier: str, **kwargs: Any) -> list[str]:
        """Return the list of cards that are buyable for cost"""
        types = kwargs.get("types", {})
        buyable: list[str] = []
        types = self._type_selector(types)
        if modifier == "less":
            buyable = self.cards_under(cost, types=types)
        elif modifier == "equal":
            buyable = self.cards_worth(cost, types=types)
        buyable = [_ for _ in buyable if _.purchasable]
        if not kwargs.get("ignore_debt", False):
            buyable = [_ for _ in buyable if not _.debtcost]
        if not kwargs.get("ignore_potcost", False):
            buyable = [_ for _ in buyable if not _.potcost]
        buyable = [_ for _ in buyable if _.name not in kwargs.get("exclude", [])]
        return buyable

    ###########################################################################
    def plr_pick_card(self, force: bool = False, **kwargs: Any) -> Card:
        sel = self.card_sel(force=force, **kwargs)
        assert sel is not None
        return sel[0]

    ###########################################################################
    def has_state(self, state: str) -> bool:
        return state in [_.name for _ in self.states]

    ###########################################################################
    def has_artifact(self, artifact: str) -> bool:
        return artifact in [_.name for _ in self.artifacts]

    ###########################################################################
    def assign_state(self, state: str) -> None:
        """Assign a state to the player - remove from other players if unique"""
        assert isinstance(state, str)
        state_card = self.game.states[state]

        if state_card.unique_state:
            for player in self.game.player_list():
                for st in player.states[:]:
                    if st.name == state:
                        player.states.remove(st)
                        break
        self.states.append(state_card)

    ###########################################################################
    def assign_artifact(self, artifact: str) -> None:
        assert isinstance(artifact, str)
        artifact_card = self.game.artifacts[artifact]
        # Remove artifact from whoever currently has it
        for pl in self.game.player_list():
            for st in pl.artifacts[:]:
                if st.name == artifact and self != pl:
                    pl.output(f"{self.name} took your {artifact}")
                    pl.artifacts.remove(st)
                    break
        # If we already have it don't get it again
        if artifact_card not in self.artifacts:
            self.artifacts.append(artifact_card)

    ###########################################################################
    def assign_project(self, project: Project) -> bool:
        assert isinstance(project, str)
        project_card = self.game.projects[project]
        if len(self.projects) == 2:
            self.output("Can't have more than two projects")
            return False
        if project in [_.name for _ in self.projects]:
            self.output(f"Already have project {project}")
            return False
        self.projects.append(project_card)
        return True

    ###########################################################################
    def remove_state(self, state: State | str) -> None:
        if isinstance(state, str):
            name = state
        else:
            name = state.name
        self.states.remove([_ for _ in self.states if _.name == name][0])

    ###########################################################################
    def remove_artifact(self, artifact: Artifact | str) -> None:
        if isinstance(artifact, str):
            name = artifact
        else:
            name = artifact.name
        self.artifacts.remove([_ for _ in self.artifacts if _.name == name][0])

    ###########################################################################
    def plr_discard_cards(
        self, num: int = 1, any_number: bool = False, **kwargs: Any
    ) -> Optional[list[Card]]:
        """Get the player to discard exactly num cards"""
        if "prompt" not in kwargs:
            if any_number:
                kwargs["prompt"] = "Discard any number of cards"
            else:
                kwargs["prompt"] = f"Discard {num} cards"
        discard = self.card_sel(
            num=num, anynum=any_number, verbs=("Discard", "Undiscard"), **kwargs
        )
        if discard is None:
            return None
        for card in discard:
            self.output(f"Discarding {card}")
            self.discard_card(card)
        return discard

    ###########################################################################
    def plr_discard_down_to(self, num: int) -> None:
        """Get the player to discard down to num cards in their hand"""
        num_to_go = len(self.piles[Piles.HAND]) - num
        if num_to_go <= 0:
            return
        self.plr_discard_cards(num_to_go, force=True)

    ###########################################################################
    def game_over(self) -> None:
        """Game is over - do anything special required"""
        for card in self.end_of_game_cards + list(self.game.landmarks.values()):
            card.hook_end_of_game(game=self.game, player=self)

    ###########################################################################
    def output(self, msg: str, end: str = "") -> None:
        raise NotImplementedError

    ###########################################################################
    def plr_choose_options(self, prompt: str, *choices: tuple[str, Any]) -> Any:
        raise NotImplementedError

    ###########################################################################
    def user_input(self, options: list[Option | dict[str, Any]], prompt: str) -> Any:
        raise NotImplementedError

    ###########################################################################
    def card_sel(self, num: int = 1, **kwargs: Any) -> list[Card] | None:
        raise NotImplementedError

    ###########################################################################
    def card_pile_sel(self, num: int = 1, **kwargs: Any) -> list[str] | None:
        raise NotImplementedError


# EOF
