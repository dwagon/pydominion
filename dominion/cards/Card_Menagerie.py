#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Menagerie(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.CORNUCOPIA
        self.desc = """+1 Action. Reveal your hand. If there are no duplicate cards in it, +3 Cards. Otherwise, +1 Card."""
        self.name = "Menagerie"
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        hand = set()
        for card in player.hand:
            player.reveal_card(card)
            hand.add(card.name)
        if len(hand) == player.hand.size():
            player.output("No duplicates - picking up 3 cards")
            player.pickup_cards(3)
        else:
            player.output("Duplicates - picking up 1 card")
            player.pickup_cards(1)


###############################################################################
class Test_Menagerie(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Menagerie"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Menagerie"].remove()

    def test_play_unique(self):
        self.plr.hand.set("Copper", "Estate", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_play_non_unique(self):
        self.plr.hand.set("Copper", "Copper", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
