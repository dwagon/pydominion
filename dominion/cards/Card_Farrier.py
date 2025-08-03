#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Farrier"""
import unittest
from dominion import Card, Game, Piles, Player, Phase, NoCardException


###############################################################################
class Card_Farrier(Card.Card):
    """Farrier"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA_GUILDS
        self.name = "Farrier"
        self.overpay = True
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.cost = 2

    def dynamic_description(self, player: Player.Player) -> str:
        """Variable description"""
        if player.phase == Phase.BUY:
            return """+1 Card; +1 Action; +1 Buy. Overpay: +1 Card at the end of this turn per $1 overpaid."""
        return """+1 Card; +1 Action; +1 Buy."""

    def hook_overpay(self, game: "Game.Game", player: "Player.Player", amount: int) -> None:
        """+1 Card at the end of this turn per $1 overpaid."""
        player.newhandsize += amount


###############################################################################
class TestFarrier(unittest.TestCase):
    """Test Farrier"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Farrier"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Farrier")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_card(self) -> None:
        """Play the Farrier"""
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)  # Used 1 to play card
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 1 - 1)  # -1 for played Farrier

    def test_buy(self) -> None:
        """Buy a Farrier"""
        self.plr.coins.set(6)
        self.plr.test_input = ["3"]
        self.plr.buy_card("Farrier")
        self.plr.end_turn()
        self.assertEqual(len(self.plr.piles[Piles.HAND]), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
