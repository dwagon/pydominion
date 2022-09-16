#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_FaithfulHound(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+2 Cards; When you discard this other than during Clean-up,
            you may set it aside, and put it into your hand at end of turn."""
        self.name = "Faithful Hound"
        self.cards = 2
        self.cost = 2

    def hook_discard_this_card(self, game, player, source):
        if player.phase != "cleanup":
            player.add_card(self, "hand")


###############################################################################
class Test_FaithfulHound(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Faithful Hound"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.plr._tracker_dont_boon = True
        self.card = self.g["Faithful Hound"].remove()

    def test_play(self):
        """Play a Faithful Hound"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_discard(self):
        pass  # TODO


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
