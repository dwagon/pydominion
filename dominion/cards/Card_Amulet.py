#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Amulet"""
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Amulet(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Now and next turn - Choose 1: +1 Coin, trash card, gain silver"
        self.name = "Amulet"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        self.amulet_special(player)

    def duration(self, game: Game.Game, player: Player.Player) -> None:
        self.amulet_special(player)

    def amulet_special(self, player: Player.Player) -> None:
        """Now and at the start of your next turn, choose one: +1 Coin;
        or trash a card from your hand; or gain a Silver"""
        choice = player.plr_choose_options(
            "Pick one",
            ("Gain a coin", "coin"),
            ("Trash a card", "trash"),
            ("Gain a silver", "silver"),
        )
        match choice:
            case "coin":
                player.coins.add(1)
            case "trash":
                player.plr_trash_card(num=1)
            case "silver":
                try:
                    player.gain_card("Silver")
                except NoCardException:
                    player.output("No more Silver")


###############################################################################
class TestAmulet(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Amulet"], badcards=["Shaman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Amulet")
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_coin(self) -> None:
        """Play an amulet with coin"""
        self.plr.test_input = ["coin", "coin"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_silver(self) -> None:
        """Play an amulet with coin"""
        self.plr.test_input = ["silver", "silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_trash(self) -> None:
        """Play an amulet with trash"""
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash", "duchy", "finish", "trash", "1", "finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
