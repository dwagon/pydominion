#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_ActingTroupe(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Acting Troupe"
        self.desc = "+4 Villagers. Trash this."
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        player.villagers += 4
        player.trash_card(self)


###############################################################################
class TestActingTroupe(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Acting Troupe"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self):
        self.card = self.g.get_card_from_pile("Acting Troupe")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertLessEqual(self.plr.villagers.get(), 4)
        self.assertIn("Acting Troupe", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
