#!/usr/bin/env python

import unittest
import Game
from Boon import Boon


###############################################################################
class Boon_Earths_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = Game.NOCTURNE
        self.desc = "You may discard a Treasure to gain a card costing up to 4"
        self.name = "The Earth's Gift"
        self.purchasable = False
        self.coin = 2

    def special(self, game, player):
        treasures = [c for c in player.hand if c.isTreasure()]
        if not treasures:
            return
        tr = player.plrDiscardCards(cardsrc=treasures, prompt="Discard a Treasure to gain a card costing up to 4")
        if tr:
            player.plrGainCard(4)


###############################################################################
class Test_Earths_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Earth's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_earths_gift(self):
        self.coins = 0
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Discard Copper', 'Get Silver']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 2 + 2)     # Boon + Bard
            self.assertIsNotNone(self.plr.in_discard('Silver'))
            self.assertIsNotNone(self.plr.in_discard('Copper'))
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
