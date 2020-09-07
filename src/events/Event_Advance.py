#!/usr/bin/env python

import unittest
import Card
import Game
from Event import Event


###############################################################################
class Event_Advance(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = Game.ADVENTURE
        self.desc = "You may trash an Action card from your hand. If you do, gain an Action card costing up to 6."
        self.name = "Advance"
        self.cost = 0

    def special(self, game, player):
        actions = [c for c in player.hand if c.isAction()]
        trash = player.plrTrashCard(prompt="Trash a card to gain an action costing up to 6", cardsrc=actions)
        if trash:
            player.plrGainCard(6, types={Card.TYPE_ACTION: True})


###############################################################################
class Test_Advance(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Advance'], initcards=['Moat', 'Lurker'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events['Advance']

    def test_advance(self):
        """ Use Advance twice"""
        self.plr.setHand('Moat')
        self.plr.test_input = ['Trash moat', 'Get Lurker']
        self.plr.performEvent(self.card)
        self.assertIsNone(self.plr.in_hand('Moat'))
        self.assertIsNotNone(self.plr.in_discard('Lurker'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
