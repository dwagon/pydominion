#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Trader(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.HINTERLANDS
        self.desc = """Trash a card from your hand. Gain a number of Silvers equal to its cost in coins.
        When you would gain a card, you may reveal this from your hand. If you do, instead, gain a Silver."""
        self.name = "Trader"
        self.cost = 4

    def special(self, game, player):
        card = player.plr_trash_card(
            prompt="Trash a card from your hand. Gain a number of Silvers equal to its cost in coins."
        )
        if card:
            player.output(f"Gaining {card[0].cost} Silvers")
            for _ in range(card[0].cost):
                player.gain_card("Silver")

    def hook_gain_card(self, game, player, card):
        if card.name == "Silver":
            return {}
        silver = player.plr_choose_options(
            f"From your Trader gain {card.name} or gain a Silver instead?",
            (f"Still gain {card.name}", False),
            ("Instead gain Silver", True),
        )
        if silver:
            return {"replace": "Silver", "destination": "discard"}
        return {}


###############################################################################
class Test_Trader(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Trader"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Trader"].remove()

    def test_play(self):
        """Play a trader - trashing an estate"""
        tsize = self.g.trash_size()
        self.plr.hand.set("Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["estate", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.discardpile.size(), 2)
        for i in self.plr.discardpile:
            self.assertEqual(i.name, "Silver")
        self.assertEqual(self.g.trash_size(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Estate"))

    def test_gain(self):
        self.plr.test_input = ["Instead"]
        self.plr.add_card(self.card, "hand")
        self.plr.set_coins(6)
        self.plr.buy_card(self.g["Gold"])
        self.assertIn("Silver", self.plr.discardpile)
        self.assertNotIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
