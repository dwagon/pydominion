#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Treasure_Trove(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.TREASURE
        self.base = Game.ADVENTURE
        self.desc = "+2 Coin. When you play this, gain a Gold and a Copper"
        self.name = 'Treasure Trove'
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        """ When you play this, gain a Gold and a Copper """
        player.gainCard('Copper')
        player.gainCard('Gold')
        player.output("Gained a Copper and a Gold")


###############################################################################
class Test_Treasure_Trove(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Treasure Trove'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Treasure Trove'].remove()

    def test_play(self):
        """ Play a treasure trove"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discardpile[0].name, 'Copper')
        self.assertEqual(self.plr.discardpile[1].name, 'Gold')
        self.assertEqual(self.plr.discard_size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
