#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Stockpile """

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Stockpile(Card.Card):
    """Stockpile"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """3 Coin; +1 Buy; When you play this, Exile it."""
        self.name = "Stockpile"
        self.coin = 3
        self.buys = 1
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.exile_card(self)


###############################################################################
class Test_Stockpile(unittest.TestCase):
    """Test Stockpile"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Stockpile"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Stockpile")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the card"""
        self.plr.play_card(self.card)
        self.assertIn("Stockpile", self.plr.piles[Piles.EXILE])
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
