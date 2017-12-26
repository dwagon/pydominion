#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_WilloWisp(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'spirit']
        self.base = 'nocturne'
        self.desc = "+1 Card; +1 Action; Reveal the top card of your deck. If it costs 2 or less, put it into your hand."
        self.name = "Will-o'-Wisp"
        self.purchasable = False
        self.card = 1
        self.actions = 1
        self.insupply = False
        self.cost = 0

    def special(self, game, player):
        c = player.nextCard()
        if c.cost <= 2 and not c.potcost and not c.debtcost:
            player.addCard(c, 'hand')
            player.output("Moving {} from your deck to your hand".format(c.name))
        else:
            player.addCard(c, 'topdeck')
            player.output("Keep {} on top of your deck".format(c.name))


###############################################################################
class Test_WilloWisp(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Will-o'-Wisp"])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g["Will-o'-Wisp"].remove()

    def test_special_cheap(self):
        self.plr.setHand()
        self.plr.setDeck('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Copper'))

    def test_special_expensive(self):
        self.plr.setHand()
        self.plr.setDeck('Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 0)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNone(self.plr.inHand('Gold'))
        self.assertIsNotNone(self.plr.inDeck('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
