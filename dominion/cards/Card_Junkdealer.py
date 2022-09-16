#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Junkdealer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "+1 card, +1 action, +1 coin, trash a card"
        self.name = "Junk Dealer"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 2

    def special(self, game, player):
        player.plr_trash_card(force=True)


###############################################################################
class Test_Junkdealer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Junk Dealer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.jd = self.g["Junk Dealer"].remove()
        self.plr.hand.set("Copper", "Silver", "Silver", "Gold")
        self.plr.deck.set("Estate", "Province", "Duchy")
        self.plr.add_card(self.jd, "hand")

    def test_trash(self):
        tsize = self.g.trashpile.size()
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.play_card(self.jd)
        self.assertEqual(self.plr.hand.size(), 4)
        self.assertEqual(self.g.trashpile.size(), tsize + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
