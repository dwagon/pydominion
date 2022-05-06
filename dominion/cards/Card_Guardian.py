#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Guardian(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_NIGHT, Card.TYPE_DURATION]
        self.base = Game.NOCTURNE
        self.desc = """Until your next turn, when another player plays an
            Attack card, it doesn't affect you. At the start of your next turn,
            +1 Coin."""
        self.name = "Guardian"
        self.defense = True
        self.cost = 2

    def duration(self, game, player):
        player.add_coins(1)

    def hook_gain_this_card(self, game, player):
        return {"destination": "hand"}


###############################################################################
class Test_Guardian(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Guardian"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Guardian"].remove()

    def test_gain(self):
        self.plr.gain_card("Guardian")
        self.assertIn("Guardian", self.plr.hand)

    def test_duration(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.get_coins(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
