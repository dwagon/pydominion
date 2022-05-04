#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Duchess(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = """+2 Coin.  Each player (including you) looks at the top card of his deck, and discards it or puts it back."""
        self.name = "Duchess"
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        for plr in game.player_list():
            card = plr.next_card()
            if plr == player:
                name = "your"
            else:
                name = "%s's" % player.name
            keep = plr.plr_choose_options(
                "Due to %s Duchess you can keep or discard the top card" % name,
                ("Keep %s on top of deck" % card.name, True),
                ("Discard %s" % card.name, False),
            )
            if keep:
                plr.add_card(card, "topdeck")
            else:
                plr.output("Discarding %s" % card.name)
                plr.discard_card(card)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    if "Estate" in args[0] or "Duchy" in args[0] or "Province" in args[0]:
        return False
    return True


###############################################################################
class Test_Duchess(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Duchess"].remove()

    def test_play(self):
        """Play duchess - keep on deck"""
        self.plr.set_deck("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["keep"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIsNotNone(self.plr.in_deck("Province"))
        self.assertNotIn("Province", self.plr.discardpile)

    def test_disacrd(self):
        """Play duchess - discard"""
        self.plr.set_deck("Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIsNone(self.plr.in_deck("Province"))
        self.assertIn("Province", self.plr.discardpile)

    def test_buy_duchess(self):
        self.plr.test_input = ["Duchess"]
        self.plr.gain_card("Duchy")
        self.assertIn("Duchess", self.plr.discardpile)
        self.assertIn("Duchy", self.plr.discardpile)

    def test_buy_duchy(self):
        self.plr.test_input = ["No"]
        self.plr.gain_card("Duchy")
        self.assertNotIn("Duchess", self.plr.discardpile)
        self.assertIn("Duchy", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
