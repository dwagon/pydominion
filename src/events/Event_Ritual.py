#!/usr/bin/env python

import unittest
from Event import Event


###############################################################################
class Event_Ritual(Event):
    def __init__(self):
        Event.__init__(self)
        self.base = 'empires'
        self.desc = "Gain a Curse. If you do, trash a card from your hand. +1VP per Coin it cost."
        self.name = "Ritual"
        self.cost = 4
        self.required_cards = ['Curse']

    def special(self, game, player):
        card = player.gainCard('Curse')
        if card:
            tc = player.plrTrashCard(prompt="Trash a card, +1 VP per coin it costs")
            if tc:
                player.addScore('Ritual', tc[0].cost)


###############################################################################
class Test_Ritual(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Ritual'])
        self.g.start_game()
        self.plr = self.g.playerList()[0]
        self.event = self.g.events['Ritual']

    def test_ritual(self):
        """ Use Ritual"""
        self.plr.addCoin(4)
        self.plr.setHand('Gold')
        self.plr.test_input = ['Gold']
        self.plr.performEvent(self.event)
        self.assertEqual(self.plr.getScoreDetails()['Ritual'], 6)
        self.assertIsNotNone(self.g.inTrash('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
