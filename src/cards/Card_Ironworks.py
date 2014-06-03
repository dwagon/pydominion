#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Ironworks(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "Gain a card costing up to 4. Extra depending on what it is"
        self.name = 'Iron Works'
        self.cost = 4

    def special(self, player, game):
        """ Gain a card costing up to 4. If it is an action card:
            +1 action; treasure card +1 gold; victory card, +1 card"""
        c = player.plrGainCard(4, force=True)
        if c.isVictory():
            player.pickupCard()
        if c.isAction():
            player.t['actions'] += 1
        if c.isTreasure():
            player.t['gold'] += 1


###############################################################################
class Test_Ironworks(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        # Make most of the cards too expensive to ensure we can select what we want
        initcards = ['ironworks', 'greathall', 'apprentice', 'banditcamp',
                     'city', 'count', 'duke', 'library', 'market', 'rebuild']
        self.g.startGame(numplayers=1, initcards=initcards)
        self.plr = self.g.players[0]
        self.card = self.g['ironworks'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_great_hall(self):
        """ Use Ironworks to gain a Great Hall """
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Great Hall')
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(len(self.plr.hand), 6)

    def test_play_silver(self):
        """ Use Ironworks to gain a Silver """
        self.plr.test_input = ['5']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Silver')
        self.assertEqual(self.plr.t['actions'], 0)
        self.assertEqual(self.plr.t['gold'], 1)
        self.assertEqual(len(self.plr.hand), 5)

    def test_play_ironworks(self):
        """ Use Ironworks to gain an Ironworks """
        self.plr.test_input = ['2']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[-1].name, 'Iron Works')
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['gold'], 0)
        self.assertEqual(len(self.plr.hand), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
