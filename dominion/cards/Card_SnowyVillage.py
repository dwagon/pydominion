#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Snowy_Village """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_SnowyVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = "+1 Card; +4 Actions; +1 Buy; Ignore any further +Actions you get this turn."
        self.name = "Snowy Village"
        self.cost = 3
        self.cards = 1
        self.actions = 4
        self.buys = 1

    def special(self, game, player):
        player.misc["no_actions"] = True


###############################################################################
class Test_SnowyVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Snowy Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Snowy Village"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play a card"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 4)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 4 - 1)  # -1 for playing card
        self.assertEqual(self.plr.get_buys(), 1 + 1 + 1)
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
