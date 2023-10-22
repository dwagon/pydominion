#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Champion(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "For the rest of the game +1 Action / Action; Defense"
        self.name = "Champion"
        self.permanent = True
        self.purchasable = False
        self.defense = True
        self.numcards = 5
        self.cost = 6

    def hook_post_action(self, game, player, card):
        player.add_actions(1)


###############################################################################
class Test_Champion(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Page", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Champion")

    def test_champion(self):
        """Play a champion"""
        self.plr.add_card(self.card, "duration")
        self.assertEqual(self.plr.actions.get(), 1)
        moat = self.g.get_card_from_pile("Moat")
        self.plr.add_card(moat, Piles.HAND)
        self.plr.play_card(moat)
        self.assertEqual(self.plr.actions.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
