#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card
from dominion.Player import Phase


###############################################################################
class Card_Devils_Workshop(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.NIGHT
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """If the number of cards you've gained this turn is: 2+,
            gain an Imp from its pile; 1, gain a card costing up to 4;
            0, gain a Gold."""
        self.name = "Devil's Workshop"
        self.cost = 4
        self.required_cards = [("Card", "Imp")]

    def night(self, game, player):
        nc = len(player.stats["gained"])
        player.output(f"You gained {nc} cards this turn")
        if nc >= 2:
            player.gain_card("Imp")
            player.output("Gained an Imp")
        elif nc == 1:
            player.plr_gain_card(4)
        else:
            player.gain_card("Gold")
            player.output("Gained a Gold")


###############################################################################
class Test_Devils_Workshop(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Devil's Workshop", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Devil's Workshop"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_0(self):
        self.plr.phase = Phase.NIGHT
        self.plr.play_card(self.card)
        try:
            self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_play_1(self):
        self.plr.phase = Phase.NIGHT
        self.plr.gain_card("Copper")
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        try:
            self.assertLessEqual(self.plr.piles[Piles.DISCARD][0].name, "Moat")
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise

    def test_play_2(self):
        self.plr.phase = Phase.NIGHT
        self.plr.gain_card("Copper")
        self.plr.gain_card("Estate")
        self.plr.play_card(self.card)
        try:
            self.assertIn("Imp", self.plr.piles[Piles.DISCARD])
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
