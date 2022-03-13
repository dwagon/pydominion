#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


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
        c = player.nextCard()
        player.reveal_card(c)
        if c.cost <= 2 and not c.potcost and not c.debtcost:
            player.addCard(c, "hand")
            player.output("Moving {} from your deck to your hand".format(c.name))
        else:
            player.addCard(c, "topdeck")
            player.output("Keep {} on top of your deck".format(c.name))


###############################################################################
class Test_WilloWisp(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Will-o'-Wisp"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Will-o'-Wisp"].remove()

    def test_special_cheap(self):
        self.plr.setHand()
        self.plr.setDeck("Copper", "Estate")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_hand("Copper"))
        self.assertIsNotNone(self.plr.in_hand("Estate"))

    def test_special_expensive(self):
        self.plr.setHand()
        self.plr.setDeck("Gold", "Estate")
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNone(self.plr.in_hand("Gold"))
        self.assertIsNotNone(self.plr.in_deck("Gold"))
        self.assertIsNotNone(self.plr.in_hand("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
