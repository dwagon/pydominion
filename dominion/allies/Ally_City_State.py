#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/City-state """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_CityState(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """When you gain an Action card during your turn, you may spend 2 Favors to play it."""
        self.name = "City State"

    def hook_gain_card(self, game, player, card):
        if not card.isAction():
            return
        if player.get_favors() < 2:
            return
        ch = player.plr_choose_options(
            f"Play {card.name} from City State?",
            ("Do nothing", False),
            ("Play Card", True),
        )
        if ch:
            player.play_card(card, discard=False, costAction=False)
            player.add_favors(-2)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_CityState(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ally="City State",
            initcards=["Underling"],
            use_liaisons=True,
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play card"""
        self.plr.set_hand()
        self.plr.set_favors(2)
        self.plr.set_actions(0)
        self.plr.test_input = ["Play"]
        self.plr.gain_card("Underling")
        self.assertEqual(self.plr.get_favors(), 2 - 2 + 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 1)

    def test_dont_play(self):
        """Dont play card"""
        self.plr.set_hand()
        self.plr.set_favors(2)
        self.plr.set_actions(0)
        self.plr.test_input = ["nothing"]
        self.plr.gain_card("Underling")
        self.assertEqual(self.plr.get_favors(), 2)
        self.assertEqual(self.plr.get_actions(), 0)
        self.assertEqual(self.plr.hand.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
