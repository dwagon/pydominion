#!/usr/bin/env python

import unittest
from cards.Card_Castles import CastleCard


###############################################################################
class Card_CrumblingCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = ['victory', 'castle']
        self.base = 'empires'
        self.cost = 4
        self.desc = "1VP. When you gain or trash this, +1VP and gain a Silver."
        self.victory = 1
        self.name = "Crumbling Castle"

    def hook_gainThisCard(self, game, player):
        player.addScore('Crumbling Castle', 1)
        player.gainCard('Silver')

    def hook_trashThisCard(self, game, player):
        player.addScore('Crumbling Castle', 1)
        player.gainCard('Silver')


###############################################################################
class Test_CrumblingCastle(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Castles'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        while True:
            self.card = self.g['Castles'].remove()
            if self.card.name == 'Crumbling Castle':
                break

    def test_play(self):
        """ Play a castle """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()['Crumbling Castle'], 1)

    def test_trash(self):
        self.plr.trashCard(self.card)
        self.assertEqual(self.plr.getScoreDetails()['Crumbling Castle'], 1)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
