#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Longship"""

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Longship(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "+2 Actions; At the start of your next turn, +2 Cards."
        self.name = "Longship"
        self.cost = 5
        self.actions = 2

    def duration(self, game, player):
        player.pickup_cards(2)


###############################################################################
class Test_Longship(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Longship"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Longship")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Longship"""
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(
            self.plr.actions.get(), actions + 2 - 1
        )  # -1 for playing Longship
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
