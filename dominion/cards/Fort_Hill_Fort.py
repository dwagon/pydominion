#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Hill_Fort"""

import unittest
from dominion import Game, Card


###############################################################################
class Card_Hill_Fort(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FORT]  # pylint: disable=no-member
        self.base = Game.ALLIES
        self.cost = 5
        self.name = "Hill Fort"
        self.desc = """Gain a card costing up to $4.
            Choose one: Put it into your hand; or +1 Card and +1 Action."""

    def special(self, game, player):
        chc = player.plr_choose_options(
            "Choose One - gain a card costing up to $4 and ...",
            ("put it into your hand", "hand"),
            ("+1 Card and +1 Action", "disc"),
        )
        if chc == "hand":
            player.plr_gain_card(cost=4, destination="hand")
        elif chc == "disc":
            player.plr_gain_card(cost=4)
            player.pickup_card()
            player.add_actions(1)


###############################################################################
class Test_Hill_Fort(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g["Forts"].remove()
            if self.card.name == "Hill Fort":
                break
        self.plr.add_card(self.card, "hand")

    def test_play_hand(self):
        self.plr.test_input = ["put it", "Get Silver"]
        hndsz = self.plr.hand.size()
        acts = self.plr.get_actions()
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_hand("Silver"))
        self.assertEqual(self.plr.hand.size(), hndsz)
        self.assertEqual(self.plr.get_actions(), acts - 1)

    def test_play_disc(self):
        self.plr.test_input = ["card", "Get Silver"]
        hndsz = self.plr.hand.size()
        acts = self.plr.get_actions()
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_hand("Silver"))
        self.assertEqual(self.plr.hand.size(), hndsz + 1 - 1)
        self.assertEqual(self.plr.get_actions(), acts - 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
