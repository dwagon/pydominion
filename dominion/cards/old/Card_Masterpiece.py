#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player, Phase, NoCardException


###############################################################################
class Card_Masterpiece(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.GUILDS
        self.name = "Masterpiece"
        self.overpay = True
        self.coin = 1
        self.cost = 3

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return """+1 Coin. When you buy this, you may overpay for it.
                If you do, gain a Silver per coin you overpaid."""
        return "+1 Coin"

    def hook_overpay(self, game: Game.Game, player: Player.Player, amount: int) -> None:
        for _ in range(amount):
            try:
                player.gain_card("Silver")
            except NoCardException:
                player.output("No more Silvers")
                break
        player.output(f"Gained {amount} Silvers")


###############################################################################
class TestMasterpiece(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Masterpiece"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Masterpiece")

    def test_play(self) -> None:
        """Play a Masterpiece"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy(self) -> None:
        """Buy a Masterpiece"""
        self.plr.coins.set(5)
        self.plr.test_input = ["1"]
        self.plr.buy_card("Masterpiece")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
