#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Ghost_Town(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.DURATION]
        self.base = Card.CardExpansion.NOCTURNE
        self.name = "Ghost Town"
        self.cost = 3

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """At the start of your next turn, +1 Card and +1 Action. This
                is gained to your hand (instead of your discard pile)."""
        return "At the start of your next turn, +1 Card and +1 Action."

    def hook_gain_this_card(self, game, player):
        return {"destination": Piles.HAND}

    def duration(self, game, player):
        player.pickup_card()
        player.add_actions(1)


###############################################################################
class Test_Ghost_Town(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Ghost Town"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.gtown = self.g["Ghost Town"].remove()

    def test_play_card(self):
        """Play Ghost Town"""
        self.plr.add_card(self.gtown, Piles.HAND)
        self.plr.play_card(self.gtown)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self):
        self.plr.gain_card("Ghost Town")
        self.assertNotIn("Ghost Town", self.plr.piles[Piles.DISCARD])
        self.assertIn("Ghost Town", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
