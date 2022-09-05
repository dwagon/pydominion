#!/usr/bin/env python

import unittest
from dominion import Card, Game


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
        prov = player.hand["Province"]
        if prov:
            player.reveal_card(prov)
            player.gain_card("Gold", destination="hand")
        else:
            player.gain_card("Silver", destination="hand")


###############################################################################
class Test_Explorer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Explorer"], oldcards=True)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Explorer"].remove()
        self.plr.add_card(self.card, "hand")

    def test_province(self):
        self.plr.gain_card("Province", "hand")
        self.plr.play_card(self.card)
        self.assertIn("Gold", self.plr.hand)
        # 5 + province + gold
        self.assertEqual(self.plr.hand.size(), 7)

    def test_no_province(self):
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.hand)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
