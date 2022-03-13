#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Mastermind """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Mastermind(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.MENAGERIE
        self.desc = """At the start of your next turn, you may play an Action card from your hand three times."""
        self.name = "Mastermind"
        self.cost = 5

    def duration(self, game, player):
        options = [{"selector": "0", "print": "Don't play a card", "card": None}]
        index = 1
        for c in player.hand:
            if not c.isAction():
                continue
            sel = "%d" % index
            pr = "Play %s thrice" % c.name
            options.append({"selector": sel, "print": pr, "card": c})
            index += 1
        if index == 1:
            player.output("No action cards to repeat")
            return
        o = player.userInput(options, "Play which action card three times?")
        if not o["card"]:
            return
        for i in range(1, 4):
            player.output("Number %d play of %s" % (i, o["card"].name))
            player.playCard(o["card"], discard=False, costAction=False)
        player.add_card(o["card"], "played")
        player.hand.remove(o["card"])


###############################################################################
class Test_Mastermind(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Mastermind", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mastermind"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a card"""
        self.plr.set_discard("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.plr.set_hand("Moat")
        self.plr.test_input = ["Play Moat"]
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
