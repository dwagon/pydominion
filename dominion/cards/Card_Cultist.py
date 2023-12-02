#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys, NoCardException


###############################################################################
class Card_Cultist(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.LOOTER,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+2 Cards; Each other player gains a Ruins. You may play
            a Cultist from your hand.  When you trash this, +3 Cards."""
        self.name = "Cultist"
        self.cost = 5
        self.cards = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other play gains a Ruins. You may play a Cultist
        from your hand."""
        for plr in player.attack_victims():
            plr.output(f"Gained a ruin from {player}'s Cultist")
            try:
                plr.gain_card("Ruins")
            except NoCardException:
                player.output("No more Ruins")

        if cultist := player.piles[Piles.HAND]["Cultist"]:
            if player.plr_choose_options(
                "Play another cultist?",
                ("Don't play cultist", False),
                ("Play another cultist", True),
            ):
                player.play_card(cultist, cost_action=False)

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        """When you trash this, +3 cards"""
        player.pickup_cards(3)
        return {}


###############################################################################
class TestCultist(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Cultist", "Moat"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g.get_card_from_pile("Cultist")

    def test_play(self) -> None:
        """Play a cultists - should give 2 cards"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 1)
        self.assertTrue(self.victim.piles[Piles.DISCARD][0].isRuin())

    def test_defense(self) -> None:
        """Make sure moats work against cultists"""
        self.plr.add_card(self.card, Piles.HAND)
        moat = self.g.get_card_from_pile("Moat")
        self.victim.add_card(moat, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)
        self.assertTrue(self.victim.piles[Piles.DISCARD].is_empty())

    def test_no_other(self) -> None:
        """Don't ask to play another cultist if it doesn't exist"""
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.test_input, ["0"])

    def test_another_cultist_no(self) -> None:
        """Don't play the other cultist"""
        self.plr.piles[Piles.HAND].set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)

    def test_another_cultist_yes(self) -> None:
        """Another cultist can be played for free"""
        self.plr.piles[Piles.HAND].set("Cultist", "Estate", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 2)
        self.assertEqual(self.plr.actions.get(), 0)
        for c in self.plr.piles[Piles.PLAYED]:
            self.assertEqual(c.name, "Cultist")
        self.assertEqual(self.victim.piles[Piles.DISCARD].size(), 2)
        for c in self.victim.piles[Piles.DISCARD]:
            self.assertTrue(c.isRuin())

    def test_trash(self) -> None:
        """Trashing a cultist should give 3 more cards"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.trash_card(self.card)
        self.assertIn("Cultist", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
