#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Stonemason(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.name = 'Stonemason'
        self.overpay = True
        self.cost = 2

    def desc(self, player):
        if player.phase == 'buy':
            return """Trash a card from your hand. Gain 2 cards each costing less than it.
        When you buy this, you may overpay for it. If you do, gain 2 Actions each costing the amount you overpaid."""
        else:
            return "Trash a card from your hand. Gain 2 cards each costing less than it."

    def special(self, game, player):
        tc = player.plrTrashCard(printcost=True, prompt="Trash a card from your hand. Gain 2 cards each costing less than it.")
        if tc:
            cost = player.cardCost(tc[0]) - 1
            if cost < 0:
                player.output("No suitable cards")
                return
            for i in range(2):
                player.plrGainCard(cost, 'less')

    def hook_overpay(self, game, player, amount):
        player.plrGainCard(amount, 'less', types={'action': True})
        player.plrGainCard(amount, 'less', types={'action': True}, prompt="Gain another card costing up to %s" % amount)


###############################################################################
class Test_Stonemason(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Stonemason', 'Moat'], badcards=["Fool's Gold"])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Stonemason'].remove()

    def test_play(self):
        """ Play a stonemason"""
        self.plr.setHand('Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['trash province', 'get gold', 'get silver']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.inTrash('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Silver'))

    def test_buy(self):
        self.plr.coin = 5
        self.plr.test_input = ['3', 'Moat', 'Stonemason']
        self.plr.buyCard(self.g['Stonemason'])
        self.assertIsNotNone(self.plr.inDiscard('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Stonemason'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
