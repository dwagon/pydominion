#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Project, Player

STARCHART = "star chart"


###############################################################################
class Project_StarChart(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you shuffle, you may pick one of the cards to go on top."
        self.name = "Star Chart"
        self.cost = 3

    def hook_pre_shuffle(self, game: Game.Game, player: Player.Player) -> None:
        names = {_.name for _ in player.piles[Piles.DISCARD]}
        choices = []
        for name in names:
            choices.append((f"Put {name} on top", name))
        if not choices:
            player.output("No suitable cards")
            return
        opt = player.plr_choose_options("Pick a card to put on top of your deck", *choices)
        if card := player.piles[Piles.DISCARD][opt]:
            player.specials[STARCHART] = card
            player.secret_count += 1

    def hook_post_shuffle(self, game: Game.Game, player: Player.Player) -> None:
        if card := player.specials.get(STARCHART):
            player.move_card(card, Piles.TOPDECK)
            player.secret_count -= 1


###############################################################################
class TestStarChart(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["Star Chart"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        self.plr.assign_project("Star Chart")
        self.plr.piles[Piles.DISCARD].set("Copper", "Copper", "Silver", "Gold", "Estate", "Gold")
        self.plr.piles[Piles.DECK].set()
        self.plr.test_input = ["Put Gold"]
        c = self.plr.next_card()
        self.assertEqual(c.name, "Gold")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
