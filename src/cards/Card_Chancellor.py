#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Chancellor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+2 Coin; You may immediately put your deck into your discard pile."
        self.name = 'Chancellor'
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        ans = player.plrChooseOptions("Discard deck?", ("Don't Discard", False), ("Discard Deck", True))
        if ans:
            for c in player.deck[:]:
                player.addCard(c, 'discard')
                player.deck.remove(c)


###############################################################################
class Test_Chancellor(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Chancellor'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g['Chancellor'].remove()
        self.plr.setHand('Estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_nodiscard(self):
        self.plr.setDeck('Copper', 'Silver', 'Gold')
        self.plr.setDiscard('Estate', 'Duchy', 'Province')
        self.plr.test_input = ["Don't discard"]
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.deckSize(), 3)
        self.assertEqual(self.plr.discard_size(), 3)

    def test_discard(self):
        self.plr.setDeck('Copper', 'Silver', 'Gold')
        self.plr.setDiscard('Estate', 'Duchy', 'Province')
        self.plr.test_input = ['discard deck']
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.deckSize(), 0)
        self.assertEqual(self.plr.discard_size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
