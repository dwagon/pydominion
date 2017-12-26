#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_War(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocture'
        self.desc = "Reveal cards from your deck until revealing one costing 3 or 4. Trash it and discard the rest."
        self.name = "War"
        self.purchasable = False

    def special(self, game, player):
        while True:
            c = player.nextCard()
            if not c:
                break
            if c.cost in (3, 4):
                player.output("Trashing {}".format(c.name))
                player.trashCard(c)
                break
            else:
                player.output("Discarding {}".format(c.name))
                player.discardCard(c)


###############################################################################
class Test_War(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "War":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_war(self):
        tsize = self.g.trashSize()
        self.plr.setDeck('Duchy', 'Cursed Village', 'Silver')
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.inTrash('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
