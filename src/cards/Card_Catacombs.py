#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Catacombs(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "Look at top 3 cards and put them in hand or discard for +3 cards"
        self.name = 'Catacombs'
        self.cost = 5

    def special(self, game, player):
        """ Look at the top 3 cards of your deck. Choose one: Put them
            into your hand; or discard them and +3 cards """
        cards = []
        for i in range(3):
            cards.append(player.nextCard())
        player.output("You drew %s" % ", ".join([c.name for c in cards]))
        ans = player.plrChooseOptions("What do you want to do?", ("Keep the three", True), ("Discard and draw 3 more", False))
        if ans:
            for c in cards:
                player.addCard(c, 'hand')
        else:
            for c in cards:
                player.addCard(c, 'discard')
            player.pickupCards(3)

    def hook_trashThisCard(self, game, player):
        """ When you trash this, gain a cheaper card """
        player.plrGainCard(cost=self.cost - 1)


###############################################################################
class Test_Catacombs(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['catacombs'])
        self.plr = self.g.players.values()[0]
        self.cat = self.g['catacombs'].remove()
        self.plr.addCard(self.cat, 'hand')

    def test_keep(self):
        self.plr.setDeck('province', 'gold', 'gold', 'gold')
        self.plr.test_input = ['0']
        self.plr.playCard(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(len(self.plr.hand), 8)
        numgold = sum([1 for c in self.plr.hand if c.name == 'Gold'])
        self.assertEqual(numgold, 3)

    def test_discard(self):
        self.plr.setDeck('province', 'province', 'province', 'gold', 'gold', 'gold')
        self.plr.test_input = ['1']
        self.plr.playCard(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(len(self.plr.hand), 8)
        numgold = sum([1 for c in self.plr.hand if c.name == 'Gold'])
        self.assertEqual(numgold, 0)
        numprov = sum([1 for c in self.plr.hand if c.name == 'Province'])
        self.assertEqual(numprov, 3)
        numgold = sum([1 for c in self.plr.discardpile if c.name == 'Gold'])
        self.assertEqual(numgold, 3)

    def test_trash(self):
        self.plr.test_input = ['1']
        self.plr.trashCard(self.cat)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertTrue(self.plr.discardpile[0].cost < self.cat.cost)
        self.assertEqual(self.g.trashpile[0].name, self.cat.name)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
