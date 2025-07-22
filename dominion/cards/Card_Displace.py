#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Displace"""

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Displace(Card.Card):
    """Displace"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Exile a card from your hand. Gain a differently named card
            costing up to 2 Coin more than it."""
        self.name = "Displace"
        self.cost = 5

    def special(self, game, player):
        if crd := player.card_sel(
            prompt="Exile a card to gain a different one costing 2 more",
            verbs=("Exile", "Unexile"),
        ):
            player.exile_card(crd[0])
            player.plr_gain_card(cost=crd[0].cost + 2, exclude=[crd[0].name])


###############################################################################
class Test_Displace(unittest.TestCase):
    """Test Displace"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Displace"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Displace")

    def test_playcard(self):
        """Play a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Exile Copper", "Get Estate"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.EXILE])
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
