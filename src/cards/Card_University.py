#!/usr/bin/env python

import unittest
from Card import Card


class Card_University(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Gain an action card costing up to 5"
        self.name = 'University'
        self.cost = 2
        self.required_cards = ['Potion']
        self.potcost = True

    def special(self, game, player):
        """ Gain an action card costing up to 5"""
        c = player.plrGainCard(5, types={'action': True})
        if c:
            player.output("Gained %s from university" % c.name)


###############################################################################
class Test_University(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['University'], badcards=['Inn', 'Death Cart', 'Blessed Village', 'Cursed Village', 'Experiment', 'Ducat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.university = self.g['University'].remove()
        self.plr.addCard(self.university, 'hand')

    def test_gain(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.university)
        try:
            self.assertEqual(self.plr.discardSize(), 1)
            self.assertTrue(self.plr.discardpile[0].isAction())
            self.assertLessEqual(self.plr.discardpile[0].cost, 5)
        except AssertionError:      # pragma: no cover
            self.g.print_state()
            raise

    def test_none(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.university)
        self.assertTrue(self.plr.discardpile.isEmpty())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
