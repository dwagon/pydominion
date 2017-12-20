#!/usr/bin/env python

import unittest
from State import State


###############################################################################
class State_Deluded(State):
    def __init__(self):
        State.__init__(self)
        self.cardtype = 'state'
        self.base = 'nocture'
        self.desc = "At the start of your Buy phase, return this, and you can't buy Actions this turn."
        self.name = "Deluded"
        self.purchasable = False

    def hook_preBuy(self, game, player):
        player.remove_state(self)

    def hook_cardCost(self, game, player, card):
        # Make action cards impossible to afford
        if card.isAction():
            return 99999
        return 0


###############################################################################
class Test_Deluded(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.state = self.g.states['Deluded']

    def test_deluded(self):
        self.plr.assign_state(self.state)
        self.plr.test_input = ['Estate']
        self.assertGreater(self.plr.cardCost(self.g['Bard']), 99)
        self.plr.test_input = ['End Phase']
        self.plr.buyPhase()
        self.assertEqual(self.plr.states, [])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
