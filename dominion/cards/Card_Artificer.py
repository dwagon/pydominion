#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Artificer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ADVENTURE
        self.desc = """+1 Card, +1 Action, +1 Coin; Discard any number of cards.
            You may gain a card costing exactly 1 per card discarded, putting it on top of your deck"""
        self.name = "Artificer"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 5

    def special(self, game, player):
        """Discard any number of cards. You may gain a card costing
        exactly 1 per card discarded, putting it on top of your deck"""
        todiscard = player.plr_discard_cards(
            anynum=True, prompt="Select which card(s) to discard"
        )
        cost = len(todiscard)
        player.plr_gain_card(
            cost=cost,
            modifier="equal",
            destination="topdeck",
            prompt="Gain a card costing %d" % cost,
        )


###############################################################################
class Test_Artificer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Artificer"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Artificer"].remove()

    def test_play(self):
        """Play an artificer - discard none and pick up a copper"""
        self.plr.set_deck("Province")
        self.plr.set_hand()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["finish", "copper"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.deck[0].name, "Copper")

    def test_play_more(self):
        """Play an artificer - discard three and pick up a silver"""
        self.plr.set_deck("Gold")
        self.plr.set_hand("Estate", "Duchy", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "discard estate",
            "discard duchy",
            "discard province",
            "finish",
            "get silver",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertEqual(self.plr.deck[0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
