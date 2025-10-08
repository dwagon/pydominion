#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Mining_Village"""
import unittest

from dominion import Game, Piles, Player, Card


###############################################################################
class Card_MiningVillage(Card.Card):
    """Mining Village"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+1 card, +2 actions, trash self for +2 coin"
        self.name = "Mining Village"
        self.cards = 1
        self.actions = 2
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash this card immediately. If you do +2 coin"""
        if self.location != Piles.PLAYED:
            player.output(f"{self} not in played - can't trash")
            return
        if player.plr_choose_options(
            "Choose one",
            ("Do nothing", False),
            (f"Trash {self} for +2 coin", True),
        ):
            player.output(f"Trashing {self}")
            player.coins.add(2)
            player.trash_card(self)


###############################################################################
class TestMiningVillage(unittest.TestCase):
    """Test Mining Village"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Mining Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mining Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Mining Village"""
        self.plr.test_input = ["Do nothing"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Mining Village", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Mining Village")

    def test_trash(self) -> None:
        """Trash the mining village"""
        self.plr.test_input = ["Trash"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Mining Village", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
