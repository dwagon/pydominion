#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Bury"""

import unittest

from dominion import Card, Game, Event, Player, Piles


###############################################################################
class Event_Bury(Event.Event):
    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """+1 Buy; Put any card from your discard pile on the bottom of your deck."""
        self.name = "Bury"
        self.cost = 1
        self.buys = 1

    def special(self, game: Game.Game, player: Player.Player):
        """Put any card from your discard pile on the bottom of your deck."""
        if cards := player.card_sel(
            prompt="Put card from discard pile on the bottom of your deck", num=1, force=True, cardsrc=Piles.DISCARD
        ):
            player.move_card(cards[0], Piles.DECK)


###############################################################################
class TestBury(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, events=["Bury"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Bury"]

    def test_play(self):
        """Perform a Bury"""
        self.plr.coins.add(1)
        self.plr.piles[Piles.DISCARD].set("Estate", "Silver", "Duchy")
        self.plr.test_input = ["Select Silver"]
        self.plr.perform_event(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DECK])
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
