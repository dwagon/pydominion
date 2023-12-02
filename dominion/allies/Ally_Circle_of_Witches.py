#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Circle_of_Witches"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player, NoCardException, OptionKeys


###############################################################################
class Ally_Circle_of_Witches(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = "After playing a Liaison, you may spend 3 Favors to have each other player gain a curse"
        self.required_cards = ["Curse"]
        self.name = "Circle of Witches"

    def hook_post_play(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if player.favors.get() < 3:
            return {}
        if not card.isLiaison():
            return {}
        if player.plr_choose_options(
            "Spend three favors to Curse everyone else: ",
            ("Nope, I'll be nice", False),
            ("Curse them", True),
        ):
            player.favors.add(-3)
            for plr in game.player_list():
                if plr != player:
                    try:
                        plr.gain_card("Curse")
                        plr.output(f"{player}'s {self} cursed you")
                    except NoCardException:
                        player.output("No more Curses")
        return {}


###############################################################################
class TestCircleOfWitches(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, allies="Circle of Witches", initcards=["Underling", "Moat"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_card(self) -> None:
        """Play a liaison and curse"""
        self.plr.favors.set(4)
        card = self.g.get_card_from_pile("Underling")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Curse"]
        self.plr.play_card(card)
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])
        self.assertEqual(self.plr.favors.get(), 1 + 1)  # +1 for playing underling


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
