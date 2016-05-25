#!/usr/bin/env python

import unittest
from Card import Card


class Card_Traderoute(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "+1 buy, +1 coin per token, trash card from your hand"
        self.name = 'Trade Route'
        self.cost = 3
        self.buys = 1

    @classmethod
    def setup(cls, game):
        cls.tokens = {}
        cls.game = game
        for cp in list(game.cardpiles.values()):
            if cp.isVictory():
                cls.tokens[cp.cardname] = cp.numcards

    def isWorth(self):
        worth = 0
        for cp in list(self.game.cardpiles.values()):
            if cp.cardname in self.tokens:
                if self.tokens[cp.cardname] != cp.numcards:
                    worth += 1
        return worth

    def special(self, game, player):
        """ +1 coin per token on the trade route map. Trash a card
            from your hand. Setup: Put a token on each victory card
            supply pile. When a card is gained from that pile move the
            token to the trade route map """
        player.plrTrashCard()
        player.addCoin(self.isWorth())


###############################################################################
class Test_Traderoute(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Trade Route'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.traderoute = self.g['Trade Route'].remove()
        self.plr.addCard(self.traderoute, 'hand')

    def test_playZero(self):
        self.plr.test_input = ['finish selecting']
        self.plr.playCard(self.traderoute)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.getBuys(), 2)

    def test_playOne(self):
        self.plr.test_input = ['finish selecting']
        self.g['Estate'].remove()
        self.plr.playCard(self.traderoute)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_playTwo(self):
        self.plr.test_input = ['finish selecting']
        self.g['Estate'].remove()
        self.g['Province'].remove()
        self.plr.playCard(self.traderoute)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
