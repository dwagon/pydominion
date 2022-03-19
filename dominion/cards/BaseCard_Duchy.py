#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Duchy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.DOMINION
        self.desc = "3 VP"
        self.playable = False
        self.basecard = True
        self.name = "Duchy"
        self.cost = 5
        self.victory = 3

    def calc_numcards(self, game):
        if game.numplayers == 2:
            return 8
        return 12

    def hook_gain_this_card(self, game, player):
        if "Duchess" in game:
            duchess = player.plr_choose_options(
                "Gain a Duchess as well?", ("No thanks", False), ("Gain Duchess", True)
            )
            if duchess:
                player.gain_card("Duchess")
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return False  # Don't gain a duchess


###############################################################################
class Test_Duchy(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Duchy"].remove()

    def test_have(self):
        self.plr.add_card(self.card)
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Duchy"], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
