#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Groom """


import contextlib
import unittest
from dominion import Game, Card, Piles, NoCardException


###############################################################################
class Card_Groom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.cost = 4
        self.name = "Groom"
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain a card costing up to 4 Coin. If it's an...
            Action card, gain a Horse;
            Treasure card, gain a Silver;
            Victory card, +1 Card and +1 Action."""
        self.required_cards = [("Card", "Horse")]

    def special(self, game, player):
        card = player.plr_gain_card(4)
        if card.isAction():
            player.gain_card("Horse")
        if card.isTreasure():
            player.gain_card("Silver")
        if card.isVictory():
            with contextlib.suppress(NoCardException):
                player.pickup_card()
            player.add_actions(1)


###############################################################################
class Test_Groom(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Groom", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Groom")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard_action(self):
        """Play Card"""
        self.plr.test_input = ["Get Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Horse", self.plr.piles[Piles.DISCARD])

    def test_playcard_victory(self):
        """Play Card"""
        self.plr.test_input = ["Get Estate"]
        self.plr.play_card(self.card)
        self.assertNotIn("Horse", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
