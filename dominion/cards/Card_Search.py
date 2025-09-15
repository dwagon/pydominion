#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Search"""

import unittest

from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Search(Card.Card):
    """Search"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+$2; The next time a Supply pile empties, trash this and gain a Loot."""
        self.name = "Search"
        self.cost = 2
        self.coin = 2
        self.permanent = True
        self.required_cards = ["Loot"]

    def hook_emptied_pile(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> None:
        player.output(f"Supply pile {card} emptied - {self} trashing itself")
        player.trash_card(self)
        player.gain_card("Loot")


###############################################################################
class TestSearch(unittest.TestCase):
    """Test Search"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Search", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Search")

    def test_play_card(self) -> None:
        """Play Card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.assertIn("Search", self.plr.piles[Piles.DURATION])

    def test_empty_stack(self):
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.piles[Piles.DISCARD].set()
        for i in range(10):
            self.g.get_card_from_pile("Moat")
        self.assertIn("Search", self.g.trash_pile)
        self.assertGreaterEqual(len(self.plr.piles[Piles.DISCARD]), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
