#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Seaway"""
import unittest

from dominion import Card, Game, Piles, Event, Token


###############################################################################
class Event_Seaway(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = """Gain an Action card costing up to $4. Move your +1 Buy token to its pile.
        (When you play a card from that pile, you first get +1 Buy.)"""
        self.name = "Seaway"
        self.cost = 5

    def special(self, game, player):
        """Gain an Action card costing up to $4. Move your +1 Buy token to its pile."""
        if card := player.plr_gain_card(4, types={Card.CardType.ACTION: True}):
            player.place_token(Token.PLUS_1_BUY, card.pile)


###############################################################################
class Test_Seaway(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Seaway"], initcards=["Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Seaway"]

    def test_play(self):
        """Perform a Seaway"""
        self.plr.coins.add(5)
        self.plr.test_input = ["Get Militia"]
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertIn("Militia", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.which_token("Militia"), [Token.PLUS_1_BUY])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
