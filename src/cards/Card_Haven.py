#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Haven(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "+1 cards, +1 action; play a card next turn"
        self.name = 'Haven'
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def special(self, game, player):
        """ Set aside a card from your hand face down. At the start of
            your next turn, put it into your hand. """
        c = player.plrPickCard(force=True)
        player.addCard(c, 'duration')
        player.hand.remove(c)
        self.savedHavenCard = c

    def duration(self, game, player):
        c = self.savedHavenCard
        player.addCard(c, 'hand')
        # Can't guarantee the order so it may be in played
        # or still in durationpile
        if c in player.played:
            player.played.remove(c)
        elif c in player.durationpile:
            player.durationpile.remove(c)
        player.output("Pulling %s out of from haven" % c)
        del self.savedHavenCard


###############################################################################
class Test_Haven(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['haven'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['haven'].remove()
        self.plr.setDiscard('copper', 'copper', 'copper', 'copper', 'copper')
        self.plr.setDeck('estate', 'estate', 'estate', 'estate', 'gold')
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a haven """
        self.plr.test_input = ['pick gold']
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertEquals(self.plr.durationSize(), 2)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEquals(self.plr.playedSize(), 1)
        self.assertTrue(self.plr.inHand('Gold'))
        self.assertEquals(self.plr.handSize(), 6)
        self.assertEquals(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
