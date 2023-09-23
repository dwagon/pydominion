#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Marquis"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Marquis(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Marquis"
        self.buys = 1
        self.desc = "+1 Buy; +1 Card per card in your hand. Discard down to 10 cards in hand."
        self.cost = 6

    def special(self, game, player):
        hand_size = player.piles[Piles.HAND].size()
        player.pickup_cards(num=hand_size)
        player.plr_discard_down_to(10)


###############################################################################
class Test_Marquis(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Marquis"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Marquis")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
