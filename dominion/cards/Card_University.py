#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


class Card_University(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALCHEMY
        self.desc = "Gain an action card costing up to 5"
        self.name = "University"
        self.cost = 2
        self.required_cards = ["Potion"]
        self.potcost = True

    def special(self, game, player):
        """Gain an action card costing up to 5"""
        card = player.plr_gain_card(5, types={Card.CardType.ACTION: True})
        if card:
            player.output(f"Gained {card} from university")


###############################################################################
class TestUniversity(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["University"],
            badcards=[
                "Inn",
                "Death Cart",
                "Blessed Village",
                "Cursed Village",
                "Experiment",
                "Ducat",
                "Hostelry",
            ],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.university = self.g.get_card_from_pile("University")
        self.plr.add_card(self.university, Piles.HAND)

    def test_gain(self):
        self.plr.test_input = ["1"]
        self.plr.play_card(self.university)
        try:
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
            self.assertTrue(self.plr.piles[Piles.DISCARD][0].isAction())
            self.assertLessEqual(self.plr.piles[Piles.DISCARD][0].cost, 5)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_none(self):
        self.plr.test_input = ["0"]
        self.plr.play_card(self.university)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
