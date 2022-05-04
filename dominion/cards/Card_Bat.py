#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT]
        self.base = Game.NOCTURNE
        self.desc = "Trash up to 2 cards from your hand. If you trashed at least one, exchange this for a Vampire."
        self.name = "Bat"
        self.cost = 2
        self.insupply = False
        self.purchasable = False

    def night(self, game, player):
        tr = player.plr_trash_card(num=2)
        if tr:
            player.replace_card(self, "Vampire")


###############################################################################
class Test_Bat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Vampire"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Bat"].remove()

    def test_play(self):
        self.plr.phase = Card.TYPE_NIGHT
        self.plr.set_hand("Duchy", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Silver", "Trash Gold", "Finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Bat", self.plr.discardpile)
        self.assertIn("Vampire", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
