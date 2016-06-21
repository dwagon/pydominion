#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Fortress(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+1 Card +2 Actions. When you trash this, put it into your hand."""
        self.name = 'Fortress'
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def hook_trashThisCard(self, game, player):
        player.output("Putting Fortress back in hand")
        if self in player.played:
            player.addCard(self, 'hand')
            player.played.remove(self)
        if self in player.hand:
            player.addCard(self, 'hand')
            player.hand.remove(self)
        return {'trash': False}


###############################################################################
class Test_Fortress(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Fortress'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Fortress'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the card """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 2)

    def test_trash(self):
        self.plr.trashCard(self.card)
        self.assertIsNotNone(self.plr.inHand('Fortress'))
        self.assertIsNone(self.g.inTrash('Fortress'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
