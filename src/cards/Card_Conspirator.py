#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Conspirator(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+2 gold. If played more than 3 actions +1 card, +1 action"
        self.name = 'Conspirator'
        self.gold = 2
        self.cost = 4

    def special(self, player, game):
        """ If you've player 3 or more actions this turn (counting
            this); +1 card, +1 action """
        if self.numActionsPlayed(player) >= 3:
            player.pickupCard()
            player.addActions(1)

    def numActionsPlayed(self, player):
        return sum([1 for c in player.played if c.isAction()])


###############################################################################
class Test_Conspirator(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['conspirator', 'witch'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['conspirator'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the conspirator with not enough actions """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)
        self.assertEqual(self.plr.getActions(), 0)
        self.assertEqual(self.plr.handSize(), 5)

    def test_actions(self):
        """ Play the conspirator with enough actions """
        self.plr.setPlayed('witch', 'witch', 'witch')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
