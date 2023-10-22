#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Enhance(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """You may trash a non-Victory card from your hand,
            to gain a card costing up to 2 Coin more than it."""
        self.name = "Enhance"
        self.cost = 3

    def special(self, game, player):
        crds = [_ for _ in player.piles[Piles.HAND] if not _.isVictory()]
        if not crds:
            player.output("No non-Victory cards available")
            return
        tc = player.plr_trash_card(
            prompt="Trash to gain a card costing 2 more than",
            printcost=True,
            cardsrc=crds,
        )
        if not tc:
            return
        new_cost = tc[0].cost + 2
        player.plr_gain_card(cost=new_cost, force=True)


###############################################################################
class TestEnhance(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            events=["Enhance"],
            initcards=["Festival"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Enhance"]

    def test_play(self):
        """Perform an Enhance"""
        self.plr.coins.add(3)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        self.plr.test_input = ["Trash Silver", "Get Festival"]
        self.plr.perform_event(self.card)
        self.assertIn("Silver", self.g.trash_pile)
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Festival"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
