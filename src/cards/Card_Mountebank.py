#!/usr/bin/env python

import unittest
from Card import Card


class Card_Mountebank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack']
        self.base = 'prosperity'
        self.desc = "+2 coin. Others discard curse or gain one + copper"
        self.name = 'Mountebank'
        self.needcurse = True
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        """ Each other player may discard a Curse. If he doesnt,
            he gains a Curse and a Copper """
        for plr in player.attackVictims():
            for c in plr.hand:
                if c.cardname == 'curse':
                    player.output("Player %s discarded a curse" % plr.name)
                    plr.discardCard(c)
                    break
            else:
                player.output("Player %s gained a curse and a copper" % plr.name)
                plr.addCard(game['Curse'].remove())
                plr.addCard(game['Copper'].remove())


###############################################################################
class Test_Mountebank(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['mountebank'])
        self.g.startGame()
        self.attacker, self.victim = self.g.playerList()
        self.mountebank = self.g['mountebank'].remove()
        self.curse = self.g['curse'].remove()

    def test_hascurse(self):
        self.attacker.addCard(self.mountebank, 'hand')
        self.victim.addCard(self.curse, 'hand')
        self.attacker.playCard(self.mountebank)
        self.assertEqual(self.victim.discardpile[0].name, 'Curse')

    def test_nocurse(self):
        self.attacker.addCard(self.mountebank, 'hand')
        self.attacker.playCard(self.mountebank)
        discards = [c.name for c in self.victim.discardpile]
        self.assertEqual(sorted(discards), sorted(['Curse', 'Copper']))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
