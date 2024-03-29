#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


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
        self.pile = "Wizards"

    def special(self, game, player):
        player.plr_gain_card(4)

    def duration(self, game, player):
        return {"dest": Piles.HAND}


###############################################################################
class TestConjurer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Play a conjurer"""
        card = self.g.get_card_from_pile("Wizards", "Conjurer")
        self.plr.add_card(card, Piles.HAND)
        self.plr.test_input = ["Get Silver"]
        self.plr.play_card(card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
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
