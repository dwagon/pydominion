#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/League_of_Shopkeepers"""

import unittest
from dominion import Card, Game, Piles, Ally


###############################################################################
class Ally_League_Shopkeepers(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = """After playing a Liaison, if you have 5 or more Favors, +$1;
            and if 10 or more, +1 Action and +1 Buy."""
        self.name = "League of Shopkeepers"

    def hook_post_action(self, game, player, card):  # pylint: disable=no-self-use
        if not card.isLiaison():
            return
        if player.favors.get() >= 5:
            player.coins.add(1)
        if player.favors.get() >= 10:
            player.add_actions(1)
            player.buys.add(1)


###############################################################################
class Test_League_Shopkeepers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, ally="League of Shopkeepers", initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Underling"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_one(self):
        self.plr.favors.set(1)
        cns = self.plr.coins.get()
        acts = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cns)
        self.assertEqual(self.plr.actions.get(), acts)
        self.assertEqual(self.plr.buys.get(), buys)

    def test_play_six(self):
        self.plr.favors.set(6)
        cns = self.plr.coins.get()
        acts = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cns + 1)
        self.assertEqual(self.plr.actions.get(), acts)
        self.assertEqual(self.plr.buys.get(), buys)

    def test_play_eleven(self):
        self.plr.favors.set(11)
        cns = self.plr.coins.get()
        acts = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), cns + 1)
        self.assertEqual(self.plr.actions.get(), acts + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
