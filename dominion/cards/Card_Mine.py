#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Mine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "Trash a treasure, gain a better treasure"
        self.name = "Mine"
        self.cost = 5

    def special(self, game, player):
        """Trash a treasure card from your hand. Gain a treasure card
        costing up to 3 more, put it in your hand"""
        options = [{"selector": "0", "print": "Don't trash a card", "card": None}]
        index = 1
        for c in player.hand:
            if c.isTreasure():
                sel = "%s" % index
                options.append({"selector": sel, "print": f"Trash/Upgrade {c.name}", "card": c})
                index += 1
        player.output("Trash a treasure to gain a better one")
        o = player.user_input(options, "Trash which treasure?")
        if o["card"]:
            val = o["card"].cost
            # Make an assumption and pick the best treasure card
            # TODO - let user pick
            for tc in game._base_cards:
                if game[tc].cost == val + 3:
                    c = player.gain_card(tc, "hand")
                    player.output(f"Converted to {c.name}")
                    player.trash_card(o["card"])
                    break
            else:  # pragma: no cover
                player.output("No appropriate treasure card exists")


###############################################################################
class Test_Mine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mine"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mine"].remove()

    def test_convcopper(self):
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand[0].name, "Silver")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_actions(), 0)

    def test_convnothing(self):
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand[0].name, "Copper")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
