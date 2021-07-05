#!/usr/bin/env python

import unittest
import Game
import Card


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
                options.append(
                    {"selector": sel, "print": "Trash/Upgrade %s" % c.name, "card": c}
                )
                index += 1
        player.output("Trash a treasure to gain a better one")
        o = player.userInput(options, "Trash which treasure?")
        if o["card"]:
            val = o["card"].cost
            # Make an assumption and pick the best treasure card
            # TODO - let user pick
            for tc in game.base_cards:
                if game[tc].cost == val + 3:
                    c = player.gainCard(tc, "hand")
                    player.output("Converted to %s" % c.name)
                    player.trashCard(o["card"])
                    break
            else:  # pragma: no cover
                player.output("No appropriate treasure card exists")


###############################################################################
class Test_Mine(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Mine"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mine"].remove()

    def test_convcopper(self):
        self.plr.setHand("Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand[0].name, "Silver")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_actions(), 0)

    def test_convnothing(self):
        self.plr.setHand("Copper")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand[0].name, "Copper")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
