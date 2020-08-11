#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Poacher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+1 Card, +1 Action, +1 Coin. Discard a card per empty supply pile."
        self.name = 'Poacher'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 4

    def special(self, game, player):
        empties = sum([1 for st in game.cardpiles if game[st].is_empty()])
        if empties:
            player.plrDiscardCards(num=empties, force=True)


###############################################################################
class Test_Poacher(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Poacher', 'Moat'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Poacher'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_actions(), 1)

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
