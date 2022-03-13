#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fellowship_of_Scribes """

import unittest
from dominion import Game, Ally


###############################################################################
class Ally_Fellowship_of_Scribes(Ally.Ally):
    def __init__(self):
        Ally.Ally.__init__(self)
        self.base = Game.ALLIES
        self.desc = """After playing an Action, if you have 4 or fewer cards in hand, you may spend a Favor for +1 Card."""
        self.name = "Fellowship of Scribes"

    def hook_postAction(self, game, player, card):
        if not player.getFavor():
            return
        if player.hand.size() > 4:
            return
        choice = player.plrChooseOptions(
            "Use Fellowship of Scribes to spend a favor to gain a card?",
            ("Gain a card", "gain"),
            ("No thanks", "no"),
        )
        if choice == "gain":
            player.pickupCard()
            player.addFavor(-1)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class Test_Fellowship_of_Scribes(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            ally="Fellowship of Scribes",
            initcards=["Festival", "Underling"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play and gain a card"""
        self.card = self.g["Festival"].remove()
        self.plr.setHand("Duchy")
        self.plr.addCard(self.card, "hand")
        self.plr.setFavor(2)
        self.plr.test_input = ["Gain"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getFavor(), 1)
        self.assertEqual(self.plr.hand.size(), 1 + 1)

    def test_play_no_gain(self):
        """Play and don't gain a card"""
        self.card = self.g["Festival"].remove()
        self.plr.setHand("Duchy")
        self.plr.addCard(self.card, "hand")
        self.plr.setFavor(2)
        self.plr.test_input = ["No"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getFavor(), 2)
        self.assertEqual(self.plr.hand.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
