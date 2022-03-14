#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Kingscourt(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.desc = "You may play an Action card from your hand three times."
        self.name = "King's Court"
        self.cost = 7
        self.base = Game.PROSPERITY

    def special(self, game, player):
        """You may chose an Action card in your hand. Play it three times"""
        actions = [_ for _ in player.hand if _.isAction()]
        if not actions:
            player.output("No action cards to repeat")
            return
        index = 1
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        for c in actions:
            sel = "%d" % index
            pr = "Play %s thrice" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        o = player.user_input(options, "Play which action card three times?")
        if not o["card"]:
            return
        player.hand.remove(o["card"])
        for i in range(1, 4):
            player.output("Number %d play of %s" % (i, o["card"].name))
            player.card_benefits(o["card"])
        player.add_card(o["card"], "played")


###############################################################################
class Test_Kingscourt(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["King's Court", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["King's Court"].remove()

    def test_play(self):
        self.plr.set_deck("Estate", "Estate", "Gold", "Gold", "Duchy", "Duchy")
        self.plr.set_hand("Moat", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["play moat"]
        self.plr.play_card(self.card)
        # (moat + 2) * 3 + estate
        self.assertEqual(self.plr.hand.size(), 2 * 3 + 1)
        self.assertEqual(self.plr.played.size(), 2)
        for c in self.plr.played:
            if c.name == "Moat":
                break
        else:  # pragma: no cover
            self.fail("Didn't put moat in played")
        for c in self.plr.played:
            if c.name == "King's Court":
                break
        else:  # pragma: no cover
            self.fail("Didn't put moat in played")

    def test_noactions(self):
        self.plr.set_hand("Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 0)
        self.assertEqual(self.plr.played.size(), 1)

    def test_picked_nothing(self):
        """Selected no actions with Kings court"""
        self.plr.set_hand("Estate", "Estate", "Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["don't play"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 0)
        self.assertEqual(self.plr.played.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
