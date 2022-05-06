#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Countinghouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = """Look through the discard pile, reveal any number of
            copper cards from it, and put them into your hand."""
        self.name = "Counting House"
        self.cost = 5

    def special(self, game, player):
        count = 0
        for c in player.discardpile:
            game.print_state()
            if c.name == "Copper":
                player.move_card(c, "hand")
                count += 1
        player.output(f"Picked up {count} coppers")


###############################################################################
class Test_Countinghouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Counting House"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ch = self.g["Counting House"].remove()
        self.plr.hand.set()
        self.plr.add_card(self.ch, "hand")

    def test_pullcoppers(self):
        self.plr.discardpile.set("Copper", "Gold", "Duchy", "Copper")
        self.plr.play_card(self.ch)
        self.assertEqual(self.plr.hand.size(), 2)
        for c in self.plr.hand:
            self.assertEqual(c.name, "Copper")
        self.assertNotIn("Copper", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
