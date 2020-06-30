#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Plague(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocturne'
        self.desc = "Gain a Curse to your hand."
        self.name = "Plague"
        self.purchasable = False
        self.required_cards = ['Curse']

    def special(self, game, player):
        player.gainCard('Curse', destination='hand')


###############################################################################
class Test_Plague(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "Plague":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_plague(self):
        self.plr.setDeck('Duchy', 'Cursed Village', 'Gold')
        self.plr.gainCard('Cursed Village')
        self.assertIsNotNone(self.plr.inHand('Curse'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
