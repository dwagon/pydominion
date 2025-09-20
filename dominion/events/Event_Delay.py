#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Delay"""

import unittest

from dominion import Game, Event, Piles


###############################################################################
class Event_Delay(Event.Event):
    """Delay"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = "menagerie"
        self.desc = """You may set aside an Action card from your hand. At the
            start of your next turn, play it."""
        self.name = "Delay"
        self.cost = 0

    def special(self, game, player):
        actions = []
        for card in player.piles[Piles.HAND]:
            if card.isAction():
                actions.append(card)
        if not actions:
            player.output("No actions to delay")
            return
        delay = player.card_sel(
            prompt="Set aside an action card to play next turn", cardsrc=actions
        )
        player.defer_card(delay[0])


###############################################################################
class TestDelay(unittest.TestCase):
    """Test Delay"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            events=["Delay"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Delay"]

    def test_play(self):
        """Perform a Delay"""
        self.plr.test_input = ["Select Moat"]
        self.plr.piles[Piles.HAND].set("Moat", "Copper", "Estate")
        self.plr.perform_event(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DEFER])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
