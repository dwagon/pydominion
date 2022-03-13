#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Junkdealer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = "+1 card, +1 action, +1 coin, trash a card"
        self.name = "Junk Dealer"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 2

    def special(self, game, player):
        player.plrTrashCard(force=True)


###############################################################################
class Test_Junkdealer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Junk Dealer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.jd = self.g["Junk Dealer"].remove()
        self.plr.set_hand("Copper", "Silver", "Silver", "Gold")
        self.plr.set_deck("Estate", "Province", "Duchy")
        self.plr.add_card(self.jd, "hand")

    def test_trash(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.playCard(self.jd)
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertEqual(self.g.trashSize(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
