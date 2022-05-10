#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Architects%27_Guild"""

import unittest
from dominion import Card, Game, Ally


###############################################################################
class Ally_Architects_Guild(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = "When you gain a card, you may spend 2 Favors to gain a cheaper non-Victory card."
        self.name = "Architects Guild"

    def hook_gain_card(self, game, player, card):
        if player.get_favors() < 2:
            return
        player.add_favors(-2)  # To stop re-triggering before favors are spent
        crd = player.plr_gain_card(
            cost=card.cost - 1,
            types={Card.TYPE_ACTION: True, Card.TYPE_TREASURE: True},
            prompt=f"Spend 2 favors to gain a card worth {card.cost-1} or less",
        )
        if not crd:
            player.add_favors(2)


###############################################################################
class Test_Architects_Guild(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, ally="Architects Guild", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        """Play and gain a card"""
        self.plr.set_favors(2)
        self.plr.test_input = ["Get Silver"]
        self.plr.gain_card("Gold")
        self.assertIn("Silver", self.plr.discardpile)
        self.assertEqual(self.plr.get_favors(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
