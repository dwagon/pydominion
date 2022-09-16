#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Conjurer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.WIZARD,  # pylint: disable=no-member
            Card.CardType.DURATION,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 4
        self.name = "Conjurer"
        self.desc = """Gain a card costing up to $4.
            At the start of your next turn, put this into your hand."""

    def special(self, game, player):
        player.plr_gain_card(4)

    def duration(self, game, player):
        return {"dest": "hand"}


###############################################################################
class Test_Conjurer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Play a conjurer"""
        while True:
            card = self.g["Wizards"].remove()
            if card.name == "Conjurer":
                break
        self.plr.add_card(card, "hand")
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(card)
        self.assertIn("Silver", self.plr.discardpile)
        self.plr.end_turn()
        self.g.print_state()
        self.plr.start_turn()
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(card)
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
