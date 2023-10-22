#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Buried_Treasure"""

import unittest
from typing import Optional

from dominion import Game, Card, Piles


###############################################################################
class Card_BuriedTreasure(Card.Card):
    """Buried Treasure"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "At the start of your next turn, +1 Buy and +$3. When you gain this, play it."
        self.name = "Buried Treasure"
        self.cost = 5

    def duration(self, game, player):
        """At the start of your next turn, +1 Buy and +$3"""
        player.buys.add(1)
        player.coins.add(3)

    def hook_gain_this_card(self, game, player):
        """When you gain this, play it."""
        return {"destination": Piles.DURATION}


###############################################################################
class Test_BuriedTreasure(unittest.TestCase):
    """Test Buried Treasure"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Buried Treasure", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Buried Treasure")

    def test_gain_card(self):
        """Gain a card"""
        self.plr.gain_card("Buried Treasure")
        self.assertIn("Buried Treasure", self.plr.piles[Piles.DURATION])

    def test_duration(self):
        """Duration"""
        self.plr.add_card(self.card, Piles.DURATION)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
