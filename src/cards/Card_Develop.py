#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Develop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = """Trash a card from your hand. Gain a card costing exactly 1 more
        than it and a card costing exactly 1 less than it, in either order, putting them on top of your deck."""
        self.name = 'Develop'
        self.cost = 3

    def special(self, game, player):
        cards = player.plrTrashCard()
        if not cards:
            return
        card = cards[0]
        if player.cardsWorth(card.cost+1):
            player.plrGainCard(cost=card.cost+1, modifier='equal', destination='topdeck')
        else:
            player.output("No cards worth %s" % (card.cost+1))
        if player.cardsWorth(card.cost-1):
            player.plrGainCard(cost=card.cost-1, modifier='equal', destination='topdeck')
        else:
            player.output("No cards worth %s" % (card.cost-1))


###############################################################################
class Test_Develop(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Develop', 'Smithy'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Develop'].remove()

    def test_play(self):
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy', 'gold', 'smithy']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.inTrash('Duchy'))
        self.assertIsNotNone(self.plr.inDeck('Gold'))
        self.assertIsNotNone(self.plr.inDeck('Smithy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
