#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Patrician(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.desc = "+1 Card, +1 Action. Reveal the top card of your deck. If it costs 5 or more, put it into your hand."
        self.name = "Patrician"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    ###########################################################################
    def special(self, game, player):
        topcard = player.nextCard()
        player.revealCard(topcard)
        if topcard.cost >= 5:
            player.addCard(topcard, "hand")
            player.output("Adding %s to hand" % topcard.name)
        else:
            player.addCard(topcard, "topdeck")
            player.output("%s too cheap to bother with" % topcard.name)


###############################################################################
class Test_Patrician(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Patrician"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Patrician"].remove()

    def test_play_cheap(self):
        """Play the Patrician"""
        self.plr.setDeck("Estate", "Estate")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_play_good(self):
        """Play the Patrician"""
        self.plr.setDeck("Gold", "Estate")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 7)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_hand("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
