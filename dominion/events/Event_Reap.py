#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Reap"""
import unittest
from typing import Optional

from dominion import Card, Game, Piles, Event, PlayArea


###############################################################################
class Event_Reap(Event.Event):
    """Reap"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = """Gain a Gold. Set it aside. If you do, at the start of your next turn, play it."""
        self.name = "Reap"
        self.cost = 7

    def special(self, game, player):
        gold = player.gain_card("Gold")
        if not hasattr(player, "_reap_reserve"):
            player._reap_reserve = PlayArea.PlayArea("Reap", game)
        player._reap_reserve.add(gold)
        player.secret_count += 1
        player.piles[Piles.DISCARD].remove(gold)
        gold.location = "reap_reserve"

    def duration(self, game, player):
        if not hasattr(player, "_reap_reserve"):
            return
        for card in player._reap_reserve:
            player.play_card(card, cost_action=False, discard=False)
            player.add_card(card, Piles.PLAYED)
            player.secret_count -= 1
        player._reap_reserve.empty()


###############################################################################
class TestReap(unittest.TestCase):
    """Test Reap"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Reap"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Reap"]

    def test_rush(self):
        """Use Reap"""
        self.plr.coins.set(7)
        self.plr.perform_event(self.event)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertIn("Gold", self.plr.piles[Piles.PLAYED])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
