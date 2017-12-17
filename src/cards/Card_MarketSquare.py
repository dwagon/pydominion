#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_MarketSquare(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'darkages'
        self.desc = """+1 Card, +1 Action, +1 Buy.
        When one of your cards is trashed, you may discard this from your hand. If you do, gain a Gold."""
        self.name = 'Market Square'
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.cost = 3

    def hook_trashCard(self, game, player, card):
        gold = player.plrChooseOptions(
            "Discard Market Square to gain a Gold?",
            ("Keep Market Square in hand", False),
            ("Discard and gain a Gold", True))
        if gold:
            player.discardCard(self)
            player.gainCard("Gold")


###############################################################################
class Test_MarketSquare(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Market Square'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Market Square'].remove()

    def test_play(self):
        """ Play the card """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getActions(), 1)

    def test_trash_and_keep(self):
        """ Choose to keep MS after a trash """
        self.plr.setHand('Copper', 'Market Square')
        self.plr.test_input = ['keep']
        self.plr.trashCard(self.plr.inHand('Copper'))
        self.assertIsNotNone(self.plr.inHand('Market Square'))

    def test_trash_and_discard(self):
        """ Choose to keep MS after a trash """
        self.plr.setHand('Copper', 'Market Square')
        self.plr.test_input = ['discard']
        self.plr.trashCard(self.plr.inHand('Copper'))
        self.assertIsNone(self.plr.inHand('Market Square'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
