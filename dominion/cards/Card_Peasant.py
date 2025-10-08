#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Peasant"""
import unittest
from typing import Optional, Union

from dominion import Game, Piles, Card, Player, PlayArea


###############################################################################
class Card_Peasant(Card.Card):
    """Peasant"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Buy, +1 Coin; Discard to replace with Soldier"
        self.name = "Peasant"
        self.traveller = True
        self.buys = 1
        self.coin = 1
        self.cost = 2

    def hook_discard_this_card(
        self, game: "Game.Game", player: "Player.Player", source: Optional[Union[Piles, "PlayArea.PlayArea"]]
    ) -> None:
        """Replace with Treasure Hunter"""
        player.replace_traveller(self, "Soldier")


###############################################################################
class TestPeasant(unittest.TestCase):
    """Test Peasant"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Peasant"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Peasant")

    def test_play(self):
        """Play a peasant"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
