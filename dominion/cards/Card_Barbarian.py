#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
###############################################################################
class Card_Barbarian(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK]
        self.base = Game.ALLIES
        self.desc = """+$2; Each other player trashes the top card of their deck.
            If it costs $3 or more they gain a cheaper card sharing a type with it;
            otherwise they gain a Curse."""
        self.name = "Barbarian"
        self.coin = 2
        self.cost = 5
        self.required_cards = ["Curse"]

    def special(self, game, player):
        for plr in player.attack_victims():
            crd = plr.next_card()
            plr.output(f"{player.name}'s Barbarian: Trashes your {crd.name}")
            plr.trash_card(crd)
            if crd.cost < 3:
                plr.gain_card("Curse")
                return
            cards = []
            for cp in game.cardTypes():
                if set(cp.cardtype).intersection(set(crd.cardtype)):
                    if cp.cost < crd.cost:
                        cards.append(cp)
            gained = plr.card_sel(prompt="Gain a cheaper card", cardsrc=cards)
            plr.gain_card(gained[0], "discard")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    """ If we need to pick up cards - pick up the best """
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
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Barbarian"])
        self.g.start_game()
        self.attacker, self.victim = self.g.player_list()
        self.card = self.g["Barbarian"].remove()
        self.attacker.add_card(self.card, "hand")

    def test_play(self):
        """Test against a low cost victim card"""
        self.victim.set_deck("Copper")
        self.attacker.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIn("Curse", self.victim.discardpile)

    def test_expense(self):
        """Test trashing an expensive card"""
        self.victim.set_deck("Province")
        self.victim.test_input = ["Select Gold"]
        self.attacker.play_card(self.card)
        self.assertIsNotNone(self.g.in_trash("Province"))
        self.assertNotIn("Curse", self.victim.discardpile)
        self.assertIn("Gold", self.victim.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
