#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Famine(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocture'
        self.desc = "Reveal the top 3 cards of your deck. Discard the Actions. Shuffle the rest into your deck."
        self.name = "Famine"
        self.purchasable = False

    def special(self, game, player):
        for i in range(3):
            c = player.nextCard()
            if c.isAction():
                player.output("Discarding {}".format(c))
                player.discardCard(c)
            else:
                player.output("Putting {} back in deck".format(c))
                player.addCard(c, 'topdeck')
        player.deck.shuffle()


###############################################################################
class Test_Famine(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "The Flame's Gift":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)
        self.card = self.g['Cursed Village'].remove()

    def test_flames_gift(self):
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.inTrash('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
