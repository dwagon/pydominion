#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Outpost(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'dutation']
        self.base = 'seaside'
        self.desc = """You only draw 3 cards (instead of 5) in this turn's Clean-up phase.
        Take an extra turn after this one.
        This can't cause you to take more than two consecutive turns."""
        self.name = 'Outpost'
        self.cost = 5

    def hook_cleanup(self, game, player):
        player.newhandsize = 3

    def hook_endTurn(self, game, player):
        game.currentPlayer = game.playerToRight(player)
        player.output("Having a second turn due to Output")


###############################################################################
class Test_Outpost(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Outpost'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Outpost'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play Outpost """
        self.plr.playCard(self.card)
        self.plr.endTurn()
        self.g.print_state()
        # TODO - Not sure how to test this


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
