#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Haggler"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Haggler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+2 Coin.
        This turn, when you gain a card, if you bought it, gain a cheaper non-Victory card."""
        self.name = "Haggler"
        self.coin = 2
        self.cost = 5

    def hook_buy_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> None:
        cost = card.cost - 1
        player.plr_gain_card(
            cost=cost,
            types={Card.CardType.ACTION: True, Card.CardType.TREASURE: True},
            prompt=f"Gain a non-Victory card costing under {cost}",
        )


###############################################################################
class Test_Haggler(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Haggler"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Haggler")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_buy(self) -> None:
        """Buy a Gold and haggle a silver"""
        self.plr.piles[Piles.PLAYED].set("Haggler")
        self.plr.test_input = ["Get Silver -"]
        self.plr.coins.set(6)
        self.plr.buy_card("Gold")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
