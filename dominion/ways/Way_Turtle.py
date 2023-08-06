#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Turtle"""

import unittest
from dominion import Card, Game, Way


###############################################################################
class Way_Turtle(Way.Way):
    """Turtle"""

    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = (
            "Set this aside. If you did, play it at the start of your next turn."
        )
        self.name = "Way of the Turtle"

    def special_way(self, game, player, card):
        player.defer_card(card)
        return {"discard": False}


###############################################################################
class Test_Turtle(unittest.TestCase):
    """Test Turtle"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Turtle"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Turtle"]

    def test_play(self):
        """Perform a Turtle"""
        self.plr.add_card(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(len(self.plr.hand), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
