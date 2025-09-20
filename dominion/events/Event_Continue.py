#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Continue"""
import unittest
from typing import Any

from dominion import Card, Game, Event, Player, Phase, Piles


###############################################################################
class Event_Continue(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Once per turn: Gain a non-Attack Action card costing up to $4.
            Return to your Action phase and play it. +1 Action and +1 Buy."""
        self.name = "Continue"
        self.cost = 0
        self.debtcost = 8

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Once per turn: Gain a non-Attack Action card costing up to $4. Return to your Action phase and play it."""
        if not player.do_once("Continue"):
            player.output("Can only play Continue once per turn")
            return
        actions = [name for name in game.get_action_piles(4) if not game.card_instances[name].isAttack()]
        choices: list[tuple[str, Any]] = [("Do nothing", None)]
        for card_name in actions:
            choices.append((f"Gain and Play {card_name}", card_name))
        if choice := player.plr_choose_options("Gain a card and return to Action phase and play it", *choices):
            card = player.gain_card(choice)
            player.phase = Phase.ACTION
            player.play_card(card, cost_action=False)
        player.actions.add(1)
        player.buys.add(1)


###############################################################################
class TestContinue(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, events=["Continue"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.event = self.g.events["Continue"]

    def test_play(self) -> None:
        self.plr.coins.set(3)
        actions = self.plr.actions.get()
        buys = self.plr.actions.get()
        self.plr.test_input = ["Moat"]
        self.plr.perform_event(self.event)
        self.assertEqual(self.plr.debt.get(), 8)
        self.assertEqual(self.plr.actions.get(), actions + 1)  # +1 from event
        self.assertEqual(self.plr.buys.get(), buys + 1 - 1)  # +1 from event - 1 for buying event
        self.assertIn("Moat", self.plr.piles[Piles.PLAYED])
        self.assertEqual(self.plr.phase, Phase.ACTION)

        self.plr.debt.set(0)
        self.plr.perform_event(self.event)
        self.assertIn("Can only play Continue once per turn", self.plr.messages)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
