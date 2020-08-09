#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Catacombs(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DARKAGES
        self.desc = """Look at the top 3 cards of your deck. Choose one: Put them
            into your hand; or discard them and +3 cards. When you trash this, gain a cheaper card."""
        self.name = 'Catacombs'
        self.cost = 5

    def special(self, game, player):
        cards = []
        for _ in range(3):
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Catacombs'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.cat = self.g['Catacombs'].remove()
        self.plr.addCard(self.cat, 'hand')

    def test_keep(self):
        self.plr.setDeck('Province', 'Gold', 'Gold', 'Gold')
        self.plr.test_input = ['keep the three']
        self.plr.playCard(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(self.plr.handSize(), 8)
        numgold = sum([1 for c in self.plr.hand if c.name == 'Gold'])
        self.assertEqual(numgold, 3)

    def test_discard(self):
        self.plr.setDeck('Province', 'Province', 'Province', 'Gold', 'Gold', 'Gold')
        self.plr.test_input = ['discard and draw']
        self.plr.playCard(self.cat)
        # Normal 5, +3 new ones
        self.assertEqual(self.plr.handSize(), 8)
        numgold = sum([1 for c in self.plr.hand if c.name == 'Gold'])
        self.assertEqual(numgold, 0)
        numprov = sum([1 for c in self.plr.hand if c.name == 'Province'])
        self.assertEqual(numprov, 3)
        numgold = sum([1 for c in self.plr.discardpile if c.name == 'Gold'])
        self.assertEqual(numgold, 3)

    def test_trash(self):
        self.plr.test_input = ['get estate']
        self.plr.trashCard(self.cat)
        self.assertEqual(self.plr.discard_size(), 1)
        self.assertTrue(self.plr.discardpile[0].cost < self.cat.cost)
        self.assertIsNotNone(self.g.in_trash('Catacombs'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
