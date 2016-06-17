#!/usr/bin/env python

import unittest
from Card import Card
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Sirmichael(KnightCard):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
        self.name = "Sir Michael"
        self.desc = """Each other player discards down to 3 cards in hand.
        Each other player reveals the top 2 cards of his deck, trashes one of them
        costing from 3 to 6, and discards the rest. If a Knight is trashed by this, trash this card."""
        self.cost = 5

    def special(self, game, player):
        for plr in player.attackVictims():
            plr.plrDiscardDownTo(3)
        self.knight_special(game, player)


###############################################################################
class Test_Sir_Michael(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Knight'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Sir Michael':
                break

    def test_score(self):
        """ Play the Sir"""
        self.vic.test_input = ['1', '2', '0']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEquals(self.vic.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
