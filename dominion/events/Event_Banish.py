#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Banish"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Event, Player


###############################################################################
class Event_Banish(Event.Event):
    """Banish"""

    def __init__(self):
        Event.Event.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "Exile any number of cards with the same name from your hand."
        self.name = "Banish"
        self.cost = 4

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        card_names = {_.name for _ in player.piles[Piles.HAND]}
        options: list[tuple[str, Any]] = [("Exile nothing", None)]
        for cname in card_names:
            options.append((f"Exile {cname} ({player.piles[Piles.HAND].count(cname)} in hand)", cname))
        card_name = player.plr_choose_options("Pick a card to exile", *options)
        if card_name is None:
            return
        if player.piles[Piles.HAND].count(card_name) == 1:
            count = 1
        else:
            options = []
            for i in range(player.piles[Piles.HAND].count(card_name) + 1):
                options.append((f"Exile {i} {card_name}", i))
            count = player.plr_choose_options("How many to exile", *options)
        for _ in range(count):
            exile_from_hand(player, card_name)


###############################################################################
def exile_from_hand(player: Player.Player, card_name: str) -> None:
    for card in player.piles[Piles.HAND]:
        if card.name == card_name:
            player.exile_card(card)
            break


###############################################################################
class Test_Banish(unittest.TestCase):
    """Test Banish"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            events=["Banish"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.events["Banish"]

    def test_Banish_multi(self) -> None:
        """Use Banish"""
        self.plr.coins.add(4)
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Estate", "2"]
        self.plr.perform_event(self.card)
        self.assertIn("Estate", self.plr.piles[Piles.EXILE])
        self.assertIn("Estate", self.plr.piles[Piles.HAND])

    def test_Banish_single(self) -> None:
        """Use Banish"""
        self.plr.coins.add(4)
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Estate", "Duchy")
        self.plr.test_input = ["Duchy"]
        self.plr.perform_event(self.card)
        self.assertIn("Duchy", self.plr.piles[Piles.EXILE])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
