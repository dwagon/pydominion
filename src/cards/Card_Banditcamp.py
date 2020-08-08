#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Banditcamp(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 Card +2 Actions. Gain a Spoils from the Spoils pile."
        self.name = 'Bandit Camp'
        self.required_cards = ['Spoils']
        self.cost = 5
        self.actions = 2
        self.cards = 1

    def special(self, game, player):
        """ Gain a spoils """
        player.output("Gained a Spoils")
        player.gainCard('Spoils')


###############################################################################
class Test_Banditcamp(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bandit Camp'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        bc = self.g['Bandit Camp'].remove()
        self.plr.addCard(bc, 'hand')
        self.plr.playCard(bc)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.discardpile[0].name, 'Spoils')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
