#!/usr/bin/env python
# pylint: disable=protected-access

import unittest
import random
from typing import Any

from dominion import Card, PlayArea, Game, Piles, Player
from dominion.Option import Option

DRUID = "druid"


###############################################################################
class Card_Druid(Card.Card):
    """Druid"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Buy; Receive one of the set-aside Boons"
        self.name = "Druid"
        self.buys = 1
        self.cost = 2

    def setup(self, game: Game.Game) -> None:
        game.specials[DRUID] = PlayArea.PlayArea([])
        random.shuffle(game.boons)
        for _ in range(3):
            game.specials[DRUID].add(game.boons.pop())

    def special(self, game: Game.Game, player: Player.Player) -> None:
        options: list[Option | dict[str, Any]] = []
        for i in range(3):
            boon = list(game.specials[DRUID])[i]
            to_print = f"Receive {boon.name}: {boon.description(player)}"
            options.append({"selector": f"{i}", "print": to_print, "boon": boon})
        b = player.user_input(options, "Which boon? ")
        player.receive_boon(boon=b["boon"], discard=False)


###############################################################################
class TestDruid(unittest.TestCase):
    """Test Druid"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Druid", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Druid")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Druid"""
        self.plr.test_input = ["0", "0"]
        self.plr.play_card(self.card)
        self.assertGreaterEqual(self.plr.buys.get(), 2)

    def test_set_aside(self) -> None:
        """Test that we don't get a set aside boon"""
        set_aside = {
            _.name for _ in self.g.specials[DRUID]
        }  # pylint: disable=no-member
        left = {_.name for _ in self.g.boons}
        if set_aside.intersection(left):
            self.fail("Set aside boons not set aside")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
