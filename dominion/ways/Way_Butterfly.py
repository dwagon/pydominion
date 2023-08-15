#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Butterfly """

import unittest
from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Butterfly(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "You may return this to its pile to gain a card costing exactly $1 more than it."
        self.name = "Way of the Butterfly"

    def special_way(self, game, player, card):
        game[card.name].add(card)
        player.remove_card(card)
        cst = player.card_cost(card)
        player.plr_gain_card(cst + 1, "equal")
        return {"discard": False}


###############################################################################
class TestButterfly(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
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
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Get Witch"]
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Witch"])
        self.assertEqual(len(self.g["Moat"]), 10)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
