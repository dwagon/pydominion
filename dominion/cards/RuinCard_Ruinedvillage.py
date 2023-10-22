#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Ruined_Village """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_RuinedVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Ruined Village"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action"
        self.actions = 1
        self.pile = "Ruins"


###############################################################################
class TestRuinedVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Ruins")
            if self.card.name == "Ruined Village":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a ruined village"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
