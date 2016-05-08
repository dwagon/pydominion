#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Pathfinding(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Move your +1 Card Token to an Action Supply Pile"
        self.name = "Pathfinding"
        self.cost = 8

    def special(self, game, player):
        """ Move your +1 Card token to an Action Supply Pile """
        actionpiles = []
        for cp in game.cardpiles.values():
            if cp.isAction():
                actionpiles.append(cp)
        stacks = player.cardSel(num=1, prompt='What stack to add the +1 Card Token to?', cardsrc=actionpiles)
        if stacks:
            player.place_token('+Card', stacks[0])


###############################################################################
class Test_Pathfinding(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['pathfinding'], initcards=['moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Pathfinding']

    def test_with_treasure(self):
        """ Use Pathfinding """
        self.plr.addCoin(8)
        self.plr.test_input = ['moat']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.tokens['+Card'], 'moat')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
