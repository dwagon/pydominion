#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Treasurehunter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_TRAVELLER]
        self.base = Game.ADVENTURE
        self.desc = """+1 Action, +1 Coin; Gain a Silver per card the player
            to your right gained in his last turn. Discard to replace with Warrior"""
        self.name = "Treasure Hunter"
        self.purchasable = False
        self.actions = 1
        self.coin = 1
        self.cost = 3
        self.numcards = 5

    def special(self, game, player):
        """Gain a Silver per card the player to your right gained in his last turn"""
        righty = game.playerToRight(player)
        numsilver = len(righty.stats["gained"])
        player.output(
            "Gaining %d silvers as %s gained %d cards"
            % (numsilver, righty.name, numsilver)
        )
        for _ in range(numsilver):
            player.gain_card("Silver")

    def hook_discard_this_card(self, game, player, source):
        """Replace with Warrior"""
        player.replace_traveller(self, "Warrior")


###############################################################################
class Test_Treasurehunter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Page"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g["Treasure Hunter"].remove()

    def test_treasure_hunter(self):
        """Play a treasure_hunter"""
        self.other.gain_card("Copper")
        self.other.gain_card("Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 2)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
