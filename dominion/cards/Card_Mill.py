#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Mill"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_Mill(Card.Card):
    """Mill"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.INTRIGUE
        self.name = "Mill"
        self.desc = "+1 Card; +1 Action; You may discard 2 cards, for +2 Coin; 1VP"
        self.cost = 4
        self.actions = 1
        self.victory = 1
        self.cards = 1

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        dc = player.plr_discard_cards(num=2)
        if len(dc) == 2:
            player.coins.add(2)


###############################################################################
class TestMill(unittest.TestCase):
    """Test Mill"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mill"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mill")

    def test_play(self):
        """Test play"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.test_input = ["Discard Gold", "Finish"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.get_score_details()["Mill"], 1)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_discard(self):
        """Test discard"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.test_input = ["Discard Gold", "Discard Silver", "Finish"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
