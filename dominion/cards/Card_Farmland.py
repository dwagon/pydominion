#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Farmland(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.HINTERLANDS
        self.desc = """2VP; When you buy this, trash a card from your hand.
            Gain a card costing exactly 2 more than the trashed card."""
        self.name = "Farmland"
        self.cost = 6
        self.victory = 2

    def hook_gain_this_card(self, game, player):
        c = player.plrTrashCard(force=True)
        player.plrGainCard(cost=c[0].cost + 2, modifier="equal")
        return {}


###############################################################################
class Test_Farmland(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            initcards=["Farmland", "Militia"],
            badcards=["Death Cart", "Cemetery", "Blessed Village"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Farmland"].remove()

    def test_gain(self):
        """Gain a farmland"""
        try:
            tsize = self.g.trashSize()
            self.plr.set_hand("Estate", "Duchy")
            self.plr.test_input = ["Trash Estate", "Get Militia"]
            self.plr.gain_card("Farmland")
            self.assertEqual(self.g.trashSize(), tsize + 1)
            self.assertEqual(self.plr.hand.size(), 1)
            # 1 for farmland, 1 for gained card
            self.assertEqual(self.plr.discardpile.size(), 2)
        except (AssertionError, IOError):  # pragma: no cover
            self.g.print_state()
            raise

    def test_score(self):
        self.plr.set_deck("Farmland")
        sd = self.plr.get_score_details()
        self.assertEqual(sd["Farmland"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
