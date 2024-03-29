#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Merchant_Camp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.DURATION,
            Card.CardType.ACTION,
            Card.CardType.LIAISON,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Merchant Camp"
        self.actions = 2
        self.coin = 1
        self.desc = "+2 Actions; +$1; When you discard this from play, you may put it onto your deck."
        self.cost = 3

    def hook_discard_this_card(self, game, player, source):
        opt = player.plr_choose_options("Put Merchant Camp onto deck?", ("Onto deck", True), ("Onto discard", False))
        if opt:
            player.move_card(self, "topdeck")


###############################################################################
class Test_Merchant_Camp(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Merchant Camp", "moat"], ally="Plateau Shepherds")
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Merchant Camp")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card and discard to deck"""
        self.plr.test_input = ["Onto deck"]
        self.plr.play_card(self.card)
        self.plr.discard_card(self.card)
        self.assertNotIn("Merchant Card", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DECK].top_card(), self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
