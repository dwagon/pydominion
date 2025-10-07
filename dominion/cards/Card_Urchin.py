#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Urchin(Card.Card):
    """Urchin"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card; +1 Action; Each other player discards down to 4 cards.
            When you play another Attack card with this in play, you may trash this.
            If you do, gain a Mercenary."""
        self.name = "Urchin"
        self.required_cards = [("Card", "Mercenary")]
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        for plr in player.attack_victims():
            plr.output(f"Discard down to 4 cards from {player.name}'s Urchin")
            plr.plr_discard_down_to(4)

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        attacks = sum(1 for card in player.piles[Piles.PLAYED] if card.isAttack())
        if attacks >= 2:
            if player.plr_choose_options(
                "Trash the urchin?",
                ("Keep the Urchin", False),
                ("Trash and gain a Mercenary", True),
            ):
                player.trash_card(self)
                player.gain_card("Mercenary")
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    num_to_discard = len(player.piles[Piles.HAND]) - 4
    return player.pick_to_discard(num_to_discard)


###############################################################################
class TestUrchin(unittest.TestCase):
    """Test Urchin"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Urchin", "Militia"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Urchin")

    def test_play(self) -> None:
        """Play an Urchin"""
        self.plr.add_card(self.card, Piles.HAND)
        self.victim.test_input = ["1", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.victim.piles[Piles.HAND].size(), 4)

    def test_mercenary(self) -> None:
        """Play an Urchin and get a mercenary"""
        self.plr.piles[Piles.PLAYED].set("Urchin", "Militia")
        for crd in self.plr.piles[Piles.PLAYED]:
            crd.player = self.plr
        self.plr.test_input = ["end phase", "end phase", "mercenary"]
        self.plr.turn()
        self.assertIn("Mercenary", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Urchin", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
