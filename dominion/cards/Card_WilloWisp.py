#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_WilloWisp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_SPIRIT]
        self.base = Game.NOCTURNE
        self.desc = "+1 Card; +1 Action; Reveal the top card of your deck. If it costs 2 or less, put it into your hand."
        self.name = "Will-o'-Wisp"
        self.purchasable = False
        self.cards = 1
        self.actions = 1
        self.insupply = False
        self.cost = 0

    def special(self, game, player):
        c = player.next_card()
        player.reveal_card(c)
        if c.cost <= 2 and not c.potcost and not c.debtcost:
            player.add_card(c, "hand")
            player.output(f"Moving {c.name} from your deck to your hand")
        else:
            player.add_card(c, "topdeck")
            player.output(f"Keep {c.name} on top of your deck")


###############################################################################
class Test_WilloWisp(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Will-o'-Wisp"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Will-o'-Wisp"].remove()

    def test_special_cheap(self):
        self.plr.set_hand()
        self.plr.set_deck("Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIn("Copper", self.plr.hand)
        self.assertIn("Estate", self.plr.hand)

    def test_special_expensive(self):
        self.plr.set_hand()
        self.plr.set_deck("Gold", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertNotIn("Gold", self.plr.hand)
        self.assertIsNotNone(self.plr.in_deck("Gold"))
        self.assertIn("Estate", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
