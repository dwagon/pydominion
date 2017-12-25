#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Haunting(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocture'
        self.desc = "If you have at least 4 cards in hand, put one of them onto your deck."
        self.name = "Haunting"
        self.purchasable = False

    def special(self, game, player):
        if player.handSize() >= 4:
            card = player.cardSel(force=True)
            player.addCard(card[0], 'topdeck')


###############################################################################
class Test_Haunting(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "Haunting":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_none(self):
        self.plr.setHand('Duchy', 'Gold', 'Silver')
        self.plr.gainCard('Cursed Village')

    def test_activate(self):
        self.plr.setHand('Duchy', 'Gold', 'Silver', 'Province')
        self.plr.test_input = ['Gold']
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.deck[-1].name, 'Gold')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF