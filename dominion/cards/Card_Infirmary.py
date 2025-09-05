#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Infirmary"""
import unittest

from dominion import Game, Card, Piles, Player, Phase


###############################################################################
class Card_Infirmary(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.name = "Infirmary"
        self.overpay = True
        self.cost = 3
        self.cards = 1

    def dynamic_description(self, player: "Player.Player") -> str:
        if player.phase == Phase.BUY:
            return """+1 Card; You may trash a card from your hand. Overpay: Play this once per $1 overpaid."""
        return """+1 Card; You may trash a card from your hand."""

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may trash a card from your hand."""
        player.plr_trash_card(1)

    def hook_overpay(self, game: "Game.Game", player: "Player.Player", amount: int) -> None:
        """Play this once per $1 overpaid."""
        for run in range(amount):
            player.play_card(self, cost_action=False, discard=False)


###############################################################################
class Test_Infirmary(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Infirmary"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Infirmary")

    def test_play(self) -> None:
        """Play card"""
        self.plr.piles[Piles.DECK].set("Gold", "Province")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Trash Copper", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1 - 2)  # -2 for play and discard

    def test_buy(self) -> None:
        """Test overpaying"""
        self.plr.coins.set(6)
        self.plr.piles[Piles.DECK].set("Gold", "Province")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Duchy")
        self.plr.test_input = ["2", "Trash Copper", "Trash Estate"]
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.buy_card("Infirmary")
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Estate", self.g.trash_pile)
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Infirmary", self.plr.piles[Piles.DISCARD])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 2)  # -2 for play and discard


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
