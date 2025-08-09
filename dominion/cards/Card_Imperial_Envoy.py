#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Imperial_Envoy"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Imperial_Envoy(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+5 Cards; +1 Buy; +2 Debt"""
        self.name = "Imperial Envoy"
        self.cards = 5
        self.buys = 1
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+2 Debt"""
        player.debt.add(2)


###############################################################################
class Test_Imperial_Envoy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Imperial Envoy"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Imperial Envoy")

    def test_play(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        debt = self.plr.debt.get()
        buys = self.plr.buys.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.play_card(self.card)
        self.assertEqual(debt + 2, self.plr.debt.get())
        self.assertEqual(buys + 1, self.plr.buys.get())
        self.assertEqual(hand_size + 5 - 1, len(self.plr.piles[Piles.HAND]))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
