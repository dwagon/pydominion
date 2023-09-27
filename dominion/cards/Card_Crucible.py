#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Crucible"""
import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Crucible(Card.Card):
    """Crucible"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """Trash a card from your hand. +$1 per $1 it costs."""
        self.name = "Crucible"
        self.cost = 4

    def special(self, game, player):
        card = player.plr_trash_card(force=True)
        player.output(f"Gained {card[0].cost} coin")
        player.coins.add(card[0].cost)


###############################################################################
class Test_Crucible(unittest.TestCase):
    """Test Crucible"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Crucible"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Crucible")

    def test_play(self):
        """Play a salvage"""
        self.plr.piles[Piles.HAND].set("Duchy", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
