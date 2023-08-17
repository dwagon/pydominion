#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Advance(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "You may trash an Action card from your hand. If you do, gain an Action card costing up to 6."
        self.name = "Advance"
        self.cost = 0

    def special(self, game, player):
        actions = [c for c in player.piles[Piles.HAND] if c.isAction()]
        trash = player.plr_trash_card(
            prompt="Trash a card to gain an action costing up to 6", cardsrc=actions
        )
        if trash:
            player.plr_gain_card(6, types={Card.CardType.ACTION: True})


###############################################################################
class Test_Advance(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            eventcards=["Advance"],
            initcards=["Moat", "Lurker"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Advance"]

    def test_advance(self):
        """Use Advance twice"""
        self.plr.piles[Piles.HAND].set("Moat")
        self.plr.test_input = ["Trash moat", "Get Lurker"]
        self.plr.perform_event(self.card)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Lurker"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
