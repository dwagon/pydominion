#!/usr/bin/env python

import unittest
import Game
from cards.Card_Castles import CastleCard


###############################################################################
class Card_HumbleCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = ['treasure', 'victory', 'castle']
        self.base = 'empires'
        self.cost = 3
        self.desc = "+1 Coin; Worth 1VP per Castle you have."
        self.coin = 1
        self.name = "Humble Castle"

    def special_score(self, game, player):
        score = 0
        for card in player.allCards():
            if card.isCastle():
                score += 1
        return score


###############################################################################
class Test_HumbleCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Castles'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Humble Castle':
                break

    def test_play(self):
        """ Play a castle """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_score(self):
        self.plr.addCard(self.card, 'discard')
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Humble Castle'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
