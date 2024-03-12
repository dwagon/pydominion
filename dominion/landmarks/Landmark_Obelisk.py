#!/usr/bin/env python

import random
import unittest
from typing import Optional
from dominion import Card, Game, Landmark, Player


###############################################################################
class Landmark_Obelisk(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Obelisk"
        self._chosen: Optional[str] = None

    def dynamic_description(self, player: "Player.Player") -> str:  # pragma: no coverage
        if self._chosen:
            return f"When scoring, 2VP per card you have from the {self._chosen} pile."
        else:
            return "When scoring, 2VP per card you have from the chosen pile."

    def hook_end_of_game(self, game: Game.Game, player: Player.Player) -> None:
        for card in player.all_cards():
            if card.name == self._chosen:
                player.add_score("Obelisk", 2)

    def setup(self, game: Game.Game) -> None:
        card_pile = random.choice(game.get_action_piles())
        self._chosen = card_pile


###############################################################################
class Test_Obelisk(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            landmarks=["Obelisk"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Use Obelisk"""
        chosen = self.g.landmarks["Obelisk"]._chosen  # type: ignore
        card = self.g.get_card_from_pile(chosen)
        self.plr.pickup_card(card)
        self.plr.pickup_card(card)

        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Obelisk"], 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
