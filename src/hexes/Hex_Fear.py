#!/usr/bin/env python

import unittest
from Hex import Hex


###############################################################################
class Hex_Fear(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = 'hex'
        self.base = 'nocture'
        self.desc = "If you have at least 5 cards in hand, discard an Action or Treasure"
        self.name = "Fear"
        self.purchasable = False

    def special(self, game, player):
        if player.handSize() < 5:
            return
        tanda = [_ for _ in player.hand if _.isAction() or _.isTreasure()]
        player.plrDiscardCards(num=1, cardsrc=tanda, prompt="Discard an Action or a Treasure")


###############################################################################
def botresponse(player, kind, args=[], kwargs={}):
    return player.pick_to_discard(1, keepvic=True)


###############################################################################
class Test_Fear(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for h in self.g.hexes[:]:
            if h.name != "Fear":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_empty_war(self):
        self.plr.setHand('Estate', 'Duchy', 'Province', 'Gold')
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.discardSize(), 1)     # The Cursed Village

    def test_war(self):
        self.plr.setHand('Estate', 'Duchy', 'Estate', 'Duchy', 'Copper')
        self.plr.test_input = ['Copper']
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.discardSize(), 2)
        self.assertIsNotNone(self.plr.inDiscard('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
