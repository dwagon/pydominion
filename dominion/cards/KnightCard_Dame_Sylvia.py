#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Dame_Sylvia """

import unittest

from dominion import Game, Piles, Card, Player
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_DameSylvia(KnightCard):
    def __init__(self) -> None:
        KnightCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.KNIGHT,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Dame Sylvia"
        self.desc = """+2 Coin
            Each other player reveals the top 2 cards of his deck, trashes one of
            them costing from 3 to 6, and discards the rest.
            If a Knight is trashed by this, trash this card."""
        self.coin = 2
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        self.knight_special(game, player)


###############################################################################
class TestDameSylvia(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Knights"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.print_state()
        self.card = self.g.get_card_from_pile("Knights", "Dame Sylvia")

    def test_score(self) -> None:
        """Play the Dame"""
        self.assertIsNotNone(self.card)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
