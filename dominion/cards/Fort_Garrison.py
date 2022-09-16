#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Garrison(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.DURATION,
            Card.CardType.FORT,  # pylint: disable=no-member
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.coin = 2
        self.name = "Garrison"
        self.desc = """+$2; This turn, when you gain a card, add a token here.
            At the start of your next turn, remove them for +1 Card each."""
        self._tokens = 0

    def hook_gain_card(self, game, player, card):
        self._tokens += 1

    def duration(self, game, player):
        if self._tokens:
            player.output(f"Picking up {self._tokens} cards from Garrison")
            player.pickup_cards(self._tokens)
            self._tokens = 0


###############################################################################
class Test_Garrison(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g["Forts"].remove()
            if self.card.name == "Garrison":
                break
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a garrison"""
        self.plr.test_input = ["Get Silver"]
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 2)
        self.plr.gain_card("Estate")
        self.plr.gain_card("Copper")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
