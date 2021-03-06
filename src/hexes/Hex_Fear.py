#!/usr/bin/env python

import unittest
import Card
import Game
from Hex import Hex


###############################################################################
class Hex_Fear(Hex):
    def __init__(self):
        Hex.__init__(self)
        self.cardtype = Card.TYPE_HEX
        self.base = Game.NOCTURNE
        self.desc = "If you have at least 5 cards in hand, discard an Action or Treasure"
        self.name = "Fear"
        self.purchasable = False

    def special(self, game, player):
        if player.hand.size() < 5:
            return
        tanda = [_ for _ in player.hand if _.isAction() or _.isTreasure()]
        player.plrDiscardCards(num=1, cardsrc=tanda, prompt="Discard an Action or a Treasure")


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(1, keepvic=True)


###############################################################################
class Test_Fear(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cursed Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for h in self.g.hexes[:]:
            if h.name != "Fear":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_empty_war(self):
        self.plr.setHand('Estate', 'Duchy', 'Province', 'Gold')
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.discardpile.size(), 1)     # The Cursed Village

    def test_war(self):
        self.plr.setHand('Estate', 'Duchy', 'Estate', 'Duchy', 'Copper')
        self.plr.test_input = ['Copper']
        self.plr.gainCard('Cursed Village')
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertIsNotNone(self.plr.in_discard('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
