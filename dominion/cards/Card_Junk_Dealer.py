#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Junk_Dealer"""
import unittest

from dominion import Game, Piles, Card, Player


###############################################################################
class Card_JunkDealer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card; +1 Action; +$1; Trash a card from your hand."""
        self.name = "Junk Dealer"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 5

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Trash a card from your hand."""
        player.plr_trash_card(force=True)


###############################################################################
class TestJunkDealer(unittest.TestCase):
    """Test Junk Dealer"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Junk Dealer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.jd = self.g.get_card_from_pile("Junk Dealer")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Silver", "Gold")
        self.plr.piles[Piles.DECK].set("Estate", "Province", "Duchy")
        self.plr.add_card(self.jd, Piles.HAND)

    def test_trash(self):
        """Test"""
        trash_size = self.g.trash_pile.size()
        self.plr.test_input = ["trash copper", "finish"]
        self.plr.play_card(self.jd)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 4)
        self.assertEqual(self.g.trash_pile.size(), trash_size + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
