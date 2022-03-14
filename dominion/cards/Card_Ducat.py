#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Ducat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.RENAISSANCE
        self.buys = 1
        self.name = "Ducat"
        self.cost = 2

    ###########################################################################
    def desc(self, player):
        if player.phase == "buy":
            return "+1 Coffers; +1 Buy; When you gain this, you may trash a Copper from your hand."
        return "+1 Coffers; +1 Buy"

    ###########################################################################
    def special(self, game, player):
        player.add_coffer()

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        cu = player.in_hand("Copper")
        if cu:
            player.plr_trash_card(cardsrc=[cu], num=1)
        else:
            player.output("No Coppers")


###############################################################################
class Test_Ducat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Ducat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        card = self.g["Ducat"].remove()
        self.plr.set_coffers(0)
        self.plr.add_card(card, "hand")
        self.plr.play_card(card)
        self.assertEqual(self.plr.get_coffers(), 1)
        self.assertEqual(self.plr.get_buys(), 1 + 1)

    def test_gain_trash(self):
        self.plr.test_input = ["Copper"]
        self.plr.set_hand("Copper")
        self.plr.gain_card("Ducat")

    def test_gain_nothing(self):
        self.plr.set_hand("Silver")
        self.plr.gain_card("Ducat")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
