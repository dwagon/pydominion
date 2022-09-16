#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Caravan(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+1 cards, +1 action; +1 card next turn"
        self.name = "Caravan"
        self.cards = 1
        self.actions = 1
        self.cost = 4

    def duration(self, game, player):
        """+1 card next turn"""
        player.pickup_cards(1, verb="Picked up from Caravan:")


###############################################################################
class Test_Caravan(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Caravan"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Caravan"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a caravan"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.durationpile.size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.assertEqual(self.plr.played.size(), 1)
        self.assertEqual(self.plr.played[-1].name, "Caravan")
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
