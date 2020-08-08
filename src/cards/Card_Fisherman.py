#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fisherman """

import unittest
import Game
from Card import Card


###############################################################################
class Card_Fisherman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = Game.MENAGERIE
        self.desc = "+1 Card; +1 Action; +1 Coin; During your turns, if your discard pile is empty, this costs 3 Coin less."
        self.name = 'Fisherman'
        self.coin = 1
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_this_card_cost(self, game, player):
        if player.discardpile.is_empty():
            return -3
        return 0


###############################################################################
class Test_Fisherman(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Fisherman'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Fisherman'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play the card """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 1)

    def test_buycard(self):
        """ Buy the card """
        self.plr.setDiscard('Copper')
        self.assertEqual(self.plr.cardCost(self.card), 5)
        self.plr.setDiscard()
        self.assertEqual(self.plr.cardCost(self.card), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
