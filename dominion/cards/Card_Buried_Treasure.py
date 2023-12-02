#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Buried_Treasure"""

import unittest

from dominion import Game, Card, Piles, OptionKeys, Player


###############################################################################
class Card_BuriedTreasure(Card.Card):
    """Buried Treasure"""

    def __init__(self) -> None:
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

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, str]:
        """When you gain this, play it."""
        return {OptionKeys.DESTINATION: Piles.DURATION}


###############################################################################
class TestBuriedTreasure(unittest.TestCase):
    """Test Buried Treasure"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Buried Treasure", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Buried Treasure")

    def test_gain_card(self) -> None:
        """Gain a card"""
        self.plr.gain_card("Buried Treasure")
        self.assertIn("Buried Treasure", self.plr.piles[Piles.DURATION])

    def test_duration(self) -> None:
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
