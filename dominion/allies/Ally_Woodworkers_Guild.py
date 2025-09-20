#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Woodworkers_Guild"""

import unittest

from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_Woodworkers_Guild(Ally.Ally):
    """Woodworkers Guild"""

    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """At the start of your Buy phase, you may spend a Favor to
        trash an Action card from your hand. If you did, gain an Action card."""
        self.name = "Woodworkers' Guild"

    def hook_pre_buy(self, game, player):
        if player.favors.get() == 0:
            return
        actions = [_ for _ in player.piles[Piles.HAND] if _.isAction()]
        if not actions:
            return
        spend = player.plr_choose_options(
            "Spend a favor to trash an action card to gain any action card",
            ("Do nothing", False),
            ("Spend favor", True),
        )
        if not spend:
            return
        trash = player.plr_trash_card(cardsrc=actions)
        if not trash:
            return
        player.favors.add(-1)
        player.plr_gain_card(
            cost=99,
            ignore_debt=True,
            ignore_potcost=True,
            types={Card.CardType.ACTION: True},
        )


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pylint: disable=unused-argument
    """Bot response - just do nothing"""
    return False


###############################################################################
class Test_Woodworkers_Guild(unittest.TestCase):
    """Test Woodworkers Guild"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, allies="Woodworkers' Guild", initcards=["Underling", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card(self):
        """Play and gain a card"""
        self.plr.piles[Piles.HAND].set("Underling")
        self.plr.favors.set(2)
        self.plr.test_input = [
            "Spend favor",
            "Trash Underling",
            "Get Moat",
            "End Phase",
        ]
        self.plr.buy_phase()
        self.assertIn("Underling", self.g.trash_pile)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.favors.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
