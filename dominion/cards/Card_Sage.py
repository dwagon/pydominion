#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Sage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+1 Action. Reveal cards from the top of your deck
        until you reveal one costing 3 or more.
        Put that card into your hand and discard the rest."""
        self.name = "Sage"
        self.actions = 1
        self.cost = 3

    ###########################################################################
    def special(self, game, player):
        todiscard = []
        while True:
            card = player.next_card()
            if not card:
                player.output("No card costing 3 or more found")
                break
            player.reveal_card(card)
            if card.cost >= 3:
                player.output("Adding %s to hand" % card.name)
                player.add_card(card, "hand")
                break
            player.output("Discarding %s" % card.name)
            todiscard.append(card)
        for card in todiscard:
            player.discardCard(card)


###############################################################################
class Test_Sage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Sage"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Sage"].remove()

    def test_play(self):
        """Pick a card out of the pile"""
        self.plr.set_deck("Gold", "Copper", "Copper", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_hand("Gold"))

    def test_exhaust_deck(self):
        """No good card to pick out of the pile"""
        self.plr.set_deck("Copper", "Copper", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.deck.size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
