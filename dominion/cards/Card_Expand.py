#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Expand(Card.Card):
    def __init__(self)->None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = "Expand"
        self.cost = 7

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. Gain a card costing up to
        3 more than the trashed card"""
        if tc := player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain another costing up to 3 more than the one you trashed",
        ):
            cost = tc[0].cost
            player.plr_gain_card(cost + 3)


###############################################################################
class Test_Expand(unittest.TestCase):
    def setUp(self)->None:
        self.g = Game.TestGame(numplayers=1, initcards=["Expand"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.expand = self.g.get_card_from_pile("Expand")

    def test_play(self)->None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.expand, Piles.HAND)
        self.plr.test_input = ["Trash Copper", "Get Estate"]
        self.plr.play_card(self.expand)
        self.g.print_state()
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertLessEqual(self.plr.piles[Piles.DISCARD][0].cost, 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
