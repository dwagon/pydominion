#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_City(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "+1 card, +2 action, more if stacks empty"
        self.name = 'City'
        self.cost = 5
        self.cards = 1
        self.actions = 2

    ###########################################################################
    def special(self, game, player):
        """ If there are one or more empty Supply piles, +1 card.
        If there are two or more, +1 gold, +1 buy """
        empties = sum([1 for st in game.cardpiles if game[st].isEmpty()])
        if empties >= 1:
            player.pickupCard()
        if empties >= 2:
            player.addGold(1)
            player.addBuys(1)


###############################################################################
class Test_City(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['city', 'moat', 'cellar'])
        self.plr = self.g.players.values()[0]
        self.city = self.g['city'].remove()
        self.plr.addCard(self.city, 'hand')

    def test_nostacks(self):
        """ Play a city with no stacks empty """
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(len(self.plr.hand), 6)

    def test_onestack(self):
        """ Play a city with one stacks empty """
        while(True):
            c = self.g['moat'].remove()
            if not c:
                break
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(len(self.plr.hand), 7)

    def test_twostack(self):
        """ Play a city with two stacks empty """
        while(True):
            c = self.g['moat'].remove()
            if not c:
                break
        while(True):
            c = self.g['cellar'].remove()
            if not c:
                break
        self.plr.playCard(self.city)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getGold(), 1)
        # 1 default + 1 for city
        self.assertEqual(self.plr.getBuys(), 2)
        # 5 for hand, 1 for city, 1 for one stack
        self.assertEqual(len(self.plr.hand), 7)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
