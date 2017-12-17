#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Monastery(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'night'
        self.base = 'nocturne'
        self.desc = "For each card you've gained this turn, you may trash a card from your hand or a Copper you have in play."
        self.name = 'Monastery'
        self.cost = 2

    def special(self, game, player):
        numgained = len(player.stats['gained'])
        if not numgained:
            return
        player.plrTrashCard(num=numgained)


###############################################################################
class Test_Monastery(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Monastery'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.monastery = self.g['Monastery'].remove()
        self.plr.addCard(self.monastery, 'hand')

    def test_play_card(self):
        """ Play Monastery """
        self.plr.gainCard('Silver')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
