#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Barbarian """

import unittest
from dominion import Card, Game


###############################################################################
###############################################################################
class Card_Barbarian(Card.Card):
    """Barbarian"""

    def __init__(self):
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

    def special(self, game, player):
        for plr in player.attack_victims():
            self._barbarian_attack(game, attacker=player, victim=plr)

    def _barbarian_attack(self, game, attacker, victim):
        """Do the barbarian attack"""
        crd = victim.top_card()
        victim.output(f"{attacker.name}'s Barbarian: Trashes your {crd.name}")
        victim.trash_card(crd)
        if crd.cost < 3:
            victim.gain_card("Curse")
            return
        cards = []
        for cp in game.cardTypes():
            if self._cardtypes(cp).intersection(self._cardtypes(crd)):
                if cp.cost < crd.cost:
                    cards.append(cp)
        if cards:
            gained = victim.card_sel(prompt="Gain a cheaper card", cardsrc=cards)
            victim.gain_card(gained[0], "discard")
        else:
            victim.output("No suitable cards")

    def _cardtypes(self, crd):
        """Return a set of the cards cartypes"""
        if isinstance(crd.cardtype, list):
            return set(crd.cardtype)
        return set([crd.cardtype])


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
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
class Test_Barbarian(unittest.TestCase):
    """Test Barbarian"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Barbarian"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g["Barbarian"].remove()
        self.attacker.add_card(self.card, "hand")

    def Xtest_play(self):
        """Test against a low cost victim card"""
        self.victim.deck.set("Estate", "Copper")
        self.attacker.play_card(self.card)
        self.assertIn("Copper", self.g.trashpile)
        self.assertIn("Curse", self.victim.discardpile)

    def test_expense(self):
        """Test trashing an expensive card"""
        self.victim.deck.set("Estate", "Province")
        self.victim.test_input = ["Select Duchy"]
        self.attacker.play_card(self.card)
        self.assertIn("Province", self.g.trashpile)
        self.assertNotIn("Curse", self.victim.discardpile)
        self.assertIn("Duchy", self.victim.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
