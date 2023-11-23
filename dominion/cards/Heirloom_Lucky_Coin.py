#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_LuckyCoin(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "1 Coin; When you play this, gain a Silver."
        self.name = "Lucky Coin"
        self.cost = 4
        self.coin = 1
        self.purchasable = False

    def special(self, game: Game.Game, player: Player.Player) -> None:
        try:
            player.gain_card("Silver")
        except NoCardException:
            player.output("No more Silver")


###############################################################################
class TestLuckyCoin(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Fool"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Lucky Coin")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
