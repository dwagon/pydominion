#!/usr/bin/env python3
""" All the Player based stuff """
# pylint: disable=too-many-instance-attributes, too-many-public-methods
from __future__ import annotations
import json
import operator
import sys
from collections import defaultdict
from typing import Optional
from icecream import ic

ic.configureOutput(includeContext=True)

from dominion import Piles, Phase
from dominion.Card import Card, CardType
from dominion.CardPile import CardPile
from dominion.Counter import Counter
from dominion.Event import EventPile
from dominion.Option import Option
from dominion.PlayArea import PlayArea
from dominion.ProjectPile import ProjectPile
from dominion.Way import Way


###############################################################################
###############################################################################
###############################################################################
class Player:
    """All things player - generally subclassed for interface reasons"""

    def __init__(self, game, name, heirlooms=None, use_shelters=False):
        self.game = game
        self.name = name
        self.currcards = []
        self.score = {}
        self.had_cards = []
        self.messages = []
        self.hooks = {}
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
        self.projects = []
        self.states = []
        self.artifacts = []

        self.buys = Counter("Buys", 1)
        self.actions = Counter("Actions", 1)
        self.coins = Counter("Coins", 0)
        self.potions = Counter("Potions", 0)
        self.villagers = Counter("Villager", 0)
        self.debt = Counter("Debt", 0)
        self.coffers = Counter("Coffers", 0)
        self.favors = Counter("Favors", 0)
        self.newhandsize = 5
        self.playlimit = None
        self.card_token = False
        self.coin_token = False
        self.journey_token = True
        self.test_input = []
        self.forbidden_to_buy = []
        self.played_events = PlayArea("played_events", game=self.game)
        self.played_ways = []
        self._initial_deck(heirlooms, use_shelters)
        self._initial_tokens()
        self.once = {}
        self.turn_number = 0
        self.stats = {"gained": [], "bought": [], "trashed": []}
        self.pick_up_hand()
        self.secret_count = 0  # Hack to count cards that aren't anywhere normal
        self.end_of_game_cards = []
        self.phase = Phase.NONE
        self.misc = {"is_start": False, "cleaned": False}
        self.skip_turn = False
        game.output(f"Player {name} is at the table")

    ###########################################################################
    def _initial_deck(self, heirlooms=None, use_shelters=False):
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
    def _use_shelters(self):
        """Pick shelters out of the pile until we have one of each type"""
        shelters = ["Overgrown Estate", "Hovel", "Necropolis"]
        for shelter in shelters:
            card = self.game.get_card_from_pile("Shelters", shelter)
            self.add_card(card, Piles.DECK)

    ###########################################################################
    def _initial_tokens(self):
        self.tokens = {
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
    def replace_traveller(self, src, dst):
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
    def replace_card(self, src: Card, dst: str, **kwargs) -> None:
        """Replace the {src} card with the {dst} card"""
        # New card goes into hand as it is about to be discarded
        destination = kwargs.get("destination", Piles.DISCARD)
        assert isinstance(src, Card), f"replace_card {src=} {type(src)=}"
        assert isinstance(dst, str), f"replace_card {dst=} {type(dst)=}"

        newcard = self.gain_card(card_name=dst, destination=destination, callhook=False)
        if newcard:
            card_pile = self.game.card_piles[src.name]
            card_pile.add(src)
            self.piles[Piles.PLAYED].remove(src)

    ###########################################################################
    def flip_journey_token(self):
        """Flip a journey token - and return its new state"""
        if self.journey_token:
            self.journey_token = False
        else:
            self.journey_token = True
        return self.journey_token

    ###########################################################################
    def receive_hex(self, hx=None):
        """Receive a hex"""
        if hx is None:
            hx = self.game.receive_hex()
        self.output(f"Received {hx} as a hex")
        self.output(hx.description(self))
        for _ in range(hx.cards):
            self.pickup_card()
        self.add_actions(hx.actions)
        self.buys += hx.buys
        self.coins += self.hook_spend_value(hx, actual=True)
        hx.special(game=self.game, player=self)
        self.game.discard_hex(hx)

    ###########################################################################
    def receive_boon(self, boon=None, discard=True):
        """Receive a boon"""
        if boon is None:
            boon = self.game.receive_boon()
        self.output(f"Received {boon} as a boon")
        self.output(boon.description(self))
        for _ in range(boon.cards):
            self.pickup_card()
        self.add_actions(boon.actions)
        self.buys += boon.buys
        self.coins += self.hook_spend_value(boon, actual=True)
        boon.special(game=self.game, player=self)
        if discard:
            self.game.discard_boon(boon)
        return boon

    ###########################################################################
    def do_once(self, name):
        """Allow a player to do something once per turn"""
        if name in self.once:
            return False
        self.once[name] = True
        return True

    ###########################################################################
    def place_token(self, token, pilename):
        """Place a token on the specified pile"""
        assert isinstance(pilename, str)
        self.tokens[token] = pilename

    ###########################################################################
    def which_token(self, pilename):
        """Return which token(s) are on a cardstack"""
        assert isinstance(pilename, str)
        onstack = []
        for token_name, token in self.tokens.items():
            if token == pilename:
                onstack.append(token_name)
        return onstack

    ###########################################################################
    def call_reserve(self, card):
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
    def reveal_card(self, card):
        """Reveal a card to everyone"""
        if not card:
            return
        self.game.output(f"{self.name} reveals {card}")
        card.hook_revealThisCard(game=self.game, player=self)

    ###########################################################################
    def trash_card(self, card: Card, **kwargs):
        """Take a card out of the game"""
        assert isinstance(card, Card)
        self.stats["trashed"].append(card)
        trash_opts = {}
        rc = card.hook_trashThisCard(game=self.game, player=self)
        if rc:
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
    def next_card(self) -> Optional[Card]:
        """Pick up and return the next card from the deck"""
        if not self.piles[Piles.DECK]:
            self.refill_deck()
        if not self.piles[Piles.DECK]:
            self.output("No more cards in deck")
            return None
        crd = self.piles[Piles.DECK].next_card()
        crd.location = None  # We don't know where it is going yet
        return crd

    ###########################################################################
    def top_card(self) -> Optional[Card]:
        """Return the top card from the deck but don't pick it up"""
        if not self.piles[Piles.DECK]:
            self.refill_deck()
        if not self.piles[Piles.DECK]:
            self.output("No more cards in deck")
            return None
        crd = self.piles[Piles.DECK].top_card()
        return crd

    ###########################################################################
    def refill_deck(self):
        """Refill the player deck - shuffling if required"""
        self._shuffle_discard()
        while self.piles[Piles.DISCARD]:
            self.add_card(self.piles[Piles.DISCARD].next_card(), Piles.DECK)
        for card in self.relevant_cards():
            if hasattr(card, "hook_post_shuffle"):
                card.hook_post_shuffle(game=self.game, player=self)

    ###########################################################################
    def pickup_cards(self, num, verbose=True, verb="Picked up"):
        """Pickup multiple cards into players hand"""
        cards = []
        for _ in range(num):
            cards.append(self.pickup_card(verbose=verbose, verb=verb))
        return cards

    ###########################################################################
    def pickup_card(self, card=None, verbose=True, verb="Picked up"):
        """Pick a card from the deck and put it into the players hand"""
        if card is None:
            card = self.next_card()
            if not card:
                self.output("No more cards to pickup")
                return None
        assert isinstance(card, Card)
        self.add_card(card, Piles.HAND)
        if verbose:
            self.output(f"{verb} {card}")
        return card

    ###########################################################################
    def _shuffle_discard(self):
        self.output(f"Shuffling Pile of {len(self.piles[Piles.DISCARD])} cards")
        for card in self.projects:
            if hasattr(card, "hook_pre_shuffle"):
                card.hook_pre_shuffle(game=self.game, player=self)
        self.piles[Piles.DISCARD].shuffle()

    ###########################################################################
    def pick_up_hand(self, handsize=None):
        """Replenish hand from deck"""
        if handsize is None:
            handsize = self.newhandsize
        if self.card_token:
            self.output("-Card token reduce draw by one")
            handsize -= 1
            self.card_token = False
        while self.piles[Piles.HAND].size() < handsize:
            c = self.pickup_card(verb="Dealt")
            if not c:
                self.output("Not enough cards to fill hand")
                break

    ###########################################################################
    def remove_card(self, card: Card) -> None:
        """Remove a card from wherever it is"""
        if card.location in self.piles:
            self.piles[card.location].remove(card)
        elif card.location == Piles.CARDPILE:
            pass
        else:
            raise AssertionError(
                f"Trying to remove_card {card} from unknown location: {card.location}"
            )

    ###########################################################################
    def move_card(self, card: Card, dest) -> Card:
        """Move a card to {dest} card pile"""
        self.remove_card(card)
        return self.add_card(card, dest)

    ###########################################################################
    def add_card(self, card: Card, pile=Piles.DISCARD) -> Optional[Card]:
        """Add an existing card to a new location"""
        if not card:  # pragma: no cover
            return None
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
    def discard_card(self, card, source=None, hook=True):
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
    def discard_hand(self):
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
    def _playable_selection(self, index):
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
    def _night_selection(self, index):
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
    def _spendable_selection(self):
        options = []
        spendable = [c for c in self.piles[Piles.HAND] if c.isTreasure()]
        spendable.sort(key=lambda x: x.name)
        totcoin = sum(self.hook_spend_value(_) for _ in spendable)
        numpots = sum(1 for _ in spendable if _.name == "Potion")
        potstr = f", {numpots} potions" if numpots else ""
        details = f"{totcoin} coin{potstr}"
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
    def _get_whens(self):
        """Return when we are for calling reserve cards"""
        whens = ["any"]
        for c in self.piles[Piles.PLAYED]:
            if c.isAction():
                whens.append("postaction")
        if self.misc["is_start"]:
            whens.append("start")
        return whens

    ###########################################################################
    def _reserve_selection(self, index):
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
    def _project_selection(self, index):
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
    def _event_selection(self, index):
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
    def _card_check(self):
        for pile in self.piles:
            for card in self.piles[pile]:
                assert (
                    card.location == pile
                ), f"{self.name} {card.name=} {pile=} {card.location=}"

    ###########################################################################
    def _get_all_purchasable(self):
        """Return all potentially purchasable cards"""
        all_cards = PlayArea("all_purchasable")
        for name, pile in self.game.get_card_piles():
            if pile.is_empty():
                continue
            card = pile.get_top_card()
            if not card.purchasable:
                continue
            all_cards.add(card)
        all_cards.sort(key=self.card_cost)
        all_cards.sort(key=lambda x: x.basecard)
        return all_cards

    ###########################################################################
    def _buyable_selection(self, index):
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
                details.append(f"Embargo {card.embargo_level}")
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
    def _choice_selection(self):
        index = 0
        o = Option(selector="0", verb="End Phase", card=None, action="quit")
        options = [o]

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

        prompt = self._generate_prompt()
        return options, prompt

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
        if self.playlimit is not None:
            status += f" Play Limit={self.playlimit}"
        prompt = f"What to do ({status})?"
        return prompt

    ###########################################################################
    def turn(self):
        """Have a turn as the player"""
        self.turn_number += 1
        self.output("\n")
        self.output(f"{'#' * 20} Turn {self.turn_number} {'#' * 20}")
        stats = f"({self.get_score()} points, {self.count_cards()} cards)"
        if self.skip_turn:
            self.skip_turn = False
            return
        self.output(f"{self.name}'s Turn {stats}")
        self._card_check()  # DEBUG
        self.action_phase()
        self._card_check()  # DEBUG
        self.buy_phase()
        self._card_check()  # DEBUG
        self.night_phase()
        self._card_check()  # DEBUG
        self.cleanup_phase()
        self._card_check()  # DEBUG

    ###########################################################################
    def night_phase(self):
        """Do the Night Phase"""
        nights = [_ for _ in self.piles[Piles.HAND] if _.isNight()]
        if not nights:
            return
        self.output("************ Night Phase ************")
        self.phase = Phase.NIGHT
        while True:
            self._display_overview()
            options, prompt = self._choice_selection()
            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                return

    ###########################################################################
    def action_phase(self):
        self.output("************ Action Phase ************")
        self.phase = Phase.ACTION
        while True:
            self._display_overview()
            options, prompt = self._choice_selection()
            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                return

    ###########################################################################
    def buy_phase(self):
        self.output("************ Buy Phase ************")
        self.phase = Phase.BUY
        self.hook_pre_buy()
        while True:
            self._display_overview()
            options, prompt = self._choice_selection()
            opt = self.user_input(options, prompt)
            self._perform_action(opt)
            if opt["action"] == "quit":
                break
        self.hook_end_buy_phase()

    ###########################################################################
    def hook_end_buy_phase(self):
        for card in self.piles[Piles.PLAYED] + self.projects:
            card.hook_end_buy_phase(game=self.game, player=self)

    ###########################################################################
    def cleanup_phase(self):
        # Save the cards we had so that the hook_end_turn has something to apply against
        self.had_cards = (
            self.piles[Piles.PLAYED]
            + self.piles[Piles.RESERVE]
            + self.played_events
            + self.game.landmarks
            + self.piles[Piles.DURATION]
        )
        self.phase = Phase.CLEANUP
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
    def payback(self):
        payback = min(self.coins.get(), self.debt.get())
        self.output(f"Paying back {payback} debt")
        self.coins -= payback
        self.debt -= payback

    ###########################################################################
    def _perform_action(self, opt):
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
        else:  # pragma: no cover
            print(f"ERROR: Unhandled action {opt['action']}", file=sys.stderr)
            sys.exit(1)
        self.misc["is_start"] = False

    ###########################################################################
    def _display_tokens(self) -> str:
        """Generate the overview display for tokens"""
        tknoutput = []
        for tkn, tkv in self.tokens.items():
            if tkv:
                tknoutput.append(f"{tkn}: {tkv}")
        if self.card_token:
            tknoutput.append("-1 Card")
        if self.coin_token:
            tknoutput.append("-1 Coin")
        if self.journey_token:
            tknoutput.append("Journey Faceup")
        else:
            tknoutput.append("Journey Facedown")
        return "; ".join(tknoutput)

    ###########################################################################
    def _display_overview(self) -> None:
        """Display turn summary overview to player"""
        self.output("")
        self.output("-" * 50)
        self.output(f"| Phase: {self.phase.name.title()}")
        for lndmark in self.game.landmarks.values():
            self.output(f"| Landmark {lndmark.name}: {lndmark.description(self)}")
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
    def add_score(self, reason, points=1):
        """Add score to the player"""
        if reason not in self.score:
            self.score[reason] = 0
        self.score[reason] += points

    ###########################################################################
    def all_cards(self):
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
    def get_score_details(self) -> dict:
        """Calculate score of the player from all factors"""
        score = {}
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
    def get_score(self, verbose=False):
        """Return the scores - print them if {verbose} is True"""
        scr = self.get_score_details()
        vp = sum(scr.values())
        if verbose:
            self.game.output(
                f"{self.name} (Turn {self.turn_number}): {json.dumps(scr, indent=2)}"
            )
        return vp

    ###########################################################################
    def hook_pre_buy(self):
        """Hook that fires off before the buy phase"""
        for card in self.relevant_cards():
            card.hook_pre_buy(game=self.game, player=self)

    ###########################################################################
    def hook_allowed_to_buy(self, card):
        """Hook to check if you are allowed to buy a card"""
        return card.hook_allowed_to_buy(game=self.game, player=self)

    ###########################################################################
    def hook_buy_card(self, card):
        """Hook for after purchasing a card"""
        for c in self.relevant_cards():
            c.hook_buy_card(game=self.game, player=self, card=card)

    ###########################################################################
    def start_turn(self):
        self.phase = Phase.START
        self.piles[Piles.PLAYED].empty()
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
    def _defer_start_turn(self):
        """Perform the defer-pile cards at the start of the turn"""
        for card in self.piles[Piles.DEFER]:
            self.output(f"Playing deferred {card}")
            self.currcards.append(card)
            self.move_card(card, Piles.HAND)
            self.play_card(card, cost_action=False)
            self.currcards.pop()

    ###########################################################################
    def _duration_start_turn(self):
        """Perform the duration pile at the start of the turn"""
        for card in self.piles[Piles.DURATION]:
            options = {"dest": Piles.PLAYED}
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

    ###########################################################################
    def _hook_start_turn(self):
        """Start of turn hook"""
        for c in self.piles[Piles.HAND] + self.states + self.projects + self.artifacts:
            c.hook_start_turn(self.game, self)
        if self.game.ally:
            self.game.ally.hook_start_turn(self.game, self)

    ###########################################################################
    def spend_coffer(self):
        """Spend a coffer to gain a coin"""
        if self.coffers.get() <= 0:
            return
        self.coffers -= 1
        self.coins += 1
        self.output("Spent a coffer")

    ###########################################################################
    def spend_villager(self):
        """Spend a villager to gain an action"""
        if self.villagers.get() <= 0:
            return
        self.villagers -= 1
        self.add_actions(1)
        self.output("Spent a villager")

    ###########################################################################
    def exile_card(self, card):
        """Send a card to the exile pile; if the card is a name then take it
        from supply"""
        if isinstance(card, str):
            card = self.game.get_card_from_pile(card)
            if card is None:
                self.output(f"No more {card} in supply")
                return
        self.move_card(card, Piles.EXILE)

    ###########################################################################
    def end_turn(self):
        """End of turn"""
        if not self.misc["cleaned"]:
            self.cleanup_phase()
        self.playlimit = None
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
    def hook_discard_this_card(self, card, source=None):
        """A card has been discarded"""
        self.currcards.append(card)
        card.hook_discard_this_card(game=self.game, player=self, source=source)
        self.currcards.pop()

    ###########################################################################
    def hook_spend_value(self, card, actual=False):
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
    def _spend_all_cards(self):
        """Spend all treasure cards in hand"""
        for card in self.piles[Piles.HAND]:
            # Contents of hand can change as they are played
            if card.isTreasure() and card in self.piles[Piles.HAND]:
                self.play_card(card, cost_action=False)

    ###########################################################################
    def _play_card_tokens(self, card):
        tkns = self.which_token(card.name)
        if "+1 Action" in tkns:
            self.output("Gaining action from +1 Action token")
            self.add_actions(1)
        if "+1 Card" in tkns:
            c = self.pickup_card()
            self.output(f"Picked up {c.name} from +1 Card token")
        if "+1 Coin" in tkns:
            self.output("Gaining coin from +1 Coin token")
            self.coins += 1
        if "+1 Buy" in tkns:
            self.output("Gaining buy from +1 Buy token")
            self.buys += 1

    ###########################################################################
    def _hook_pre_action(self, card):
        """Hook before an action card is played"""
        options = {}
        for crd in self.piles[Piles.DURATION] + self.piles[Piles.PLAYED]:
            ans = crd.hook_pre_action(game=self.game, player=self, card=card)
            if ans:
                options.update(ans)
        return options

    ###########################################################################
    def hook_all_players_pre_action(self, card):
        options = {}
        for player in self.game.player_list():
            for crd in player.piles[Piles.DURATION]:
                ans = crd.hook_all_players_pre_action(
                    game=self.game, player=self, owner=player, card=card
                )
                if ans:
                    options.update(ans)
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
    def play_card(
        self,
        card: Card,
        discard: bool = True,
        cost_action: bool = True,
        post_action_hook: bool = True,
    ) -> None:
        """Play the card {card}"""
        options = {"skip_card": False, "discard": discard}
        if card not in self.piles[Piles.HAND] and options["discard"]:
            raise AssertionError(f"Playing {card} which is not in hand")
        if self.playlimit is not None:
            if self.playlimit <= 0:
                self.output(f"Can't play {card} due to limits in number of plays")
                return
            self.playlimit -= 1
        self.output(f"Playing {card}")
        self.currcards.append(card)
        if card.isAction():
            options.update(self._hook_pre_action(card))
            options.update(self.hook_all_players_pre_action(card))

        self._play_card_tokens(card)

        if card.isAction() and cost_action and self.phase != Phase.NIGHT:
            self.actions -= 1
        if self.actions.get() < 0:  # pragma: no cover
            self.actions.set(0)
            self.currcards.pop()
            self.output("Not enough actions")
            return

        force = options["skip_card"]

        if options["discard"]:
            self.move_after_play(card, force)

        if not options["skip_card"]:
            self.card_benefits(card)
        self.currcards.pop()
        if post_action_hook and card.isAction():
            for crd in self.relevant_cards():
                if hasattr(crd, "hook_post_action"):
                    crd.hook_post_action(game=self.game, player=self, card=card)

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
        newopts = way.special_way(game=self.game, player=self, card=card)
        if isinstance(newopts, dict):
            opts.update(newopts)
        if opts["discard"]:
            self.move_card(card, Piles.PLAYED)
        self.played_ways.append((way, card))
        self.currcards.pop()

    ###########################################################################
    def card_benefits(self, card):
        """Gain the benefits of the card being played - including special()"""
        self.add_actions(card.actions)
        self.coins += self.hook_spend_value(card, actual=True)
        self.buys += card.buys
        self.favors += card.favors
        self.potions += card.potion

        modif = 0
        if self.card_token and card.cards:
            self.output("-1 Card token reduces cards drawn")
            self.card_token = False
            modif = -1

        for _ in range(card.cards + modif):
            self.pickup_card()

        if self.phase == Phase.NIGHT:
            card.night(game=self.game, player=self)
        else:
            card.special(game=self.game, player=self)

    ###########################################################################
    def card_cost(self, card: Card) -> int:
        assert isinstance(
            card, (Card, ProjectPile, EventPile)
        ), f"Card{card=} {type(card)=}"
        cost = card.cost
        if "-Cost" in self.which_token(card.name):
            cost -= 2
        for crd in self.relevant_cards():
            cost += crd.hook_card_cost(game=self.game, player=self, card=card)
        cost += card.hook_this_card_cost(game=self.game, player=self)
        return max(0, cost)

    ###########################################################################
    def gain_card(
        self, card_name=None, destination=Piles.DISCARD, new_card=None, callhook=True
    ):
        """Add a new card to the players set of cards from a card pile, return the card gained"""
        # Options:
        #   dontadd: True - adding card handled elsewhere
        #   replace: <new_card> - Replace the gained card with <new_card>
        #   destination: <dest> - Move the new card to <dest> rather than discard pile
        #   trash: True - trash the new card
        #   shuffle: True - shuffle the deck after gaining new card
        options = {}
        if not new_card:
            pile = self.game.card_instances[card_name].pile
            if not pile:
                pile = card_name
            new_card = self.game.get_card_from_pile(pile)

        if not new_card:
            self.output(f"No more {card_name}")
            return None
        self.output(f"Gained a {new_card}")
        if callhook:
            if rc := self._hook_gain_card(new_card):
                options.update(rc)
            if rc := new_card.hook_gain_this_card(game=self.game, player=self):
                options.update(rc)

        # check for un-exiling
        if self.piles[Piles.EXILE][new_card.name]:
            self.check_unexile(new_card.name)

        # Replace is to gain a different card
        if options.get("replace"):
            self.game.card_piles[new_card.name].add(new_card)
            new_card = self.game.get_card_from_pile(options["replace"])
            if not new_card:
                self.output(f"No more {options['replace']}")
            else:
                new_card.player = self
        self.stats["gained"].append(new_card)
        destination = options.get("destination", destination)
        if callhook:
            self.hook_allplayers_gain_card(new_card)
        if options.get("trash", False):
            self.trash_card(new_card)
            return new_card
        if not options.get("dontadd", False):
            self.add_card(new_card, destination)
        if options.get("shuffle", False):
            self.piles[Piles.DECK].shuffle()
        return new_card

    ###########################################################################
    def check_unexile(self, card_name: str):
        """Give players option to un-exile card"""
        num = sum(1 for _ in self.piles[Piles.EXILE] if _.name == card_name)
        choices = [
            (f"Unexile {num} x {card_name}", True),
            ("Do nothing", False),
        ]
        unex = self.plr_choose_options(f"Un-exile {card_name}", *choices)
        if unex:
            self.unexile(card_name)

    ###########################################################################
    def unexile(self, cardname: str) -> int:
        """Un-exile cards
        Return number unexiled"""
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
    def overpay(self, card):
        """http://wiki.dominionstrategy.com/index.php/Overpay"""
        options = []
        for i in range(self.coins.get() + 1):
            options.append((f"Spend {i} more", i))
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
        if self.debt:
            self.output("Must pay off debt first")
            return
        self.buys -= 1
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
    def hook_all_players_buy_card(self, card):
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
    def hook_allplayers_gain_card(self, card):
        for player in self.game.player_list():
            for crd in player.relevant_cards():
                crd.hook_allplayers_gain_card(
                    game=self.game, player=self, owner=player, card=card
                )

    ###########################################################################
    def add_hook(self, hook_name, hook):
        self.hooks[hook_name] = hook

    ###########################################################################
    def relevant_cards(self):
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
        )

    ###########################################################################
    def _hook_gain_card(self, card):
        """Hook which is fired by a card being obtained by a player"""
        assert isinstance(card, Card)
        options = {}
        if self.hooks.get("gain_card"):
            o = self.hooks["gain_card"](game=self.game, player=self, card=card)
            options.update(o)

        for c in self.relevant_cards():
            self.currcards.append(c)
            o = c.hook_gain_card(game=self.game, player=self, card=card)
            self.currcards.pop()
            if o:
                options.update(o)
        return options

    ###########################################################################
    def has_defense(self, attacker: Player, verbose=True):
        """Does this player have a defense against attack"""
        for crd in self.piles[Piles.HAND]:
            if crd.has_defense():
                if verbose:
                    attacker.output(f"Player {self.name} is defended")
                return True
        return False

    ###########################################################################
    def add_actions(self, num=1):
        assert isinstance(num, int)
        if self.misc.get("no_actions"):
            self.output("No more additional actions allowed")
        else:
            self.actions += num

    ###########################################################################
    def gain_prize(self):
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
            option = self.plr_choose_options("Gain a Prize", *options)
            if option:
                prize = self.game.get_card_from_pile(option)
                self.add_card(prize)
        else:
            self.output("No prizes available")

    ###########################################################################
    def __str__(self):
        return f"<Player {self.name}>"

    ###########################################################################
    def buy_project(self, project):
        assert issubclass(project.__class__, ProjectPile)
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
    def perform_event(self, event: EventPile) -> bool:
        """Perform an event"""
        try:
            assert isinstance(event, EventPile)
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
    def select_by_type(cls, card, types):
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
    def cards_affordable(self, oper, coin: int, num_potions: int, types):
        """Return the list of cards for under cost
        {coin} {num_potions} are the resources constraints we have
        """
        affordable = PlayArea("affordable")
        for name, pile in self.game.get_card_piles():
            if not pile:
                continue
            card = pile.get_top_card()
            cost = self.card_cost(card)
            if not self.select_by_type(card, types):
                continue
            if not card.purchasable:
                continue
            if card.always_buyable:
                affordable.add(card)
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
        return [_ for _ in affordable]

    ###########################################################################
    def cards_under(self, coin, num_potions=0, types=None) -> list[str]:
        """Return the list of cards for under cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.le, coin, num_potions, types)

    ###########################################################################
    def cards_worth(self, coin, num_potions=0, types=None) -> list[str]:
        """Return the list of cards that are exactly cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.eq, coin, num_potions, types)

    ###########################################################################
    def get_cards(self):
        """Return a list of all the cards owned"""
        cards = defaultdict(int)
        for _, stack in self.piles.items():
            for card in stack:
                cards[card.name] += 1
        return cards

    ###########################################################################
    def count_cards(self):
        """How many cards does the player have"""
        count = {}
        for name, stack in self.piles.items():
            count[name] = len(stack)
        total = sum(count.values())
        total += self.secret_count
        return total

    ###########################################################################
    @classmethod
    def _type_selector(cls, types=None):
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
    def attack_victims(self):
        """Return list of other players who don't have defences"""
        victims = []
        for plr in list(self.game.players.values()):
            if plr == self:
                continue
            for crd in plr.piles[Piles.HAND]:
                crd.hook_underAttack(game=self.game, player=plr, attacker=self)
            if plr.has_defense(self):
                continue
            victims.append(plr)
        return victims

    ###########################################################################
    def _cost_string(self, card) -> str:
        """Generate the string showing the cost of the card"""
        assert isinstance(card, (Card, EventPile, ProjectPile))
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
    ) -> Optional[Card]:
        """Ask player to trash num cards"""
        if "prompt" not in kwargs:
            if anynum:
                kwargs["prompt"] = "Trash any cards"
            else:
                kwargs["prompt"] = f"Trash {num} cards"
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

        buyable = self._get_buyable(cost, modifier, **kwargs)
        if not buyable:
            self.output("Nothing suitable to gain")
            return
        cards = self.card_sel(
            cardsrc=buyable,
            recipient=recipient,
            verbs=("Get", "Unget"),
            **kwargs,
        )
        if cards:
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
    def _get_buyable(self, cost: int, modifier: str, **kwargs):
        """Return the list of cards that are buyable for cost"""
        types = kwargs.get("types", {})
        buyable = []
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
    def plr_pick_card(self, force=False, **kwargs):
        sel = self.card_sel(force=force, **kwargs)
        return sel[0]

    ###########################################################################
    def has_state(self, state):
        return state in [_.name for _ in self.states]

    ###########################################################################
    def has_artifact(self, artifact):
        return artifact in [_.name for _ in self.artifacts]

    ###########################################################################
    def assign_state(self, state):
        assert isinstance(state, str)
        state_card = self.game.states[state]

        if state_card.unique_state:
            for pl in self.game.player_list():
                for st in pl.states[:]:
                    if st.name == state:
                        pl.states.remove(st)
                        break
        self.states.append(state_card)

    ###########################################################################
    def assign_artifact(self, artifact):
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
    def assign_project(self, project):
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
    def remove_state(self, state):
        if isinstance(state, str):
            name = state
        else:
            name = state.name
        self.states.remove([_ for _ in self.states if _.name == name][0])

    ###########################################################################
    def remove_artifact(self, artifact):
        if isinstance(artifact, str):
            name = artifact
        else:
            name = artifact.name
        self.artifacts.remove([_ for _ in self.artifacts if _.name == name][0])

    ###########################################################################
    def plr_discard_cards(self, num=1, any_number=False, **kwargs):
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
            self.output(f"Discarding {card.name}")
            self.discard_card(card)
        return discard

    ###########################################################################
    def plr_discard_down_to(self, num):
        """Get the player to discard down to num cards in their hand"""
        num_to_go = len(self.piles[Piles.HAND]) - num
        if num_to_go <= 0:
            return
        self.plr_discard_cards(num_to_go, force=True)

    ###########################################################################
    def game_over(self):
        """Game is over - do anything special required"""
        for card in self.end_of_game_cards + list(self.game.landmarks.values()):
            card.hook_end_of_game(game=self.game, player=self)

    ###########################################################################
    def output(self, msg, end=None):
        raise NotImplementedError

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        raise NotImplementedError

    ###########################################################################
    def user_input(self, options, prompt):
        raise NotImplementedError

    ###########################################################################
    def card_sel(self, num=1, **kwargs):
        raise NotImplementedError


# EOF
