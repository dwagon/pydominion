#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Counterfeit(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.DARKAGES
        self.desc = "+1 Coin, +1 Buy; May play a treasure twice and trash it"
        self.name = "Counterfeit"
        self.cost = 5
        self.coin = 1
        self.buys = 1

    def special(self, game, player):
        """When you play this, you may play a Treasure from your
        hand twice. If you do, trash that Treasure"""
        options = [{"selector": "0", "print": "Do nothing", "card": None}]
        index = 1
        for c in player.hand:
            if c.isTreasure():
                sel = "%d" % index
                index += 1
                options.append(
                    {"selector": sel, "print": "Play %s twice" % c.name, "card": c}
                )
        if index == 1:
            return
        o = player.userInput(options, "What to do?")
        if not o["card"]:
            return
        for _ in range(2):
            player.play_card(o["card"], costAction=False, discard=False)
        player.trash_card(o["card"])


###############################################################################
class Test_Counterfiet(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Counterfeit"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Counterfeit"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_notreasures(self):
        self.plr.set_hand("Estate", "Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.test_input, ["0"])

    def test_twice(self):
        self.plr.set_hand("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertTrue(self.plr.hand.is_empty())
        self.assertIsNotNone(self.g.in_trash("Gold"))
        # CF + 2 * Gold
        self.assertEqual(self.plr.getCoin(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
