#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Toil """

import unittest
from dominion import Card, Game, Piles, Event


###############################################################################
class Event_Toil(Event.Event):
    """Toil"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Buy; You may play an Action card from your hand."
        self.name = "Toil"
        self.cost = 2
        self.buys = 1

    def special(self, game, player):
        """You may play an Action card from your hand."""
        action = player.card_sel(
            num=1,
            types={Card.CardType.ACTION: True},
            prompt="Play an action card?",
        )
        if action:
            player.play_card(action[0], cost_action=False)


###############################################################################
class TestToil(unittest.TestCase):
    """Test Toil"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Toil"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Toil"]
        self.card = self.g.get_card_from_pile("Moat")

    def test_play(self):
        """Perform a Toil"""
        self.plr.coins.add(2)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
