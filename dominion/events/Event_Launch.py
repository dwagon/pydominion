#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Launch"""
import unittest

from dominion import Card, Game, Event, Phase, Player, NoCardException


###############################################################################
class Event_Launch(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = "Once per turn: Return to your Action phase. +1 Card, +1 Action, and +1 Buy."
        self.name = "Launch"
        self.cost = 3

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if not player.do_once("Launch"):
            player.output("Can only play Launch once per turn")
            return
        if player.phase == Phase.BUY:
            player.phase = Phase.ACTION
            try:
                player.pickup_card()
            except NoCardException:
                pass
            player.actions.add(1)
            player.buys.add(1)


###############################################################################
class TestLaunch(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Launch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Launch"]

    def test_play(self) -> None:
        """Play"""
        self.plr.phase = Phase.BUY
        self.plr.coins.add(3)
        actions = self.plr.actions.get()
        buys = self.plr.buys.get()
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.actions.get(), actions + 1)
        self.assertEqual(
            self.plr.buys.get(), buys + 1 - 1
        )  # -1 for performing the event
        self.assertEqual(self.plr.phase, Phase.ACTION)

    def test_play_twice(self) -> None:
        """Can we only play once"""
        self.plr.phase = Phase.BUY
        self.plr.coins.add(6)
        self.plr.perform_event(self.card)
        self.plr.phase = Phase.BUY
        self.plr.perform_event(self.card)
        self.assertEqual(self.plr.phase, Phase.BUY)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
