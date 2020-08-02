#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Nobles(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.desc = "2VP, choose +3 cards or +2 actions"
        self.name = 'Nobles'
        self.victory = 2
        self.cost = 6

    def special(self, game, player):
        """ Choose one: +3 Cards; or +2 Actions """
        cards = player.plrChooseOptions(
            "Choose one",
            ('+3 Cards', True), ('+2 Actions', False))
        if cards:
            player.pickupCards(3)
        else:
            player.addActions(2)


###############################################################################
class Test_Nobles(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Nobles'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Nobles'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_cards(self):
        """ Play the Nobles - chosing cards """
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 8)
        self.assertEqual(self.plr.getActions(), 0)

    def test_actions(self):
        """ Play the Nobles - chosing actions """
        self.plr.test_input = ['1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getActions(), 2)

    def test_score(self):
        """ Score the nobles """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Nobles'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
