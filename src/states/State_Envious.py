#!/usr/bin/env python

import unittest
import Card
import Game
from State import State


###############################################################################
class State_Envious(State):
    def __init__(self):
        State.__init__(self)
        self.cardtype = Card.STATE
        self.base = Game.NOCTURNE
        self.desc = "At the start of your Buy phase, return this, and Silver and Gold make 1 this turn."
        self.name = "Envious"

    def hook_preBuy(self, game, player):
        player.remove_state(self)

    def hook_spendValue(self, game, player, card):
        # Silver and Gold make 1
        if card.name == 'Silver':
            return -1
        if card.name == 'Gold':
            return -2
        return 0


###############################################################################
class Test_Envious(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_envious_return(self):
        self.plr.assign_state('Envious')
        self.plr.test_input = ['End Phase']
        self.plr.buy_phase()
        self.assertEqual(self.plr.states, [])

    def test_envious(self):
        self.plr.assign_state('Envious')
        self.plr.setHand('Silver', 'Gold')
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 1)
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
