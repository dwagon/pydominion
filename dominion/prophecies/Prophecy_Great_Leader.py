#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Great_Leader"""

import unittest

from dominion import Card, Game, Prophecy, Player, OptionKeys


###############################################################################
class Prophecy_Great_Leader(Prophecy.Prophecy):
    def __init__(self) -> None:
        Prophecy.Prophecy.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = " After each Action card you play, +1 Action."
        self.name = "Great Leader"

    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, str]:
        if card.isAction():
            player.actions.add(1)
        return {}


###############################################################################
class Test_Great_Leader(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, prophecy=["Great Leader"], initcards=["Mountain Shrine", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.g.reveal_prophecy()

    def test_play(self) -> None:
        """Play when prophecy active"""
        moat = self.g.get_card_from_pile("Moat")
        actions = self.plr.actions.get()
        self.plr.play_card(moat)
        self.assertEqual(self.plr.actions.get(), actions)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
