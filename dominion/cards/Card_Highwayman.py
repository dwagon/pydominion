#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Highwayman"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Highwayman(Card.Card):
    """Highwayman"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.ATTACK,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.desc = """ At the start of your next turn, discard this from play and +3 Cards.
Until then, the first Treasure each other player plays each turn does nothing."""
        self.name = "Highwayman"
        self.cost = 5

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, str]:
        """discard this from play and +3 Cards."""
        player.pickup_cards(3)
        return {}

    def hook_all_players_pre_play(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """Until then the first Treasure each other player plays each turn does nothing."""
        if not card.isTreasure():
            return {}
        if player == owner:
            return {}
        treas_played = any(True for _ in player.piles[Piles.PLAYED] if _.isTreasure())
        if treas_played:
            return {}
        player.output(f"{owner}'s Highwayman cancel your {card}")
        owner.output(f"{player}'s {card} was cancelled")

        return {OptionKeys.SKIP_CARD: True}


###############################################################################
class TestHighwayman(unittest.TestCase):
    """Test Highwayman"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Highwayman"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Highwayman")

    def test_play(self) -> None:
        """Play Card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.victim.piles[Piles.HAND].set("Estate", "Silver", "Gold")

        gold = self.victim.piles[Piles.HAND]["Gold"]
        assert gold is not None
        self.victim.play_card(gold)
        self.assertIn("Gold", self.victim.piles[Piles.PLAYED])
        self.assertEqual(self.victim.coins.get(), 0)

        silver = self.victim.piles[Piles.HAND]["Silver"]
        assert silver is not None
        self.victim.play_card(silver)
        self.assertEqual(self.victim.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
