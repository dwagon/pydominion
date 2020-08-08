#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Treasurehunter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = Game.ADVENTURE
        self.desc = """+1 Action, +1 Coin; Gain a Silver per card the player
            to your right gained in his last turn. Discard to replace with Warrior"""
        self.name = 'Treasure Hunter'
        self.purchasable = False
        self.actions = 1
        self.coin = 1
        self.cost = 3
        self.numcards = 5

    def special(self, game, player):
        """ Gain a Silver per card the player to your right gained in his last turn """
        righty = game.playerToRight(player)
        numsilver = len(righty.stats['gained'])
        player.output("Gaining %d silvers as %s gained %d cards" % (numsilver, righty.name, numsilver))
        for _ in range(numsilver):
            player.gainCard('Silver')

    def hook_discardThisCard(self, game, player, source):
        """ Replace with Warrior """
        player.replace_traveller(self, 'Warrior')


###############################################################################
class Test_Treasurehunter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Page'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g['Treasure Hunter'].remove()

    def test_treasure_hunter(self):
        """ Play a treasure_hunter """
        self.other.gainCard('Copper')
        self.other.gainCard('Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.discard_size(), 2)
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
