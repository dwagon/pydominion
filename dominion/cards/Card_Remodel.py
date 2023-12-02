#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Remodel(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash a card and gain one costing 2 more"
        self.name = "Remodel"
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Trash a card from your hand. Gain a card costing up to
        2 more than the trashed card"""
        if tc := player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain another costing up to 2 more than the one you trashed",
        ):
            cost = tc[0].cost
            player.plr_gain_card(cost + 2)


###############################################################################
class TestRemodel(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Remodel"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.rcard = self.g.get_card_from_pile("Remodel")

    def test_nothing(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.rcard)
        self.assertEqual(self.g.trash_pile.size(), tsize)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_trash_gain_nothing(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["1", "0"]
        self.plr.play_card(self.rcard)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)

    def test_trash_gain_something(self) -> None:
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.rcard, Piles.HAND)
        self.plr.test_input = ["1", "1"]
        self.plr.play_card(self.rcard)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
