#!/usr/bin/env python

import unittest
import Game

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]

    def test_initialCardStacks(self):
        self.assertEqual(len(self.plr.deck), 5)
        self.assertEqual(len(self.plr.hand), 5)
        self.assertEqual(self.plr.played, [])
        self.assertEqual(self.plr.discardpile, [])
        self.g.print_state()

    def test_initialDeck(self):
        self.plr.deck = []
        self.plr.initial_Deck()
        self.assertEqual(len(self.plr.deck), 10)

    def test_trashcard(self):
        numcards = self.g.countCards()
        card = self.plr.hand[0]
        self.plr.trashCard(card)
        self.assertEqual(numcards, self.g.countCards())
        self.assertEqual(self.g.trashpile[0], card)

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF
