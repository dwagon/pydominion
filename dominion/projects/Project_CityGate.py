#!/usr/bin/env python
import contextlib
import unittest

from dominion import Card, Game, Piles, Project, Player, NoCardException


###############################################################################
class Project_CityGate(Project.Project):
    def __init__(self) -> None:
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, +1 Card, then put a card from your hand onto your deck."
        self.name = "City Gate"
        self.cost = 3

    def hook_start_turn(self, game: Game.Game, player: Player.Player) -> None:
        with contextlib.suppress(NoCardException):
            player.pickup_card()
        card = player.card_sel(
            force=True,
            cardsrc=Piles.HAND,
            prompt="Put a card from your hand onto your deck",
        )
        player.add_card(card[0], "topdeck")
        player.piles[Piles.HAND].remove(card[0])


###############################################################################
class TestCityGate(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["City Gate"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        self.plr.assign_project("City Gate")
        self.plr.piles[Piles.DECK].set("Gold")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Province", "Silver", "Duchy")
        self.plr.test_input = ["Select Province"]
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DECK][-1].name, "Province")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
