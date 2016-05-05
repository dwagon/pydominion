#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Forge(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = ''
        self.desc = "Trash cards from hand and gain one worth the sum of the trashed cards"
        self.name = 'Forge'
        self.cost = 7

    ###########################################################################
    def special(self, game, player):
        """ Trash any number of cards from your hand. Gain a card
            with cost exactly equal to the total cost in coins of the
            trashed cards. """
        availcosts = set()
        for cp in game.cardTypes():
            availcosts.add("%s" % cp.cost)
        player.output("Gain a card costing exactly the sum of the trashed cards")
        player.output("Costs = %s" % ", ".join(sorted(list(availcosts))))
        tc = player.plrTrashCard(anynum=True, num=0, printcost=True)
        cost = sum([c.cost for c in tc])
        player.output("Gain card worth %s" % cost)
        player.plrGainCard(cost=cost, modifier='equal')


###############################################################################
class Test_Forge(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['forge'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.forge = self.g['forge'].remove()

    def test_play(self):
        """ Play the Forge """
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.forge, 'hand')
        # Trash two cards, Finish Trashing, Select another
        self.plr.test_input = ['1', '2', '0', '1']
        self.plr.playCard(self.forge)
        self.assertEqual(self.plr.discardpile[0].cost, 4)
        self.assertEqual(self.g.trashpile[0].name, 'Estate')
        self.assertEqual(self.g.trashSize(), 2)
        self.assertEqual(self.plr.handSize(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
