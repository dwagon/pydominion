#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


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
class Test_ActingTroupe(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Acting Troupe"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.card = self.g["Acting Troupe"].remove()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertLessEqual(self.plr.villagers.get(), 4)
        self.assertIn("Acting Troupe", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
