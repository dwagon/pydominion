#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Nobles(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "2VP, choose +3 cards or +2 actions"
        self.name = "Nobles"
        self.victory = 2
        self.cost = 6

    def special(self, game, player):
        """Choose one: +3 Cards; or +2 Actions"""
        cards = player.plr_choose_options("Choose one", ("+3 Cards", True), ("+2 Actions", False))
        if cards:
            player.pickup_cards(3)
        else:
            player.add_actions(2)


###############################################################################
class Test_Nobles(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Nobles"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Nobles")
        self.plr.add_card(self.card, Piles.HAND)

    def test_cards(self):
        """Play the Nobles - chosing cards"""
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 8)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_actions(self):
        """Play the Nobles - chosing actions"""
        self.plr.test_input = ["1"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_score(self):
        """Score the nobles"""
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Nobles"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
