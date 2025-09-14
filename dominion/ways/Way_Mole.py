#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Way_of_the_Mole"""

import unittest

from dominion import Card, Game, Way, Piles, Player


###############################################################################
class Way_Mole(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Action; Discard your hand. +3 Cards."
        self.actions = 1
        self.name = "Way of the Mole"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        player.discard_hand({})
        player.pickup_cards(3)


###############################################################################
class Test_Mole(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Mole"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Mole"]

    def test_play(self):
        """Perform a Mole"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
