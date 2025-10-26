#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Rice"""
import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Rice(Card.Card):
    """Rice"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """+1 Buy; +$1 per different type among cards you have in play."""
        self.name = "Rice"
        self.cost = 7
        self.buys = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+$1 per different type among cards you have in play."""
        player.coins.add(len(self.cardtype))


###############################################################################
class TestRice(unittest.TestCase):
    """Test Rice"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Rice"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Rice")

    def test_play_treasure(self) -> None:
        """Play card"""
        self.plr.piles[Piles.PLAYED].set("Copper", "Rice", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)  # Treasure, Victory


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
