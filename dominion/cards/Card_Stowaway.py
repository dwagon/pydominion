#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Stowaway """

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, OptionKeys


###############################################################################
class Card_Stowaway(Card.Card):
    """Stowaway"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.REACTION,
        ]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """At the start of your next turn, +2 Cards.
        When anyone gains a Duration card, you may play this from your hand."""
        self.name = "Stowaway"
        self.cost = 3

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """At the start of your next turn, +2 Cards"""
        player.pickup_cards(2)
        return {}

    def hook_all_players_gain_card(
        self,
        game: Game.Game,
        player: Player.Player,
        owner: Player.Player,
        card: Card.Card,
    ) -> dict[OptionKeys, Any]:
        """When anyone gains a Duration card, you may play this from your hand."""
        if not card.isDuration():
            return {}
        if self.location != Piles.HAND:
            return {}
        owner.output(f"Player {player} gained a duration ({card})")
        if owner.plr_choose_options(
            "Do you wish to play your Stowaway?",
            ("Do Nothing", False),
            ("Play Stowaway to gain two cards", True),
        ):
            owner.pickup_cards(2)
            owner.move_card(self, Piles.PLAYED)
        return {}


###############################################################################
class Test_Stowaway(unittest.TestCase):
    """Test Stowaway"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Stowaway", "Amulet"])
        self.g.start_game()
        self.plr, self.oth = self.g.player_list()
        self.card = self.g.get_card_from_pile("Stowaway")

    def test_play_card(self) -> None:
        """Play a Stowaway"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Stowaway", self.plr.piles[Piles.PLAYED])

    def test_react_duration(self) -> None:
        """Play a Stowaway through a reaction"""
        self.plr.piles[Piles.HAND].set("Stowaway")
        self.plr.test_input = ["Play Stowaway"]
        hand_size = self.plr.piles[Piles.HAND].size()
        self.oth.gain_card("Amulet")
        self.assertEqual(
            self.plr.piles[Piles.HAND].size(), hand_size + 2 - 1
        )  # -1 for playing Stowaway
        self.assertIn("Stowaway", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Stowaway", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
