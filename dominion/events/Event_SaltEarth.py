#!/usr/bin/env python

import unittest
from dominion import Card, Game, Event


###############################################################################
class Event_SaltEarth(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1VP. Trash a Victory card from the Supply."
        self.name = "Salt the Earth"
        self.cost = 4

    def special(self, game, player):
        player.add_score("Salt the Earth", 1)
        stacks = game.getVictoryPiles()
        cp = player.card_sel(
            cardsrc=stacks, prompt="Trash a Victory card from the Supply"
        )
        if not cp:
            return
        cd = cp[0].remove()
        player.trash_card(cd)


###############################################################################
class Test_SaltEarth(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, eventcards=["Salt the Earth"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Salt the Earth"]

    def test_event(self):
        """Use Salt the Earth"""
        self.plr.coins.add(4)
        self.plr.test_input = ["Province"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.get_score_details()["Salt the Earth"], 1)
        self.assertIn("Province", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
