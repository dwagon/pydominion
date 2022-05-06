#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Salvager(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.SEASIDE
        self.desc = (
            """+1 Buy. Trash a card from your hand. Gain Coins equal to its cost."""
        )
        self.name = "Salvager"
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        card = player.plr_trash_card(force=True)
        player.output(f"Gained {card[0].cost} coin")
        player.add_coins(card[0].cost)


###############################################################################
class Test_Salvager(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Salvager"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Salvager"].remove()

    def test_play(self):
        """Play a salvage"""
        self.plr.hand.set("Duchy", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNotNone(self.g.in_trash("Duchy"))
        self.assertEqual(self.plr.get_coins(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
