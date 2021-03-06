#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Frog """

import unittest
import Game
from Way import Way


###############################################################################
class Way_Frog(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "+1 Action; When you discard this from play this turn, put it onto your deck."
        self.actions = 1
        self.name = "Way of the Frog"

    def hook_way_discard_this_card(self, game, player, card):
        player.addCard(card, 'topdeck')
        player.played.remove(card)


###############################################################################
class Test_Frog(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Way of the Frog'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Way of the Frog']

    def test_play(self):
        """ Perform a Frog """
        self.plr.setHand('Copper', 'Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.plr.discardHand()
        self.assertIsNotNone(self.plr.in_deck('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
