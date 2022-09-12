""" All the Player based stuff """
# pylint: disable=too-many-instance-attributes, too-many-public-methods
from __future__ import annotations
import operator
import sys
from collections import defaultdict
from typing import Union

from dominion import Card
from dominion.Counter import Counter
from dominion.PlayArea import PlayArea
from dominion.Option import Option
from dominion.CardPile import CardPile
from dominion.Event import EventPile
from dominion.ProjectPile import ProjectPile


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
        self.hand = PlayArea("hand", game=self.game)
        self.exilepile = PlayArea("exilepile", game=self.game)
        self.durationpile = PlayArea("durationpile", game=self.game)
        self.deferpile = PlayArea("deferpile", game=self.game)
        self.deck = PlayArea("deck", game=self.game)
        self.played = PlayArea("played", game=self.game)
        self.discardpile = PlayArea("discardpile", game=self.game)
        self.reserve = PlayArea("reserve", game=self.game)
        self.buys = 1
        self.actions = 1
        self.coin = 0
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
        self.phase = None
        self.misc = {"is_start": False, "cleaned": False}
        self.states = []
        self.artifacts = []
        self.projects = []
        self.skip_turn = False
        self.stacklist = (
            ("Discard", self.discardpile),
            ("Hand", self.hand),
            ("Reserve", self.reserve),
            ("Deck", self.deck),
            ("Played", self.played),
            ("Duration", self.durationpile),
            ("Exile", self.exilepile),
            ("Defer", self.deferpile),
        )
        game.output(f"Player {name} is at the table")

    ###########################################################################
    def _initial_deck(self, heirlooms=None, use_shelters=False):
        """Provide the initial deck - cards don't come from the piles
        hence add them back
        """
        if heirlooms is None:
            heirlooms = []

        for _ in range(7 - len(heirlooms)):
            card = self.game["Copper"].remove()
            card.player = self
            self.add_card(card, "deck")

        for hl in heirlooms:
            card = self.game[hl].remove()
            card.player = self
            self.add_card(card, "deck")

        if use_shelters:
            estates = ("Overgrown Estate", "Hovel", "Necropolis")
        else:
            estates = ("Estate", "Estate", "Estate")
        for cardname in estates:
            card = self.game[cardname].remove()
            card.player = self
            self.add_card(card, "deck")

        self.deck.shuffle()

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
    def _find_cardpile(self, cname):
        """Return the cardpile that has cards called {cname}"""
        dstcp = None
        for cp in self.game.cardpiles.values():
            if cp.name == cname:
                dstcp = cp
                break
        else:  # pragma: no cover
            assert dstcp is not None, f"Couldn't find cardpile {cname}"
        return dstcp

    ###########################################################################
    def replace_traveller(self, src, dst):
        """For traveller cards replace the src card with a copy of the
        dst card"""
        assert isinstance(src, Card.Card)
        assert isinstance(dst, str)
        dstcp = self._find_cardpile(dst)

        if src not in self.played:
            self.output(f"Not activating {src.name} traveller as not played")
            return

        choice = self.plr_choose_options(
            "Replace Traveller",
            (f"Keep {src.name}", "keep"),
            (f"Replace with a {dstcp.name}?", "replace"),
        )
        if choice == "keep":
            return
        if choice == "replace":
            self.replace_card(src, dst, destination="hand")

    ###########################################################################
    def replace_card(self, src, dst, **kwargs):
        """Replace the {src} card with the {dst} card"""
        # New card goes into hand as it is about to be discarded
        destination = kwargs["destination"] if "destination" in kwargs else "discard"

        dstcp = self._find_cardpile(dst)
        newcard = self.gain_card(cardpile=dstcp, destination=destination, callhook=False)
        if newcard:
            cardpile = self.game.cardpiles[src.name]
            cardpile.add(src)
            self.played.remove(src)

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
        self.coin += self.hook_spend_value(hx, actual=True)
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
        self.coin += self.hook_spend_value(boon, actual=True)
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
            card = self.reserve[card]
            if not card:
                return None
        assert isinstance(card, Card.Card)
        self.output(f"Calling {card.name} from Reserve")
        self.currcards.append(card)
        card.hook_call_reserve(game=self.game, player=self)
        self.currcards.pop()
        self.reserve.remove(card)
        self.add_card(card, "played")
        return card

    ###########################################################################
    def reveal_card(self, card):
        """Reveal a card to everyone"""
        self.game.output(f"{self.name} reveals {card.name}")
        card.hook_revealThisCard(game=self.game, player=self)

    ###########################################################################
    def trash_card(self, card, **kwargs):
        """Take a card out of the game"""
        assert isinstance(card, Card.Card)
        self.stats["trashed"].append(card)
        trashopts = {}
        rc = card.hook_trashThisCard(game=self.game, player=self)
        if rc:
            trashopts.update(rc)
        if trashopts.get("trash", True):
            self.game.trashpile.add(card)
            card.player = None
            card.location = "trash"
            if card in self.played:
                self.played.remove(card)
            elif card in self.hand:
                self.hand.remove(card)
        for crd in self.relevant_cards():
            if crd.name not in kwargs.get("exclude_hook", []):
                rc = crd.hook_trash_card(game=self.game, player=self, card=card)
                if rc:
                    trashopts.update(rc)

    ###########################################################################
    def next_card(self):
        """Return the next card from the deck, but don't pick it up"""
        if not self.deck:
            self.refill_deck()
        if not self.deck:
            self.output("No more cards in deck")
            return None
        crd = self.deck.next_card()
        return crd

    ###########################################################################
    def refill_deck(self):
        """Refill the player deck - shuffling if required"""
        self._shuffle_discard()
        while self.discardpile:
            self.add_card(self.discardpile.next_card(), "deck")
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
        assert isinstance(card, Card.Card)
        self.add_card(card, "hand")
        if verbose:
            self.output(f"{verb} {card.name}")
        return card

    ###########################################################################
    def _shuffle_discard(self):
        self.output(f"Shuffling Pile of {len(self.discardpile)} cards")
        for card in self.projects:
            if hasattr(card, "hook_pre_shuffle"):
                card.hook_pre_shuffle(game=self.game, player=self)
        self.discardpile.shuffle()

    ###########################################################################
    def pick_up_hand(self, handsize=None):
        if handsize is None:
            handsize = self.newhandsize
        if self.card_token:
            self.output("-Card token reduce draw by one")
            handsize -= 1
            self.card_token = False
        while self.hand.size() < handsize:
            c = self.pickup_card(verb="Dealt")
            if not c:
                self.output("Not enough cards to fill hand")
                break

    ###########################################################################
    def remove_card(self, card: Card) -> None:
        """Remove a card from wherever it is"""
        piles = {
            "discard": self.discardpile,
            "discardpile": self.discardpile,
            "hand": self.hand,
            "deck": self.deck,
            "played": self.played,
            "duration": self.durationpile,
            "reserve": self.reserve,
            "exilepile": self.exilepile,
        }
        curr_loc = card.location
        if curr_loc in piles:
            piles[curr_loc].remove(card)
        elif curr_loc == "cardpile":
            pass
        else:
            raise AssertionError(f"Trying to remove_card {card} from unknown location: {curr_loc}")

    ###########################################################################
    def move_card(self, card: Card, dest: Union[str, PlayArea]) -> Card:
        """Move a card to {dest} cardpile"""
        self.remove_card(card)
        return self.add_card(card, dest)

    ###########################################################################
    def add_card(self, card: Card, pile: Union[str, PlayArea] = "discard") -> Card:
        """Add an existing card to a new location"""
        piles = {
            "discard": self.discardpile,
            "discardpile": self.discardpile,
            "hand": self.hand,
            "deck": self.deck,
            "played": self.played,
            "duration": self.durationpile,
            "reserve": self.reserve,
            "exile": self.exilepile,
        }
        if not card:  # pragma: no cover
            return None
        card.player = self
        if isinstance(pile, PlayArea):
            card.location = pile.name
            pile.add(card)
            return card

        card.location = pile
        if pile in piles:
            piles[pile].add(card)
        elif pile == "topdeck":
            card.location = "deck"
            self.deck.addToTop(card)
        else:
            raise AssertionError(f"Adding card to unknown location: {pile}")
        return card

    ###########################################################################
    def discard_card(self, card, source=None, hook=True):
        """Discard a card"""
        assert isinstance(card, Card.Card)
        if card in self.hand:
            self.hand.remove(card)
        self.add_card(card, "discard")
        if hook:
            self.hook_discard_this_card(card, source)
            for way, crd in self.played_ways:
                if crd != card:
                    continue
                way.hook_way_discard_this_card(game=self.game, player=self, card=crd)

    ###########################################################################
    def discard_hand(self):
        # Activate hooks first so they can still access contents of the
        # players hand etc. before they get discarded
        for card in self.hand:
            self.hook_discard_this_card(card, "hand")
        for card in self.played:
            self.hook_discard_this_card(card, "played")
        for way, card in self.played_ways:
            way.hook_way_discard_this_card(game=self.game, player=self, card=card)
        while self.hand:
            card = self.hand.next_card()
            self.discard_card(card, "hand", hook=False)
        while self.played:
            card = self.played.next_card()
            self.discard_card(card, "played", hook=False)

    ###########################################################################
    def _playable_selection(self, index):
        options = []
        playable = [c for c in self.hand if c.playable and c.isAction()]
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
        nights = [c for c in self.hand if c.isNight()]
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
        spendable = [c for c in self.hand if c.isTreasure()]
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
            o = Option(selector="2", verb="Spend Coffer (1 coin)", card=None, action="coffer")
            options.append(o)

        if self.debt and self.coin:
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
        for c in self.played:
            if c.isAction():
                whens.append("postaction")
        if self.misc["is_start"]:
            whens.append("start")
        return whens

    ###########################################################################
    def _reserve_selection(self, index):
        whens = self._get_whens()
        options = []
        for card in self.reserve:
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
    def _landmark_selection(self, index):
        options = []
        for lm in self.game.landmarks.values():
            o = Option(
                selector="-",
                desc=lm.description(self),
                name=lm.name,
                card=lm,
                action=None,
                details="Landmark",
            )
            options.append(o)

        return options, index

    ###########################################################################
    def _project_selection(self, index):
        if not self.game.projects:
            return None, index
        # Can only have two projects
        if len(self.projects) == 2:
            return None, index
        options = []
        for op in self.game.projects.values():
            index += 1
            if (op.cost <= self.coin and self.buys) and (op not in self.projects):
                sel = chr(ord("a") + index)
                action = "project"
            else:
                sel = "-"
                action = None
            details = f"Project; {self.coststr(op)}"
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
        options = []
        for op in self.game.events.values():
            index += 1
            if op.cost <= self.coin and self.buys:
                sel = chr(ord("a") + index)
                action = "event"
            else:
                sel = "-"
                action = None
            details = f"Event; {self.coststr(op)}"
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
    def _get_all_purchasable(self):
        """Return all potentially purchasable cards"""
        all_cards = PlayArea("all_purchasable")
        for c in self.game.cardTypes():
            if not c.purchasable:
                continue
            all_cards.add(c)
        all_cards.sort(key=self.card_cost)
        all_cards.sort(key=lambda c: c.basecard)
        return all_cards

    ###########################################################################
    def _buyable_selection(self, index):
        options = []
        all_cards = self._get_all_purchasable()
        buyable = self.cards_under(coin=self.coin, num_potions=self.potions.get())
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
            details = [self.coststr(card)]
            if card.embargo_level:
                details.append(f"Embargo {card.embargo_level}")
            if card.getVP():
                details.append(f"Gathered {card.getVP()} VP")
            details.append(card.get_cardtype_repr())
            details.append(f"{len(card)} left")
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

        if self.phase == "action":
            if self.actions or self.villagers:
                op, index = self._playable_selection(index)
                options.extend(op)

        if self.phase == "buy":
            op = self._spendable_selection()
            options.extend(op)
            op, index = self._buyable_selection(index)
            options.extend(op)
            op, index = self._event_selection(index)
            options.extend(op)
            op, index = self._project_selection(index)
            if op:
                options.extend(op)

        if self.phase == "night":
            op, index = self._night_selection(index)
            options.extend(op)

        if self.reserve.size():
            op, index = self._reserve_selection(index)
            options.extend(op)

        op, index = self._landmark_selection(index)
        options.extend(op)

        prompt = self._generate_prompt()
        return options, prompt

    ###########################################################################
    def _generate_prompt(self) -> str:
        """Return the prompt to give to the user"""
        status = f"Actions={self.actions} Buys={self.buys}"
        if self.coin:
            status += f" Coins={self.coin}"
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
        self.output(f"{'#' * 20} Turn {self.turn_number} {'#' * 20}")
        stats = f"({self.get_score()} points, {self.count_cards()} cards)"
        if self.skip_turn:
            self.skip_turn = False
            return
        self.output(f"{self.name}'s Turn {stats}")
        self.action_phase()
        self.buy_phase()
        self.night_phase()
        self.cleanup_phase()
        self._check()

    ###########################################################################
    def _check(self):
        """For bug detection: Is everything where it should be?"""
        for stack_name, stack in self.stacklist:
            for card in stack:
                assert card.location == stack_name.lower(), f"{card} {stack_name=}"
                assert card.player == self, f"{card} {self}"

    ###########################################################################
    def night_phase(self):
        """Do the Night Phase"""
        nights = [_ for _ in self.hand if _.isNight()]
        if not nights:
            return
        self.output("************ Night Phase ************")
        self.phase = "night"
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
        self.phase = "action"
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
        self.phase = "buy"
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
        for card in self.projects:
            card.hook_end_buy_phase(game=self.game, player=self)

    ###########################################################################
    def cleanup_phase(self):
        # Save the cards we had so that the hook_end_turn has something to apply against
        self.had_cards = (
            self.played
            + self.reserve
            + self.played_events
            + self.game.landmarks
            + self.durationpile
        )
        self.phase = "cleanup"
        self.game.cleanup_boons()
        for card in self.played + self.reserve + self.artifacts:
            card.hook_cleanup(self.game, self)
        self.discard_hand()
        self.pick_up_hand()
        self.hooks = {}
        self.misc["cleaned"] = True

    ###########################################################################
    def payback(self):
        payback = min(self.coin, self.debt.get())
        self.output("Paying back {payback}%d debt")
        self.coin -= payback
        self.debt -= payback

    ###########################################################################
    def _perform_action(self, opt):
        if opt["action"] == "buy":
            self.buy_card(opt["card"])
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
            print("ERROR: Unhandled action {opt['action']}", file=sys.stderr)
            sys.exit(1)
        self.misc["is_start"] = False

    ###########################################################################
    def _display_overview(self):  # pylint: disable=too-many-branches
        self.output("-" * 50)
        tknoutput = []
        for tkn in self.tokens:
            if self.tokens[tkn]:
                tknoutput.append(f"{tkn}: {self.tokens[tkn]}")
        if self.card_token:
            tknoutput.append("-1 Card")
        if self.coin_token:
            tknoutput.append("-1 Coin")
        if self.journey_token:
            tknoutput.append("Journey Faceup")
        else:
            tknoutput.append("Journey Facedown")
        self.output(f"| Phase: {self.phase}")
        self.output(f"| Tokens: {'; '.join(tknoutput)}")
        if self.deferpile:
            self.output(f"| Defer: {', '.join([_.name for _ in self.deferpile])}")
        if self.durationpile:
            self.output("| Duration: %s" % ", ".join([c.name for c in self.durationpile]))
        if self.projects:
            self.output(f"| Project: {', '.join([p.name for p in self.projects])}")
        if self.reserve:
            self.output("| Reserve: %s" % ", ".join([c.name for c in self.reserve]))
        if self.hand:
            self.output("| Hand: %s" % ", ".join([c.name for c in self.hand]))
        else:
            self.output("| Hand: <EMPTY>")
        if self.artifacts:
            self.output(f"| Artifacts: {', '.join([_.name for _ in self.artifacts])}")
        if self.exilepile:
            self.output("| Exile: %s" % ", ".join([c.name for c in self.exilepile]))
        if self.played:
            self.output(f"| Played: {', '.join([_.name for _ in self.played])}")
        else:
            self.output("| Played: <NONE>")
        self.output(f"| Deck Size: {len(self.deck)}")
        if self.game.ally:
            self.output("| Ally: %s: %s" % (self.game.ally.name, self.game.ally.description(self)))
        self.output("| Discard: %s" % ", ".join([c.name for c in self.discardpile]))  # Debug
        self.output(f"| Trash: {', '.join([_.name for _ in self.game.trashpile])}")  # Debug
        self.output(f"| {self.discardpile.size()} cards in discard pile")
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
        x += self.discardpile
        x += self.hand
        x += self.deck
        x += self.played
        x += self.durationpile
        x += self.deferpile
        x += self.reserve
        x += self.exilepile
        return x

    ###########################################################################
    def get_score_details(self, verbose=False):
        scr = {}
        for c in self.all_cards():
            scr[c.name] = scr.get(c.name, 0) + c.victory
            scr[c.name] = scr.get(c.name, 0) + c.special_score(self.game, self)
        for s in self.states:
            scr[s.name] = scr.get(s.name, 0) + s.victory
        if self.game.ally:
            scr[self.game.ally.name] = self.game.ally.special_score(self.game, self)
        scr.update(self.score)
        return scr

    ###########################################################################
    def get_score(self, verbose=False):
        scr = self.get_score_details(verbose)
        vp = sum(scr.values())
        if verbose:
            self.game.output(f"{self.name}: {scr}")
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
        self.phase = "start"
        self.played.empty()
        self.buys = 1
        self.actions = 1
        self.coin = 0
        self.potions.set(0)
        self.played_ways = []
        self.misc = {"is_start": True, "cleaned": False}
        self.stats = {"gained": [], "bought": [], "trashed": []}
        self._display_overview()
        self.hook_start_turn()
        self._duration_start_turn()
        for card in self.deferpile:
            self.output(f"Playing deferred {card.name}")
            self.currcards.append(card)
            self.deferpile.remove(card)
            self.hand.add(card)
            self.play_card(card, costAction=False)
            self.currcards.pop()

    ###########################################################################
    def _duration_start_turn(self):
        """Perform the duration pile at the start of the turn"""
        for card in self.durationpile:
            options = {"dest": "played"}
            self.output(f"Playing {card.name} from duration pile")
            self.currcards.append(card)
            upd_opts = card.duration(game=self.game, player=self)
            if isinstance(upd_opts, dict):
                options.update(upd_opts)
            self.currcards.pop()
            if not card.permanent:
                # Handle case where cards move themselves elsewhere
                if card.location != "duration":
                    continue
                self.add_card(card, options["dest"])
                self.durationpile.remove(card)

    ###########################################################################
    def hook_start_turn(self):
        for c in self.hand + self.states + self.projects + self.artifacts:
            c.hook_start_turn(self.game, self)
        if self.game.ally:
            self.game.ally.hook_start_turn(self.game, self)

    ###########################################################################
    def spend_coffer(self):
        if self.coffers.get() <= 0:
            return
        self.coffers -= 1
        self.coin += 1
        self.output("Spent a coffer")

    ###########################################################################
    def spend_villager(self):
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
            card = self.game[card].remove()
        self.move_card(card, "exile")
        # self.exilepile.add(card)

    ###########################################################################
    def end_turn(self):
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
        self.phase = None
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
        for c in self.played:
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
        for card in self.hand:
            if card.isTreasure():
                self.play_card(card)

    ###########################################################################
    def _play_card_tokens(self, card):
        tkns = self.which_token(card.name)
        if "+1 Action" in tkns:
            self.output("Gaining action from +1 Action token")
            self.add_actions(1)
        if "+1 Card" in tkns:
            c = self.pickup_card()
            self.output("Picked up %s from +1 Card token" % c.name)
        if "+1 Coin" in tkns:
            self.output("Gaining coin from +1 Coin token")
            self.coin += 1
        if "+1 Buy" in tkns:
            self.output("Gaining buy from +1 Buy token")
            self.buys += 1

    ###########################################################################
    def hook_all_players_pre_action(self, card):
        options = {}
        for player in self.game.player_list():
            for crd in player.durationpile:
                ans = crd.hook_all_players_pre_action(
                    game=self.game, player=self, owner=player, card=card
                )
                if ans:
                    options.update(ans)
        return options

    ###########################################################################
    def defer_card(self, card):
        """Set a non-duration card to be played in its entirety next turn"""
        self.deferpile.add(card)
        if self.played[card.name]:
            self.played.remove(card)

    ###########################################################################
    def _move_after_play(self, card: Card) -> None:
        """Move the card to its next location after it has been played"""
        if card.isDuration():
            self.move_card(card, "duration")
        elif card.isReserve():
            self.move_card(card, "reserve")
        else:
            self.move_card(card, "played")

    ###########################################################################
    def play_card(
        self,
        card: Card,
        discard: bool = True,
        costAction: bool = True,
        postActionHook: bool = True,
    ) -> None:
        """Play the card {card}"""
        options = {"skip_card": False, "discard": discard}
        if card not in self.hand and options["discard"]:
            raise AssertionError(f"Playing {card.name} which is not in hand")
        if self.playlimit is not None:
            if self.playlimit <= 0:
                self.output(f"Can't play {card.name} due to limits in number of plays")
                return
            self.playlimit -= 1
        self.output(f"Playing {card.name}")
        self.currcards.append(card)
        if card.isAction():
            options.update(self.hook_all_players_pre_action(card))

        self._play_card_tokens(card)

        if card.isAction() and costAction and self.phase != "night":
            self.actions -= 1
        if self.actions < 0:  # pragma: no cover
            self.actions = 0
            self.currcards.pop()
            self.output("Not enough actions")
            return

        if options["discard"]:
            self._move_after_play(card)

        if not options["skip_card"]:
            self.card_benefits(card)
        self.currcards.pop()
        if postActionHook and card.isAction():
            for crd in self.relevant_cards():
                if hasattr(crd, "hook_post_action"):
                    crd.hook_post_action(game=self.game, player=self, card=card)

    ###########################################################################
    def perform_way(self, way, card):
        """Perform a way"""
        opts = {"discard": True}
        self.currcards.append(way)
        self.actions -= 1
        if self.actions < 0:  # pragma: no cover
            self.actions = 0
            self.currcards.pop()
            self.output("Not enough actions")
            return
        self.hand.remove(card)
        self.output(f"Playing {card.name} through {way.name}")
        self.card_benefits(way)
        newopts = way.special_way(game=self.game, player=self, card=card)
        if isinstance(newopts, dict):
            opts.update(newopts)
        if opts["discard"]:
            self.add_card(card, "played")
        self.played_ways.append((way, card))
        self.currcards.pop()

    ###########################################################################
    def card_benefits(self, card):
        """Gain the benefits of the card being played - including special()"""
        self.add_actions(card.actions)
        self.coin += self.hook_spend_value(card, actual=True)
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

        if self.phase == "night":
            card.night(game=self.game, player=self)
        else:
            card.special(game=self.game, player=self)

    ###########################################################################
    def card_cost(self, card):
        assert isinstance(card, (Card.Card, CardPile, EventPile, ProjectPile))
        cost = card.cost
        if "-Cost" in self.which_token(card.name):
            cost -= 2
        for crd in self.relevant_cards():
            cost += crd.hook_card_cost(game=self.game, player=self, card=card)
        cost += card.hook_this_card_cost(game=self.game, player=self)
        return max(0, cost)

    ###########################################################################
    def gain_card(self, cardpile=None, destination="discard", newcard=None, callhook=True):
        """Add a new card to the players set of cards from a cardpile"""
        # Options:
        #   dontadd: True - adding card handled elsewhere
        #   replace: <newcard> - Replace the gained card with <newcard>
        #   destination: <dest> - Move the new card to <dest> rather than discardpile
        #   trash: True - trash the new card
        #   shuffle: True - shuffle the deck after gaining new card
        options = {}
        if not newcard:
            if isinstance(cardpile, str):
                newcard = self.game[cardpile].remove()
            else:
                newcard = cardpile.remove()

        if not newcard:
            self.output(f"No more {cardpile}")
            return None
        self.output(f"Gained a {newcard.name}")
        newcard.player = self
        if callhook:
            if rc := self.hook_gain_card(newcard):
                options.update(rc)
            if rc := newcard.hook_gain_this_card(game=self.game, player=self):
                options.update(rc)

        # check for un-exiling
        if self.exilepile[newcard.name]:
            self.check_unexile(newcard.name)

        # Replace is to gain a different card
        if options.get("replace"):
            self.game[newcard.name].add(newcard)
            newcard = self.game[options["replace"]].remove()
            if not newcard:
                self.output(f"No more {options['replace']}")
            else:
                newcard.player = self
        self.stats["gained"].append(newcard)
        destination = options.get("destination", destination)
        if callhook:
            self.hook_allplayers_gain_card(newcard)
        if options.get("trash", False):
            self.trash_card(newcard)
            return newcard
        if not options.get("dontadd", False):
            self.add_card(newcard, destination)
        if options.get("shuffle", False):
            self.deck.shuffle()
        return newcard

    ###########################################################################
    def check_unexile(self, cardname):
        """Give players option to un-exile card"""
        num = sum(1 for _ in self.exilepile if _.name == cardname)
        choices = [
            (f"Unexile {num} x {cardname}", True),
            ("Do nothing", False),
        ]
        unex = self.plr_choose_options(f"Un-exile {cardname}", *choices)
        if unex:
            self.unexile(cardname)

    ###########################################################################
    def unexile(self, cardname: str) -> int:
        """Un-exile cards
        Return number unexiled"""
        count = 0
        if not self.exilepile:
            return 0
        for card in self.exilepile:
            if card is None:
                break
            if card.name == cardname:
                self.move_card(card, "discard")
                count += 1
        return count

    ###########################################################################
    def overpay(self, card):
        options = []
        for i in range(self.coin + 1):
            options.append(("Spend %d more" % i, i))
        ans = self.plr_choose_options("How much do you wish to overpay?", *options)
        card.hook_overpay(game=self.game, player=self, amount=ans)
        self.coin -= ans

    ###########################################################################
    def buy_card(self, card):
        assert isinstance(card, CardPile)
        if not self.buys:  # pragma: no cover
            return
        if self.debt:
            self.output("Must pay off debt first")
            return
        self.buys -= 1
        cost = self.card_cost(card)
        if card.isDebt():
            self.debt += card.debtcost
        if self.coin < cost:
            self.output("You can't afford this")
            return
        self.coin -= cost
        if card.overpay and self.coin:
            self.overpay(card)
        newcard = self.gain_card(card)
        if card.embargo_level:
            for _ in range(card.embargo_level):
                self.gain_card("Curse")
                self.output("Gained a Curse from embargo")
        self.stats["bought"].append(newcard)
        self.output(f"Bought {newcard.name} for {cost} coin")
        if "Trashing" in self.which_token(card.name):
            self.output("Trashing token allows you to trash a card")
            self.plr_trash_card()
        self.hook_buy_card(newcard)
        newcard.hook_buy_this_card(game=self.game, player=self)
        self.hook_all_players_buy_card(newcard)

    ###########################################################################
    def hook_all_players_buy_card(self, card):
        for player in self.game.player_list():
            for crd in player.durationpile:
                crd.hook_all_players_buy_card(game=self.game, player=self, owner=player, card=card)
        for crd in self.game.landmarks.values():
            crd.hook_all_players_buy_card(game=self.game, player=self, owner=self, card=card)

    ###########################################################################
    def hook_allplayers_gain_card(self, card):
        for player in self.game.player_list():
            for crd in player.relevant_cards():
                crd.hook_allplayers_gain_card(game=self.game, player=self, owner=player, card=card)

    ###########################################################################
    def add_hook(self, hook_name, hook):
        self.hooks[hook_name] = hook

    ###########################################################################
    def relevant_cards(self):
        """Return a list of all cards whos hooks we should look at"""
        return (
            self.hand
            + self.played
            + self.durationpile
            + self.reserve
            + self.game.landmarks
            + self.projects
            + self.game.ways
            + self.played_events
            + self.states
            + self.artifacts
            + self.game.ally
        )

    ###########################################################################
    def hook_gain_card(self, card):
        """Hook which is fired by a card being obtained by a player"""
        assert isinstance(card, Card.Card)
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
        for crd in self.hand:
            if crd.has_defense():
                if verbose:
                    attacker.output(f"Player {self.name} is defended")
                return True
        return False

    ###########################################################################
    def get_coins(self) -> int:
        """Return the number of coins the player has"""
        return self.coin

    ###########################################################################
    def add_coins(self, num=1):
        assert isinstance(num, int)
        self.coin += num

    ###########################################################################
    def set_coins(self, num=1):
        assert isinstance(num, int)
        self.coin = num

    ###########################################################################
    def get_actions(self):
        return self.actions

    ###########################################################################
    def set_actions(self, num=1):
        self.actions = num

    ###########################################################################
    def add_actions(self, num=1):
        assert isinstance(num, int)
        if self.misc.get("no_actions"):
            self.output("No more additional actions allowed")
        else:
            self.actions += num

    ###########################################################################
    def get_buys(self):
        return self.buys

    ###########################################################################
    def add_buys(self, num=1):
        assert isinstance(num, int)
        self.buys += num

    ###########################################################################
    def set_buys(self, num=1):
        assert isinstance(num, int)
        self.buys = num

    ###########################################################################
    def gain_prize(self):
        prizes = [self.game[c] for c in self.game.getPrizes()]
        available = [cp for cp in prizes if not cp.is_empty()]
        if available:
            self.output("Gain a prize")
            card = self.card_sel(cardsrc=available)
            self.add_card(card[0].remove())
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
        if self.coin < project.cost:
            self.output(f"Need {project.cost} coins to buy this project")
            return False
        self.buys -= 1
        self.coin -= project.cost
        self.debt += project.debtcost
        self.buys += project.buys
        self.assign_project(project.name)
        return True

    ###########################################################################
    def perform_event(self, evnt: EventPile) -> bool:
        """Perform an event"""
        try:
            assert isinstance(evnt, EventPile)
        except AssertionError:
            print("Event={evnt} ({type(evnt)})")
            raise

        if not self.buys:
            self.output("Need a buy to perform an event")
            return False
        if self.debt != 0:
            self.output("Must pay off debt first")
        if self.coin < evnt.cost:
            self.output(f"Need {evnt.cost} coins to perform this event")
            return False
        self.buys -= 1
        self.coin -= evnt.cost
        self.debt += evnt.debtcost
        self.buys += evnt.buys
        self.output(f"Using event {evnt}")
        self.currcards.append(evnt)
        evnt.special(game=self.game, player=self)
        self.currcards.pop()
        self.played_events.add(evnt)
        return True

    ###########################################################################
    @classmethod
    def select_by_type(cls, card, types):
        if card.isAction() and not types[Card.TYPE_ACTION]:
            return False
        if card.isVictory() and not types[Card.TYPE_VICTORY]:
            return False
        if card.isTreasure() and not types[Card.TYPE_TREASURE]:
            return False
        if card.isNight() and not types[Card.TYPE_NIGHT]:
            return False
        return True

    ###########################################################################
    def cards_affordable(self, oper, coin, num_potions, types):
        """Return the list of cards for under cost
        {coin} {num_potions} are the resources contraints we have
        """
        affordable = PlayArea("affordable")
        for c in self.game.cardTypes():
            if not c:
                continue
            cost = self.card_cost(c)
            if not self.select_by_type(c, types):
                continue
            if not c.purchasable:
                continue
            if c.always_buyable:
                affordable.add(c)
                continue
            if c.always_buyable:
                affordable.add(c)
                continue
            if coin is None:
                affordable.add(c)
                continue
            if c.debtcost and not c.cost:
                affordable.add(c)
                continue
            if oper(cost, coin) and oper(c.potcost, num_potions):
                affordable.add(c)
                continue
        affordable.sort(key=self.card_cost)
        affordable.sort(key=lambda c: c.basecard)
        return affordable

    ###########################################################################
    def cards_under(self, coin, num_potions=0, types=None):
        """Return the list of cards for under cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.le, coin, num_potions, types)

    ###########################################################################
    def cards_worth(self, coin, num_potions=0, types=None):
        """Return the list of cards that are exactly cost"""
        if types is None:
            types = {}
        types = self._type_selector(types)
        return self.cards_affordable(operator.eq, coin, num_potions, types)

    ###########################################################################
    def get_cards(self):
        """Return a list of all teh cards owned"""
        cards = defaultdict(int)
        for _, stack in self.stacklist:
            for card in stack:
                cards[card.name] += 1
        return cards

    ###########################################################################
    def count_cards(self):
        """How many cards does the player have"""
        count = {}
        for name, stack in self.stacklist:
            count[name] = len(stack)
        total = sum(count.values())
        total += self.secret_count
        return total

    ###########################################################################
    @classmethod
    def _type_selector(cls, types=None):
        if types is None:
            types = {}
        assert set(types.keys()) <= set(
            [Card.TYPE_ACTION, Card.TYPE_VICTORY, Card.TYPE_TREASURE, Card.TYPE_NIGHT]
        )
        if not types:
            return {
                Card.TYPE_ACTION: True,
                Card.TYPE_VICTORY: True,
                Card.TYPE_TREASURE: True,
                Card.TYPE_NIGHT: True,
            }
        _types = {
            Card.TYPE_ACTION: False,
            Card.TYPE_VICTORY: False,
            Card.TYPE_TREASURE: False,
            Card.TYPE_NIGHT: False,
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
            for crd in plr.hand:
                crd.hook_underAttack(game=self.game, player=plr, attacker=self)
            if plr.has_defense(self):
                continue
            victims.append(plr)
        return victims

    ###########################################################################
    def coststr(self, card) -> str:
        """Generate the string showing the cost of the card"""
        cost = []
        cost.append(f"{self.card_cost(card)} Coins")
        if card.debtcost:
            cost.append(f"{card.debtcost} Debt")
        if card.potcost:
            cost.append("Potion")
        if card.overpay:
            cost.append("Overpay")
        cststr = ", ".join(cost)
        return cststr.strip()

    ###########################################################################
    def plr_trash_card(self, num=1, anynum=False, cardsrc="hand", **kwargs):
        """Ask player to trash num cards"""
        if "prompt" not in kwargs:
            if anynum:
                kwargs["prompt"] = "Trash any cards"
            else:
                kwargs["prompt"] = f"Trash {num} cards"
        if len(cardsrc) == 0:
            return None
        if len(cardsrc) == 0:
            self.output("No cards to trash")
            return None
        trash = self.card_sel(
            num=num,
            cardsrc=cardsrc,
            anynum=anynum,
            verbs=("Trash", "Untrash"),
            **kwargs,
        )
        for crd in trash:
            self.trash_card(crd, **kwargs)
        return trash

    ###########################################################################
    def plr_gain_card(
        self,
        cost,
        modifier="less",
        types=None,
        recipient=None,
        force=False,
        destination="discard",
        **kwargs,
    ):
        """Gain a card up to cost coin
        if recipient defined then that player gets the card"""
        if types is None:
            types = {}
        assert modifier in ("less", "equal")
        if recipient is None:
            recipient = self
        prompt = "Gain a card "
        types = self._type_selector(types)
        if modifier == "less":
            if cost:
                prompt += f"costing up to {cost}"
            buyable = self.cards_under(cost, types=types)
        elif modifier == "equal":
            if cost:
                prompt += f"costing exactly {cost}"
            buyable = self.cards_worth(cost, types=types)
        buyable = [_ for _ in buyable if _.purchasable]
        buyable = [_ for _ in buyable if not _.debtcost]
        buyable = [_ for _ in buyable if _.name not in kwargs.get("exclude", [])]
        if "prompt" not in kwargs:
            kwargs["prompt"] = prompt
        cards = self.card_sel(
            cardsrc=buyable,
            recipient=recipient,
            verbs=("Get", "Unget"),
            force=force,
            **kwargs,
        )
        if cards:
            cardpile = cards[0]
            newcard = recipient.gain_card(cardpile, destination)
            recipient.output(f"Got a {newcard.name}")
            return newcard
        return None

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
        statecard = self.game.states[state]

        if statecard.unique_state:
            for pl in self.game.player_list():
                for st in pl.states[:]:
                    if st.name == state:
                        pl.states.remove(st)
                        break
        self.states.append(statecard)

    ###########################################################################
    def assign_artifact(self, artifact):
        assert isinstance(artifact, str)
        artifactcard = self.game.artifacts[artifact]
        # Remove artifact from whoever currently has it
        for pl in self.game.player_list():
            for st in pl.artifacts[:]:
                if st.name == artifact and self != pl:
                    pl.output(f"{self.name} took your {artifact}")
                    pl.artifacts.remove(st)
                    break
        # If we already have it don't get it again
        if artifactcard not in self.artifacts:
            self.artifacts.append(artifactcard)

    ###########################################################################
    def assign_project(self, project):
        assert isinstance(project, str)
        projectcard = self.game.projects[project]
        if len(self.projects) == 2:
            self.output("Can't have more than two projects")
            return False
        if project in [_.name for _ in self.projects]:
            self.output(f"Already have project {project}")
            return False
        self.projects.append(projectcard)
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
    def plr_discard_cards(self, num=1, anynum=False, **kwargs):
        """Get the player to discard exactly num cards"""
        if "prompt" not in kwargs:
            if anynum:
                kwargs["prompt"] = "Discard any number of cards"
            else:
                kwargs["prompt"] = f"Discard {num} cards"
        discard = self.card_sel(num=num, anynum=anynum, verbs=("Discard", "Undiscard"), **kwargs)
        for c in discard:
            self.output(f"Discarding {c.name}")
            self.discard_card(c)
        return discard

    ###########################################################################
    def plr_discard_down_to(self, num):
        """Get the player to discard down to num cards in their hand"""
        numtogo = len(self.hand) - num
        if numtogo <= 0:
            return
        self.plr_discard_cards(numtogo, force=True)

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
