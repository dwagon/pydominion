#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_FaithfulHound(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'nocturne'
        self.desc = "+2 Cards; When you discard this other than during Clean-up, you may set it aside, and put it into your hand at end of turn."
        self.name = 'Faithful Hound'
        self.cards = 2

    def hook_discardThisCard(self, game, player, source):
        if player.phase != 'cleanup':
            player.addCard(self, 'hand')


###############################################################################
class Test_FaithfulHound(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Faithful Hound'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.plr._tracker_dont_boon = True
        self.card = self.g['Faithful Hound'].remove()

    def test_play(self):
        """ Play a Faithful Hound """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5+2)

    def test_discard(self):
        pass    # TODO


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
