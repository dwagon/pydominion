#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Cutpurse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.desc = "+2 gold, other players discard copper"
        self.name = 'Cutpurse'
        self.gold = 2
        self.cost = 4

    def special(self, game, player):
        """ Each other player discard a Copper card (or reveals a
            hand with no copper)."""

        for victim in player.attackVictims():
            c = victim.inHand('Copper')
            if c:
                player.output("%s discarded a copper" % victim.name)
                victim.discardCard(c)
            else:
                player.output("%s had no coppers" % victim.name)


###############################################################################
class Test_Cutpurse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['cutpurse'])
        self.plr = self.g.players[0]
        self.victim = self.g.players[1]
        self.card = self.g['cutpurse'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play_coppers(self):
        self.victim.setHand('copper', 'copper', 'estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile[-1].name, 'Copper')
        self.assertEqual(len(self.victim.hand), 2)

    def test_play_none(self):
        self.victim.setHand('estate', 'estate', 'estate')
        self.plr.playCard(self.card)
        self.assertEqual(self.victim.discardpile, [])
        self.assertEqual(len(self.victim.hand), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF
