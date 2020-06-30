#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Poacher(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 Card, +1 Action, +1 Coin. Discard a card per empty supply pile."
        self.name = 'Poacher'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 4

    def special(self, game, player):
        empties = sum([1 for st in game.cardpiles if game[st].isEmpty()])
        if empties:
            player.plrDiscardCards(num=empties, force=True)


###############################################################################
class Test_Poacher(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Poacher', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Poacher'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 1)

    def test_empty(self):
        self.plr.setHand('Gold', 'Province')
        while True:
            c = self.g['Moat'].remove()
            if not c:
                break
        self.plr.test_input = ['Discard Gold']
        self.plr.playCard(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
