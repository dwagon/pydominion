#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Craftsman"""

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Craftsman(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "+2 Debt; Gain a card costing up to $5."
        self.name = "Craftsman"
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player"):
        player.plr_gain_card(5)
        player.debt.add(2)


###############################################################################
class Test_Craftsman(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Craftsman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Craftsman")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        debt = self.plr.debt.get()
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.debt.get(), debt + 2)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
