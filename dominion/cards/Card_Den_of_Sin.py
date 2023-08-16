#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Den_of_Sin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Den of Sin"
        self.cost = 2

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "At the start of your next turn, +2 Cards; This is gained to your hand (instead of your discard pile)."
        return "At the start of your next turn, +2 Cards"

    def duration(self, game, player):
        for _ in range(2):
            player.pickup_card()

    def hook_gain_this_card(self, game, player):
        return {"destination": Piles.HAND}


###############################################################################
class Test_Den_of_Sin(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Den of Sin"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Den of Sin"].remove()

    def test_gain(self):
        self.plr.gain_card("Den of Sin")
        self.assertIn("Den of Sin", self.plr.piles[Piles.HAND])

    def test_duration(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
