#!/usr/bin/env python

import unittest
from Card import Card


class Card_Loan(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'prosperity'
        self.desc = "+1 Gold, Dig for a treasure and trash or discard it"
        self.name = 'Loan'
        self.cost = 3
        self.gold = 1

    def special(self, game, player):
        """ When you play this, reveal cards from your deck until
            you reveal a Treasure. Discard it or trash it. Discard the
            other cards """
        while True:
            c = player.nextCard()
            if c.isTreasure():
                break
            else:
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
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['loan'])
        self.plr = self.g.players.values()[0]
        self.loan = self.plr.gainCard('loan', 'hand')

    def test_play(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.loan)
        self.assertEquals(self.plr.t['gold'], 1)

    def test_discard(self):
        self.plr.setDeck('estate', 'gold', 'estate', 'duchy')
        self.plr.test_input = ['0']
        self.plr.playCard(self.loan)
        self.assertEquals(self.plr.discardpile[-1].name, 'Gold')
        for c in self.plr.discardpile[:-1]:
            self.assertNotEqual(c.cardtype, 'treasure')
        self.assertEquals(self.g.trashpile, [])

    def test_trash(self):
        self.plr.setDeck('estate', 'gold', 'estate', 'duchy')
        self.plr.test_input = ['1']
        self.plr.playCard(self.loan)
        self.assertEquals(len(self.g.trashpile), 1)
        self.assertEquals(self.g.trashpile[0].name, 'Gold')
        for c in self.plr.discardpile:
            self.assertNotEqual(c.cardtype, 'treasure')

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
