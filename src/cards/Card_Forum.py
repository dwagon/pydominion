#!/usr/bin/env python

from Card import Card
import unittest


###############################################################################
class Card_Forum(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.name = 'Forum'
        self.cards = 3
        self.actions = 1
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return "+3 Cards, +1 Action, Discard 2 cards. When you buy this, +1 Buy."
        else:
            return "+3 Cards, +1 Action, Discard 2 cards."

    def special(self, game, player):
        player.plrDiscardCards(num=2, force=True)

    def hook_buyThisCard(self, game, player):
        player.addBuys(1)


###############################################################################
class Test_Forum(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Forum'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.card = self.g['Forum'].remove()

    def test_play(self):
        """ Play a Forum """
        self.plr.setHand('Gold', 'Duchy', 'Estate', 'Province', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy', 'province', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 3 - 2)

    def test_buy(self):
        self.plr.buyCard(self.g['Forum'])
        self.assertEqual(self.plr.getBuys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
