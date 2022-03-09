#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Pasture(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_VICTORY, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "+1 Coin; Worth 1VP per Estate you have"
        self.name = "Pasture"
        self.cost = 2
        self.coin = 1
        self.purchasable = False

    def special_score(self, game, player):
        estates = sum([1 for _ in player.allCards() if _.name == "Estate"])
        return estates


###############################################################################
class Test_Pasture(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Shepherd"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Pasture"].remove()

    def test_play(self):
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_score(self):
        self.plr.setHand("Estate", "Pasture")
        self.plr.setDeck("Estate")
        score = self.plr.getScoreDetails()
        self.assertEqual(score["Pasture"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
