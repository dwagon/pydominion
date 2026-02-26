#!/usr/bin/env python
"""Tests for NaiveBotPlayer."""

import unittest

from dominion import Action, Game, Piles
from dominion.NaiveBotPlayer import NaiveBotPlayer
from dominion.Option import Option


###############################################################################
class TestNaiveBotPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, naivebot=1, initcards=["Village", "Throne Room"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.assertIsInstance(self.plr, NaiveBotPlayer)

    def test_user_input_prefers_throne_room(self) -> None:
        village = self.g.card_instances["Village"]
        throne_room = self.g.card_instances["Throne Room"]
        options = [
            Option(selector="0", action=Action.QUIT, card=None),
            Option(selector="a", action=Action.PLAY, card=village),
            Option(selector="b", action=Action.PLAY, card=throne_room),
        ]
        picked = self.plr.user_input(options, "prompt")
        self.assertEqual(picked["card"].name, "Throne Room")

    def test_user_input_ignores_spendall(self) -> None:
        copper = self.g.card_instances["Copper"]
        options = [
            Option(selector="0", action=Action.QUIT, card=None),
            Option(selector="1", action=Action.SPENDALL, card=None),
            Option(selector="2", action=Action.SPEND, card=copper),
        ]
        picked = self.plr.user_input(options, "prompt")
        self.assertEqual(picked["action"], Action.SPEND)

    def test_user_input_prefers_end_phase_over_buying_curse(self) -> None:
        curse = self.g.card_mapping["BaseCard"]["Curse"]()
        options = [
            Option(selector="0", action=Action.QUIT, card=None),
            Option(selector="a", action=Action.BUY, card=curse),
        ]
        picked = self.plr.user_input(options, "prompt")
        self.assertEqual(picked["action"], Action.QUIT)

    def test_card_sel_discard_picks_victory(self) -> None:
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Silver")
        picked = self.plr.card_sel(num=1, verbs=("Discard", "Undiscard"))
        self.assertEqual(len(picked), 1)
        self.assertEqual(picked[0].name, "Estate")

    def test_card_sel_discard_can_choose_none(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper", "Gold")
        picked = self.plr.card_sel(num=1, verbs=("Discard", "Undiscard"))
        self.assertEqual(picked, [])

    def test_card_sel_trash_force_picks_cheapest(self) -> None:
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        picked = self.plr.card_sel(num=1, force=True, verbs=("Trash", "Untrash"))
        self.assertEqual(len(picked), 1)
        self.assertEqual(picked[0].name, "Silver")

    def test_card_sel_gain_avoids_curse(self) -> None:
        curse = self.g.card_mapping["BaseCard"]["Curse"]()
        estate = self.g.card_instances["Estate"]
        picked = self.plr.card_sel(num=1, cardsrc=[curse, estate], verbs=("Get", "Unget"))
        self.assertEqual(len(picked), 1)
        self.assertEqual(picked[0].name, "Estate")

    def test_plr_choose_options_trash_boolean(self) -> None:
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        picked = self.plr.plr_choose_options(
            "Trash a card to buy a card?",
            ("Don't trash cards", False),
            ("Trash a card", True),
        )
        self.assertFalse(picked)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
