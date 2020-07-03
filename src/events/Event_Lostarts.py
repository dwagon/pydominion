#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Lostarts(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "Move your +1 Action Token to an Action Supply Pile"
        self.name = "Lost Arts"
        self.cost = 6

    def special(self, game, player):
        """ Move your +1 Action token to an Action Supply Pile """
        actionpiles = game.getActionPiles()
        stacks = player.cardSel(num=1, prompt='What stack to add the +1 Action Token to?', cardsrc=actionpiles)
        if stacks:
            player.place_token('+1 Action', stacks[0].name)


###############################################################################
class Test_Lostarts(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Lost Arts'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Lost Arts']

    def test_with_treasure(self):
        """ Use Lost Arts """
        self.plr.addCoin(6)
        self.plr.test_input = ['moat']
        self.plr.performEvent(self.card)
        self.assertEqual(self.plr.tokens['+1 Action'], 'Moat')
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
