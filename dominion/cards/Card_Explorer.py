#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Explorer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.desc = """You may reveal a Province from your hand. If you do,
            gain a Gold to your hand. If you don't, gain a Silver to your hand."""
        self.name = "Explorer"
        self.base = Game.SEASIDE
        self.cost = 5

    def special(self, game, player):
        prov = player.in_hand("Province")
        if prov:
            player.revealCard(prov)
            player.output("Gained a Gold")
            player.gainCard("Gold", destination="hand")
        else:
            player.output("Gained a Silver")
            player.gainCard("Silver", destination="hand")


###############################################################################
class Test_Explorer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Explorer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Explorer"].remove()
        self.plr.addCard(self.card, "hand")

    def test_province(self):
        self.plr.gainCard("Province", "hand")
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.in_hand("Gold"))
        # 5 + province + gold
        self.assertEqual(self.plr.hand.size(), 7)

    def test_no_province(self):
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.in_hand("Silver"))
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
