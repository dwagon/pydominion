#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Training(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Move your +1 Coin Token to an Action Supply Pile"
        self.name = "Training"
        self.cost = 6

    def special(self, game, player):
        """ Move your +1 Coin token to an Action Supply Pile """
        actionpiles = game.getActionPiles()
        stacks = player.cardSel(num=1, prompt='What stack to add the +1 Coin Token to?', cardsrc=actionpiles)
        if stacks:
            player.place_token('+1 Coin', stacks[0].name)


###############################################################################
class Test_Training(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Training'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Training']

    def test_with_treasure(self):
        """ Use Training """
        self.plr.addCoin(6)
        self.plr.test_input = ['moat']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.tokens['+1 Coin'], 'Moat')
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
