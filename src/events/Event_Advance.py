#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Advance(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'adventure'
        self.desc = "You may trash an Action card from your hand. If you do, gain an Action card costing up to 6."
        self.name = "Advance"
        self.cost = 0

    def special(self, game, player):
        actions = [c for c in player.hand if c.isAction()]
        trash = player.plrTrashCard(prompt="Trash a card to gain an action costing up to 6", cardsrc=actions)
        if trash:
            player.plrGainCard(6, types={'action': True})


###############################################################################
class Test_Advance(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Advance'], initcards=['Moat', 'Feast'])
        self.g.start_game()
        self.plr = self.g.playerList()[0]
        self.card = self.g.events['Advance']

    def test_advance(self):
        """ Use Advance twice"""
        self.plr.setHand('Moat')
        self.plr.test_input = ['moat', 'feast']
        self.plr.performEvent(self.card)
        self.assertIsNone(self.plr.inHand('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Feast'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
