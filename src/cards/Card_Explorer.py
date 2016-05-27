#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Explorer(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Reveal a provice to gain gold else gain silver"
        self.name = 'Explorer'
        self.cost = 5

    def special(self, game, player):
        """ You may reveal a Province card from you hand. If you
            do, gain a Gold card, putting it into your hand. Otherise,
            gain a Silver card, putting it into your hand """
        if player.inHand('Province'):
            player.output("Gained a Gold")
            player.gainCard('Gold', destination='hand')
        else:
            player.output("Gained a Silver")
            player.gainCard('Silver', destination='hand')


###############################################################################
class Test_Explorer(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Explorer'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Explorer'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_province(self):
        self.plr.gainCard('Province', 'hand')
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.inHand('Gold'))
        # 5 + province + gold
        self.assertEqual(self.plr.handSize(), 7)

    def test_no_province(self):
        self.plr.playCard(self.card)
        self.assertTrue(self.plr.inHand('Silver'))
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
