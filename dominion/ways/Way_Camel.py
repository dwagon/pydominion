#!/usr/bin/env python

import unittest

from dominion import Card, Game, Way, Piles, Player


###############################################################################
class Way_Camel(Way.Way):
    def __init__(self) -> None:
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Exile a Gold from the Supply."
        self.name = "Way of the Camel"

    def special(self, game: Game.Game, player: Player.Player) -> None:
        player.exile_card_from_supply("Gold")


###############################################################################
class TestCamel(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Camel"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Camel"]

    def test_play(self) -> None:
        """Perform a Camel"""
        assert self.card is not None
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertIn("Gold", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
