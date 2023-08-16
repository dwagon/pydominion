#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Peaceful_Cult """

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Peaceful_Cult(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your Buy phase, you may spend
            any number of Favors to trash that many cards from your hand."""
        self.name = "Peaceful Cult"

    def hook_pre_buy(self, game, player):
        if not player.favors.get():
            return
        player.output("Use Peaceful Cult to trash a card per favor")
        trshed = player.plr_trash_card(num=player.favors.get())
        player.favors.add(-1 * len(trshed))


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Peaceful_Cult(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="Peaceful Cult", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.favors.set(2)
        self.plr.test_input = ["Trash Copper", "Finish", "End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.favors.get(), 1)
        self.assertIn("Copper", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
