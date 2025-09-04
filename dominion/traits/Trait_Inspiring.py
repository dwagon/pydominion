#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Inspiring"""
import unittest
from typing import Any

from dominion import Card, Game, Trait, Player, OptionKeys, Piles


###############################################################################
class Trait_Inspiring(Trait.Trait):
    def __init__(self):
        Trait.Trait.__init__(self)
        self.cardtype = Card.CardType.TRAITS
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """After playing an Inspiring card on your turn,
        you may play an Action from your hand that you don't have a copy of in play."""
        self.name = "Inspiring"

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        if not self.isTraitCard(game, card):
            return {}
        actions = get_suitable_actions(player)
        if not actions:
            player.output("No suitable cards for Inspiring")
            return {}
        choices: list[tuple[str, Any]] = [("Do nothing", None)]
        for card in actions:
            choices.append((f"Play {card}", card))

        if choice := player.plr_choose_options("Use Inspiring to play which action?", *choices):
            player.play_card(choice, cost_action=False)
        return {}


###############################################################################
def get_suitable_actions(player: "Player.Player") -> list[Card.Card]:
    return [_ for _ in player.piles[Piles.HAND] if _.isAction() and _.name not in player.piles[Piles.PLAYED]]


###############################################################################
class Test_Inspiring(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=1, traits=["Inspiring"], initcards=["Moat", "Market"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.assign_trait("Inspiring", "Moat")

    def test_play(self) -> None:
        moat = self.g.get_card_from_pile("Moat")
        self.plr.piles[Piles.HAND].set("Market")
        self.plr.add_card(moat, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Play Market"]
        self.plr.play_card(moat)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertIn("Market", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 + 1 - 2)  # +2 Moat, +1 Market, -2 Played

    def test_play_no_actions(self) -> None:
        moat = self.g.get_card_from_pile("Moat")
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Silver")
        self.plr.add_card(moat, Piles.HAND)
        hand_size = len(self.plr.piles[Piles.HAND])
        self.plr.test_input = ["Play Market"]
        self.plr.play_card(moat)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Market", self.plr.piles[Piles.PLAYED])
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 2 - 1)  # +2 Moat, -1 Played
        self.assertIn("No suitable cards for Inspiring", self.plr.messages)

    def test_already_played(self):
        self.plr.piles[Piles.HAND].set("Copper", "Market")
        self.plr.piles[Piles.PLAYED].set("Silver", "Market")
        actions = get_suitable_actions(self.plr)
        self.assertEqual(actions, [])

    def test_no_actions(self):
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Silver", "Market")
        actions = get_suitable_actions(self.plr)
        self.assertEqual(actions, [])

    def test_actions(self):
        self.plr.piles[Piles.HAND].set("Copper", "Moat")
        self.plr.piles[Piles.PLAYED].set("Silver", "Market")
        actions = get_suitable_actions(self.plr)
        self.assertEqual(actions[0].name, "Moat")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
