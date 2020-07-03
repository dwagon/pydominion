#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Devils_Workshop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'night'
        self.base = 'nocturne'
        self.desc = "If the number of cards you've gained this turn is: 2+, gain an Imp from its pile; 1, gain a card costing up to 4; 0, gain a Gold."
        self.name = "Devil's Workshop"
        self.cost = 4
        self.required_cards = [('Card', 'Imp')]

    def night(self, game, player):
        nc = len(player.stats['gained'])
        player.output("You gained {} cards this turn".format(nc))
        if nc >= 2:
            player.gainCard('Imp')
            player.output("Gained an Imp")
        elif nc == 1:
            player.plrGainCard(4)
        else:
            player.gainCard('Gold')
            player.output("Gained a Gold")


###############################################################################
class Test_Devils_Workshop(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Devil's Workshop", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Devil's Workshop"].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_0(self):
        self.plr.phase = 'night'
        self.plr.playCard(self.card)
        try:
            self.assertIsNotNone(self.plr.inDiscard('Gold'))
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_play_1(self):
        self.plr.phase = 'night'
        self.plr.gainCard('Copper')
        self.plr.test_input = ['Moat']
        self.plr.playCard(self.card)
        try:
            self.assertLessEqual(self.plr.discardpile[0].name, 'Moat')
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_play_2(self):
        self.plr.phase = 'night'
        self.plr.gainCard('Copper')
        self.plr.gainCard('Estate')
        self.plr.playCard(self.card)
        try:
            self.assertIsNotNone(self.plr.inDiscard('Imp'))
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
