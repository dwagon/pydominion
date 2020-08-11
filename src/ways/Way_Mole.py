#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Mole """

import unittest
import Game
from Way import Way


###############################################################################
class Way_Mole(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "+1 Action; Discard your hand. +3 Cards."
        self.actions = 1
        self.name = "Mole"

    def special(self, game, player):
        player.discardHand()
        player.pickupCards(3)


###############################################################################
class Test_Mole(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, waycards=['Mole'],
            initcards=['Moat'], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Mole']

    def test_play(self):
        """ Perform a Mole """
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
