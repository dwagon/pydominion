#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Bagofgold(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'prize']
        self.base = 'cornucopia'
        self.name = "Bag of Gold"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action. Gain a Gold, putting it on top of your deck."
        self.actions = 1

    def special(self, game, player):
        player.gainCard('Gold', 'topdeck')


###############################################################################
class Test_Bagofgold(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Tournament'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Bag of Gold'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.deck[-1].name, 'Gold')
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
