#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Elder(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_TOWNSFOLK,  # pylint: disable=no-member
        ]
        self.base = Game.ALLIES
        self.cost = 5
        self.coin = 2
        self.name = "Elder"
        self.desc = """+$2; Not Implemented: You may play an Action card from your hand.
            When it gives you a choice of abilities (e.g. “choose one”) this turn,
            you may choose an extra (different) option."""

    def special(self, game, player):
        pass


###############################################################################
class Test_Elder(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

        while True:
            card = self.g["Townsfolk"].remove()
            if card.name == "Elder":
                break
        self.card = card

    def test_play(self):
        """Play an elder"""
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
