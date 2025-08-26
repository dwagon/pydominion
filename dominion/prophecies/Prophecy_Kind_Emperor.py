#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Kind_Emperor"""
import unittest

from dominion import Card, Game, Prophecy, Player, Piles


###############################################################################
class Prophecy_Kind_Emperor(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "At the start of your turn, and when you remove the last Sun: Gain an Action to your hand."
        self.name = "Kind Emperor"

    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        player.plr_gain_card(
            cost=999,
            types={Card.CardType.ACTION: True},
            force=True,
            ignore_debt=True,
            ignore_potcost=True,
            destination=Piles.HAND,
        )

    def hook_reveal_prophecy(self, game: "Game.Game") -> None:
        for player in game.players.values():
            player.plr_gain_card(
                cost=999,
                types={Card.CardType.ACTION: True},
                force=True,
                ignore_debt=True,
                ignore_potcost=True,
                destination=Piles.HAND,
            )


###############################################################################
class Test_Kind_Emperor(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecies=["Kind Emperor"], initcards=["Mountain Shrine", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play when prophecy active"""
        self.plr.test_input = ["Get Moat", "Get Mountain Shrine"]
        self.g.reveal_prophecy()
        self.plr.piles[Piles.HAND].set()
        self.plr.start_turn()
        self.assertIn("Mountain Shrine", self.plr.piles[Piles.HAND])

    def test_reveal(self) -> None:
        self.plr.test_input = ["Get Mountain Shrine"]
        self.g.reveal_prophecy()
        self.assertIn("Mountain Shrine", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
