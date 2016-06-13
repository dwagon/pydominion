#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_IGG(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'hinterlands'
        self.desc = """1 Coin. When you play this, you may gain a Copper, putting it into your hand.
        When you gain this, each other player gains a Curse."""
        self.needcurse = True
        self.name = 'Ill-Gotten Gains'
        self.cost = 5
        self.coin = 1

    def special(self, game, player):
        ans = player.plrChooseOptions(
            "Gain a Copper into your hand?",
            ("No thanks", False),
            ("Gain Copper", True))
        if ans:
            player.gainCard('Copper', destination='hand')

    def hook_gainThisCard(self, game, player):
        for plr in player.attackVictims():
            plr.gainCard('Curse')
            plr.output("Cursed because %s gained an Ill-Gotten Gains" % player.name)


###############################################################################
class Test_IGG(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Ill-Gotten Gains'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Ill-Gotten Gains'].remove()

    def test_play(self):
        """ Play an Ill-Gotten Gains"""
        self.plr.setHand('Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['copper']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inHand('Copper'))
        self.assertEqual(self.plr.getCoin(), 1)

    def test_gain(self):
        """ Gain an Ill-Gotten Gains"""
        self.plr.setHand('Estate')
        self.plr.gainCard('Ill-Gotten Gains')
        self.assertIsNotNone(self.vic.inDiscard('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
