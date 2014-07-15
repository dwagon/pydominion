#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Venture(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+1 coin, get next treasure from deck"
        self.name = 'Venture'
        self.cost = 5

    def special(self, game, player):
        """ When you play this, reveal cards from your deck until
            you reveal a Treasure. Discard the other cards. Play that
            Treasure """
        while(1):
            c = player.pickupCard(verbose=False)
            if c.isTreasure():
                player.output("Picked up %s from Venture" % c.name)
                player.playCard(c)
                break
            else:
                player.output("Picked up and discarded %s" % c.name)
                player.addCoin(c.coin)    # Compensate for not keeping card
                player.discardCard(c)


###############################################################################
class Test_Venture(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['venture'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['venture'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Venture """
        self.plr.setDeck('gold')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)  # Gold
        for c in self.plr.played:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertEqual(self.plr.deck, [])

    def test_discard(self):
        """ Make sure we discard non-treasures """
        self.plr.setDeck('gold', 'estate', 'estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 3)  # Gold
        for c in self.plr.played:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail("Didn't play the gold")
        self.assertEqual(self.plr.discardSize(), 2)
        for c in self.plr.discardpile:
            if c.name != 'Estate':  # pragma: no cover
                self.fail("Didn't discard the non-treasure")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
