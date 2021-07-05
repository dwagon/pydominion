#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Butterfly """

import unittest
import Game
from Way import Way


###############################################################################
class Way_Butterfly(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "You may return this to its pile to gain a card costing exactly $1 more than it."
        self.name = "Way of the Butterfly"

    def special_way(self, game, player, card):
        game[card.name].add()
        cst = player.cardCost(card)
        player.plrGainCard(cst + 1, "equal")
        return {"discard": False}


###############################################################################
class Test_Butterfly(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            waycards=["Way of the Butterfly"],
            initcards=["Moat", "Witch"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Butterfly"]

    def test_play(self):
        """Perform a Butterfly"""
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Get Witch"]
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.plr.in_discard("Witch"))
        self.assertEqual(self.g["Moat"].stack_size(), 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
