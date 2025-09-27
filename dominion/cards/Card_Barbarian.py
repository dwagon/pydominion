#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Barbarian"""

import unittest
from typing import Optional

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Barbarian(Card.Card):
    """Barbarian"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.ALLIES
        self.desc = """+$2; Each other player trashes the top card of their deck.
            If it costs $3 or more they gain a cheaper card sharing a type with it;
            otherwise they gain a Curse."""
        self.name = "Barbarian"
        self.coin = 2
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in player.attack_victims():
            _barbarian_attack(game, attacker=player, victim=plr)


###############################################################################
def _barbarian_attack(game: Game.Game, attacker: Player.Player, victim: Player.Player) -> None:
    """Do the barbarian attack"""
    victim_card = _barbarian_trash(victim, attacker)
    if victim_card is None:
        return
    if cards := _available_cards(game, victim_card):
        if gained := victim.card_sel(prompt="Gain a cheaper card", cardsrc=cards):
            if isinstance(gained[0], str):
                card_name = gained[0]
            else:
                card_name = gained[0].name
            try:
                victim.gain_card(card_name, Piles.DISCARD)
            except NoCardException:
                victim.output(f"No more {gained[0]}")
    else:
        victim.output("No suitable cards")


###############################################################################
def _available_cards(game: Game.Game, victim_card: Card.Card) -> list[Card.Card]:
    """Return all cheaper cards sharing a type with the victims card"""
    cards = []
    for name, _ in game.get_card_piles():
        check_card = game.card_instances[name]
        if _card_types(check_card).intersection(_card_types(victim_card)):
            if check_card.cost < victim_card.cost:
                cards.append(check_card)
    return cards


###############################################################################
def _barbarian_trash(victim: Player.Player, attacker: Player.Player) -> Optional[Card.Card]:
    try:
        victim_card = victim.top_card()
    except NoCardException:
        return None
    victim.output(f"{attacker}'s Barbarian: Trashes your {victim_card}")
    victim.trash_card(victim_card)
    if victim_card.cost < 3:
        try:
            victim.gain_card("Curse")
        except NoCardException:
            attacker.output("No more Curses")
        return None
    return victim_card


###############################################################################
def _card_types(card: Card.Card) -> set[Card.CardType]:
    """Return a set of the cards card types"""
    if isinstance(card.cardtype, list):
        return set(card.cardtype)
    return {card.cardtype}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover pylint: disable=unused-argument
    """If we need to pick up cards - pick up the best"""
    picked = []
    for card in kwargs["cardsrc"]:
        if card.name == "Province":
            picked.append((6, "Province"))
        elif card.name == "Gold":
            picked.append((5, "Gold"))
        elif card.name == "Duchy":
            picked.append((4, "Duchy"))
        elif card.name == "Silver":
            picked.append((3, "Silver"))
        elif card.name == "Estate":
            picked.append((2, "Estate"))
        elif card.name == "Copper":
            picked.append((1, "Copper"))
    picked.sort()
    return [picked[-1][1]]


###############################################################################
class TestBarbarian(unittest.TestCase):
    """Test Barbarian"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Barbarian"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Barbarian")
        self.attacker.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Test against a low-cost victim card"""
        self.victim.piles[Piles.DECK].set("Estate", "Copper")
        self.attacker.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Curse", self.victim.piles[Piles.DISCARD])

    def test_expense(self) -> None:
        """Test trashing an expensive card"""
        self.victim.piles[Piles.DECK].set("Estate", "Province")
        self.victim.test_input = ["Select Duchy"]
        self.attacker.play_card(self.card)
        self.assertIn("Province", self.g.trash_pile)
        self.assertNotIn("Curse", self.victim.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.victim.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
