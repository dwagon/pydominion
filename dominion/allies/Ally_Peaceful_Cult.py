#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Peaceful_Cult """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Peaceful_Cult(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """At the start of your Buy phase, you may spend
            any number of Favors to trash that many cards from your hand."""
        self.name = "Peaceful Cult"

    def hook_pre_buy(self, game, player):
        if not player.get_favors():
            return
        player.output("Use Peaceful Cult to trash a card per favor")
        trshed = player.plrTrashCard(num=player.get_favors())
        player.add_favors(-1 * len(trshed))


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Peaceful_Cult(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, ally="Peaceful Cult", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.set_hand("Copper", "Silver", "Gold")
        self.plr.setFavor(2)
        self.plr.test_input = ["Trash Copper", "Finish", "End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.get_favors(), 1)
        self.assertTrue(self.g.in_trash("Copper"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
