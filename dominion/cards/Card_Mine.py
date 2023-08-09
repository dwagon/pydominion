#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Mine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash a treasure, gain a better treasure"
        self.name = "Mine"
        self.cost = 5

    def special(self, game, player):
        """Trash a treasure card from your hand. Gain a treasure card
        costing up to 3 more, put it in your hand"""
        options = [{"selector": "0", "print": "Don't trash a card", "card": None}]
        index = 1
        for card in player.hand:
            if card.isTreasure():
                sel = "%s" % index
                options.append({"selector": sel, "print": f"Trash/Upgrade {card.name}", "card": card})
                index += 1
        player.output("Trash a treasure to gain a better one")
        o = player.user_input(options, "Trash which treasure?")
        if o["card"]:
            val = o["card"].cost
            # Make an assumption and pick the best treasure card
            # TODO - let user pick
            for tc in game._base_cards:
                if game[tc].cost == val + 3:
                    card = player.gain_card(tc, "hand")
                    if not card:
                        player.output("No suitable cards left")
                        break
                    player.output(f"Converted to {card.name}")
                    player.trash_card(o["card"])
                    break
            else:  # pragma: no cover
                player.output("No appropriate treasure card exists")


###############################################################################
class TestMine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mine"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mine"].remove()

    def test_convert_copper(self):
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand[0].name, "Silver")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_convert_nothing(self):
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand[0].name, "Copper")
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)

    def test_convert_nothing_left(self):
        """Test where the destination treasure is no longer available"""
        while self.g["Silver"]:
            self.plr.gain_card("Silver")
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand[0].name, "Copper")
        self.assertFalse(self.plr.discardpile.is_empty())
        self.assertEqual(self.plr.hand.size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
