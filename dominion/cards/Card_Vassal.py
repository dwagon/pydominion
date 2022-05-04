#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Vassal(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.name = "Vassal"
        self.coin = 2
        self.cost = 3
        self.desc = "+2 Coin; Discard the top card of your deck. If it is an Action card, you may play it."

    def special(self, game, player):
        card = player.next_card()
        player.reveal_card(card)
        if card.isAction():
            player.add_card(card, "hand")
            player.play_card(card, costAction=False)
        else:
            player.add_card(card, "discard")


###############################################################################
class Test_Vassal(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Vassal", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Vassal"].remove()

    def test_play_action(self):
        """Play a Vassal with action next"""
        self.plr.set_deck("Silver", "Gold", "Moat")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIsNotNone(self.plr.in_played("Moat"))
        self.assertEqual(self.plr.hand.size(), 5 + 2)

    def test_play_non_action(self):
        """Play a Vassal with non-action next"""
        self.plr.set_deck("Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertIn("Gold", self.plr.discardpile)
        self.assertEqual(self.plr.hand.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
