#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Duke(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.INTRIGUE
        self.desc = "Worth 1 VP per duchy"
        self.name = "Duke"
        self.playable = False
        self.cost = 5

    def special_score(self, game, player):
        """Worth 1VP per Duchy you have"""
        vp = 0
        for c in player.all_cards():
            if c.name == "Duchy":
                vp += 1
        return vp


###############################################################################
class Test_Duke(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Duke"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_score(self):
        self.plr.deck.set("Duchy", "Duchy", "Estate")
        self.plr.hand.set("Silver")
        self.plr.discardpile.set("Duke")
        sc = self.plr.get_score()
        self.assertEqual(sc, 9)  # 3 per duchy, 1 per estate, 2 from duke


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
