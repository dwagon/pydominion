#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Circle_of_Witcches"""

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Circle_of_Witches(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = "After playing a Liaison, you may spend 3 Favors to have each other player gain a curse"
        self.required_cards = ["Curse"]
        self.name = "Circle of Witches"

    def hook_post_action(self, game, player, card):
        if player.get_favors() < 3:
            return
        if not card.isLiaison():
            return
        chc = player.plr_choose_options(
            "Spend three favors to Curse everyone else: ",
            ("Nope, I'll be nice", False),
            ("Curse them", True),
        )
        if chc:
            player.add_favors(-3)
            for plr in game.player_list():
                if plr != player:
                    plr.output(f"{player.name}'s {self.name} cursed you")
                    plr.gain_card("Curse")


###############################################################################
class Test_Circle_of_Witches(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2, ally="Circle of Witches", initcards=["Underling", "Moat"]
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play_card(self):
        """Play a liaison and curse"""
        self.plr.set_favors(4)
        card = self.g["Underling"].remove()
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Curse"]
        self.plr.play_card(card)
        self.assertIn("Curse", self.vic.discardpile)
        self.assertEqual(self.plr.get_favors(), 1 + 1)  # +1 for playing underling


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
