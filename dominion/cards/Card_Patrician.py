#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Patrician(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1 Card, +1 Action. Reveal the top card of your deck. If it costs 5 or more, put it into your hand."
        self.name = "Patrician"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        topcard = player.next_card()
        player.reveal_card(topcard)
        if topcard.cost >= 5:
            player.add_card(topcard, "hand")
            player.output("Adding %s to hand" % topcard.name)
        else:
            player.add_card(topcard, "topdeck")
            player.output("%s too cheap to bother with" % topcard.name)


###############################################################################
class Test_Patrician(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Patrician"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Patrician"].remove()

    def test_play_cheap(self):
        """Play the Patrician"""
        self.plr.deck.set("Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_play_good(self):
        """Play the Patrician"""
        self.plr.deck.set("Gold", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Gold", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
