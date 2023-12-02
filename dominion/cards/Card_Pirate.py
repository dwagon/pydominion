#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Pirate """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Pirate(Card.Card):
    """Pirate"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """At the start of your next turn, gain a Treasure costing up
            to $6 to your hand.
            When any player gains a Treasure, you may play this from your hand."""
        self.name = "Pirate"
        self.cost = 5

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """gain a Treasure costing up to $6 to your hand"""
        # Discard first to avoid the gained card triggering the pirate again
        player.move_card(self, Piles.PLAYED)
        player.plr_gain_card(
            cost=6, types={Card.CardType.TREASURE: True}, destination=Piles.HAND
        )
        return {}

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """When any player gains a Treasure, you may play this from your hand"""
        if not card.isTreasure():
            return {}
        if self.location != Piles.HAND:
            return {}
        owner.output(f"Player {player.name} gained a treasure ({card})")
        gain = owner.plr_choose_options(
            "Do you wish to play your Pirate?",
            ("Do Nothing", False),
            ("Gain a treasure costing up to $6 to your hand", True),
        )
        if not gain:
            return {}
        owner.move_card(self, Piles.PLAYED)
        owner.plr_gain_card(
            cost=6, types={Card.CardType.TREASURE: True}, destination=Piles.HAND
        )
        return {}


###############################################################################
class Test_Pirate(unittest.TestCase):
    """Test Pirate"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Pirate"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Pirate")

    def test_play_card(self) -> None:
        """Play a pirate"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.test_input = ["Get Gold"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Pirate", self.plr.piles[Piles.PLAYED])

    def test_react_treasure(self) -> None:
        """Play a pirate through a reaction"""
        self.plr.piles[Piles.HAND].set("Pirate")
        self.plr.test_input = ["Gain a treasure", "Get Gold"]
        self.oth.gain_card("Silver")
        self.assertIn("Gold", self.plr.piles[Piles.HAND])
        self.assertIn("Pirate", self.plr.piles[Piles.PLAYED])

    def test_react_not_treasure(self) -> None:
        """Play a pirate through a reaction, but not a treasure"""
        self.plr.piles[Piles.HAND].set("Pirate")
        self.plr.test_input = ["Gain a treasure", "Get Gold"]
        self.oth.gain_card("Estate")
        self.assertNotIn("Gold", self.plr.piles[Piles.HAND])
        self.assertNotIn("Pirate", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
