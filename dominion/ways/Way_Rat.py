#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Way_of_the_Rat """

import unittest
from dominion import Game
from dominion import Way


###############################################################################
class Way_Rat(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "You may discard a Treasure to gain a copy of this."
        self.name = "Way of the Rat"

    def special_way(self, game, player, card):
        treas = [_ for _ in player.hand if _.isTreasure()]
        if not treas:
            player.output("No treasures to discard")
            return
        t_to_disc = player.card_sel(prompt="Select Treasure to discard", cardsrc=treas)
        if not t_to_disc:
            return
        player.discard_card(t_to_disc[0])
        player.gain_card(card.name)


###############################################################################
class Test_Rat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            waycards=["Way of the Rat"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Rat"]

    def test_play(self):
        """Perform a Rat"""
        self.plr.set_hand("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Copper"]
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.plr.discardpile["Moat"])
        self.assertIsNotNone(self.plr.discardpile["Copper"])
        self.assertIn("Moat", self.plr.played)
        self.assertNotIn("Copper", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
