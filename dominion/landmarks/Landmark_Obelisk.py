#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Obelisk"""
import random
import unittest

from dominion import Card, Game, Landmark, Player

OBELISK = "obelisk"


###############################################################################
class Landmark_Obelisk(Landmark.Landmark):
    """Obelisk"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Obelisk"

    def dynamic_description(self, player: "Player.Player") -> str:  # pragma: no coverage
        if player.game.specials[OBELISK]:
            return f"When scoring, 2VP per card you have from the {player.game.specials[OBELISK]} pile."
        return "When scoring, 2VP per card you have from the chosen pile."

    def hook_end_of_game(self, game: Game.Game, player: Player.Player) -> None:
        for card in player.all_cards():
            if card.name == game.specials[OBELISK]:
                player.add_score("Obelisk", 2)

    def setup(self, game: Game.Game) -> None:
        """Setup: Choose a random Action Supply pile."""
        card_pile = random.choice(game.get_action_piles())
        game.specials[OBELISK] = card_pile


###############################################################################
class Test_Obelisk(unittest.TestCase):
    """Test Obelisk"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            landmarks=["Obelisk"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Use Obelisk"""
        chosen = self.g.specials[OBELISK]
        card = self.g.get_card_from_pile(chosen)
        self.plr.pickup_card(card)
        self.plr.pickup_card(card)

        self.plr.game_over()
        self.g.print_state()
        self.assertEqual(self.plr.get_score_details()["Obelisk"], 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
