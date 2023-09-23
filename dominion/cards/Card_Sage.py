#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Sage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
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
                player.add_card(card, Piles.HAND)
                break
            player.output("Discarding %s" % card.name)
            todiscard.append(card)
        for card in todiscard:
            player.discard_card(card)


###############################################################################
class Test_Sage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Sage"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Sage")

    def test_play(self):
        """Pick a card out of the pile"""
        self.plr.piles[Piles.DECK].set("Gold", "Copper", "Copper", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.HAND])

    def test_exhaust_deck(self):
        """No good card to pick out of the pile"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DECK].size(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
