#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Loan(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = """+1 Coin; When you play this, reveal cards from your
            deck until you reveal a Treasure. Discard it or trash it. Discard
            the other cards."""
        self.name = "Loan"
        self.cost = 3
        self.coin = 1

    def special(self, game, player):
        """When you play this, reveal cards from your deck until
        you reveal a Treasure. Discard it or trash it. Discard the
        other cards"""
        while True:
            c = player.next_card()
            player.reveal_card(c)
            if c.isTreasure():
                break
            player.output(f"Revealed and discarded {c.name}")
            player.discard_card(c)
        discard = player.plr_choose_options(
            "What to do?", (f"Discard {c.name}", True), (f"Trash {c.name}", False)
        )
        if discard:
            player.discard_card(c)
        else:
            player.trash_card(c)


###############################################################################
class Test_Loan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Loan"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.loan = self.plr.gain_card("Loan", "hand")

    def test_discard(self):
        tsize = self.g.trash_size()
        self.plr.set_deck("Estate", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Discard Gold"]
        self.plr.play_card(self.loan)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertEqual(self.g.trash_size(), tsize)

    def test_trash(self):
        tsize = self.g.trash_size()
        self.plr.set_deck("Estate", "Gold", "Estate", "Duchy")
        self.plr.test_input = ["Trash Gold"]
        self.plr.play_card(self.loan)
        self.assertEqual(self.g.trash_size(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertNotIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
