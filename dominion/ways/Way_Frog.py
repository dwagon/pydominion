#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Frog """

import unittest

from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Frog(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Action; When you discard this from play this turn, put it onto your deck."
        self.actions = 1
        self.name = "Way of the Frog"

    def hook_way_discard_this_card(self, game, player, card):
        player.add_card(card, "topdeck")
        player.piles[Piles.PLAYED].remove(card)


###############################################################################
class Test_Frog(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Frog"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Frog"]

    def test_play(self):
        """Perform a Frog"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.plr.discard_hand()
        self.assertIn("Moat", self.plr.piles[Piles.DECK])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
