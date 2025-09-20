#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Invasion"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, Player, NoCardException


###############################################################################
class Event_Invasion(Event.Event):
    def __init__(self) -> None:
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.PLUNDER
        self.desc = """You may play an Attack from your hand. Gain a Duchy. Gain an Action onto your deck.
            Gain a Loot; play it."""
        self.name = "Invasion"
        self.required_cards = ["Loot"]
        self.cost = 10

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """You may play an Attack from your hand. Gain a Duchy. Gain an Action onto your deck. Gain a Loot; play it."""
        # Attack
        if attacks := [_ for _ in player.piles[Piles.HAND] if _.isAttack()]:
            choices: list[tuple[str, Any]] = [("Do not attack", None)]
            for card in attacks:
                choices.append((f"Attack with {card}?", card))
            if do_attack := player.plr_choose_options("Use Invasion to attack?", *choices):
                player.play_card(do_attack, cost_action=False)

        # Gain a Duchy
        try:
            player.gain_card("Duchy")
        except NoCardException:  # pragma: no coverage
            player.output("No more Duchys")

        # Gain an Action onto your deck
        player.plr_gain_card(999, types={Card.CardType.ACTION: True}, destination=Piles.DECK)

        # Gain a Loot
        try:
            loot = player.gain_card("Loot")
        except NoCardException:  # pragma: no coverage
            player.output("No more Loot")
            return
        else:  # Play it
            player.reveal_card(loot)
            player.play_card(loot, cost_action=False)


###############################################################################
class TestInvasion(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2, events=["Invasion"], initcards=["Witch", "Village"], loot_path="tests/loot"
        )
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.events["Invasion"]

    def test_play_with_attack(self) -> None:
        """Use Invasion having an attack"""
        self.plr.coins.set(10)
        self.plr.piles[Piles.HAND].set("Witch", "Silver", "Estate", "Gold")
        self.plr.test_input = ["Attack with Witch", "Get Village"]
        self.plr.perform_event(self.card)
        self.g.print_state()
        self.assertIn("Curse", self.vic.piles[Piles.DISCARD])
        self.assertIn("Witch", self.plr.piles[Piles.PLAYED])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertIn("Village", self.plr.piles[Piles.DECK])
        found = any([True for _ in self.plr.all_cards() if _.isLoot()])
        self.assertTrue(found)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
