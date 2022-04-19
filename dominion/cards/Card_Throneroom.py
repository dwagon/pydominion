#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Throneroom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "Play action twice"
        self.name = "Throne Room"
        self.cost = 4

    def special(self, game, player):
        """You may chose an Action card in your hand. Play it twice"""
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for c in player.hand:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s twice" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        if index == 1:
            return
        o = player.user_input(options, "Play which action card twice?")
        if not o["card"]:
            return
        for i in range(1, 3):
            player.output("Number %d play of %s" % (i, o["card"].name))
            player.play_card(o["card"], discard=False, costAction=False)
        player.discard_card(o["card"])


###############################################################################
class Test_Throneroom(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Throne Room", "Mine"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_action(self):
        # Test by playing mine twice on a copper. Cu -> Ag -> Au
        self.plr.set_hand("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", "hand")
        self.plr.test_input = ["1", "1", "1"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.hand[0].name, "Gold")
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.discardpile[0].name, "Mine")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.get_actions(), 0)

    def test_donothing(self):
        self.plr.set_hand("Copper", "Mine")
        card = self.plr.gain_card("Throne Room", "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(card)

    def test_noaction(self):
        self.plr.set_hand("Copper", "Copper")
        card = self.plr.gain_card("Throne Room", "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(card)
        self.assertEqual(self.plr.test_input, ["0"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
