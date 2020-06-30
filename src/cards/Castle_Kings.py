#!/usr/bin/env python

import unittest
from cards.Card_Castles import CastleCard


###############################################################################
class Card_KingsCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = ['victory', 'castle']
        self.base = 'empires'
        self.cost = 10
        self.desc = "Worth 2VP per Castle you have."
        self.name = "King's Castle"

    def special_score(self, game, player):
        return sum([2 for card in player.allCards() if card.isCastle()])


###############################################################################
class Test_KingsCastle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Castles'])
        self.g.start_game()
        self.plr = self.g.playerList(0)

    def test_have(self):
        """ Have a kings castle"""
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == "King's Castle":  # One before Kings
                break
        self.plr.addCard(self.card, 'hand')
        self.assertEqual(self.plr.getScoreDetails()["King's Castle"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
