#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Loan(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = """+1 Coin; When you play this, reveal cards from your
            deck until you reveal a Treasure. Discard it or trash it. Discard
            the other cards."""
        self.name = 'Loan'
        self.cost = 3
        self.coin = 1

    def special(self, game, player):
        """ When you play this, reveal cards from your deck until
            you reveal a Treasure. Discard it or trash it. Discard the
            other cards """
        while True:
            c = player.nextCard()
            player.revealCard(c)
            if c.isTreasure():
                break
            player.output("Revealed and discarded %s" % c.name)
            player.discardCard(c)
        discard = player.plrChooseOptions(
            "What to do?",
            ("Discard %s" % c.name, True), ("Trash %s" % c.name, False))
        if discard:
            player.discardCard(c)
        else:
            player.trashCard(c)


###############################################################################
class Test_Loan(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Loan'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.loan = self.plr.gainCard('Loan', 'hand')

    def test_play(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.loan)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_discard(self):
        tsize = self.g.trashSize()
        self.plr.setDeck('Estate', 'Gold', 'Estate', 'Duchy')
        self.plr.test_input = ['0']
        self.plr.playCard(self.loan)
        self.assertEqual(self.plr.discardpile[-1].name, 'Gold')
        for c in self.plr.discardpile[:-1]:
            self.assertNotEqual(c.cardtype, Card.TYPE_TREASURE)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_trash(self):
        tsize = self.g.trashSize()
        self.plr.setDeck('Estate', 'Gold', 'Estate', 'Duchy')
        self.plr.test_input = ['1']
        self.plr.playCard(self.loan)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash('Gold'))
        for c in self.plr.discardpile:
            self.assertNotEqual(c.cardtype, Card.TYPE_TREASURE)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
