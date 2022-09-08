#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/League_of_Shopkeepers"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_League_Shopkeepers(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """After playing a Liaison, if you have 5 or more Favors, +$1;
            and if 10 or more, +1 Action and +1 Buy."""
        self.name = "League of Shopkeepers"

    def hook_post_action(self, game, player, card):  # pylint: disable=no-self-use
        if not card.isLiaison():
            return
        if player.get_favors() >= 5:
            player.add_coins(1)
        if player.get_favors() >= 10:
            player.add_actions(1)
            player.add_buys(1)


###############################################################################
class Test_League_Shopkeepers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="League of Shopkeepers", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Underling"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_one(self):
        self.plr.set_favors(1)
        cns = self.plr.get_coins()
        acts = self.plr.get_actions()
        buys = self.plr.get_buys()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), cns)
        self.assertEqual(self.plr.get_actions(), acts)
        self.assertEqual(self.plr.get_buys(), buys)

    def test_play_six(self):
        self.plr.set_favors(6)
        cns = self.plr.get_coins()
        acts = self.plr.get_actions()
        buys = self.plr.get_buys()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), cns + 1)
        self.assertEqual(self.plr.get_actions(), acts)
        self.assertEqual(self.plr.get_buys(), buys)

    def test_play_eleven(self):
        self.plr.set_favors(11)
        cns = self.plr.get_coins()
        acts = self.plr.get_actions()
        buys = self.plr.get_buys()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), cns + 1)
        self.assertEqual(self.plr.get_actions(), acts + 1)
        self.assertEqual(self.plr.get_buys(), buys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
