#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Chancellor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+2 Coin; You may immediately put your deck into your discard pile."
        self.name = "Chancellor"
        self.coin = 2
        self.cost = 3

    def special(self, game, player):
        ans = player.plr_choose_options(
            "Discard deck?", ("Don't Discard", False), ("Discard Deck", True)
        )
        if ans:
            for c in player.deck[:]:
                player.add_card(c, "discard")
                player.deck.remove(c)


###############################################################################
class Test_Chancellor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Chancellor"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g["Chancellor"].remove()
        self.plr.set_hand("Estate")
        self.plr.add_card(self.ccard, "hand")

    def test_nodiscard(self):
        self.plr.set_deck("Copper", "Silver", "Gold")
        self.plr.set_discard("Estate", "Duchy", "Province")
        self.plr.test_input = ["Don't discard"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.deck.size(), 3)
        self.assertEqual(self.plr.discardpile.size(), 3)

    def test_discard(self):
        self.plr.set_deck("Copper", "Silver", "Gold")
        self.plr.set_discard("Estate", "Duchy", "Province")
        self.plr.test_input = ["discard deck"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.deck.size(), 0)
        self.assertEqual(self.plr.discardpile.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
