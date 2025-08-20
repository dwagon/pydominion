#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Port"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Phase, Player, NoCardException, OptionKeys


###############################################################################
class Card_Port(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Port"
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.numcards = 12

    def dynamic_description(self, player: Player.Player) -> str:
        if player.phase == Phase.BUY:
            return "+1 Card, +2 Actions; When you gain this, gain another Port"
        return "+1 Card, +2 Actions"

    def hook_gain_this_card(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """Gain another Port"""
        try:
            player.gain_card("Port", callhook=False)
        except NoCardException:
            player.output("No more ports")
        return {}


###############################################################################
class TestPort(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Port"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Port")

    def test_play(self) -> None:
        """Play a port"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_buy(self) -> None:
        """Buy a port"""
        self.plr.piles[Piles.DISCARD].set()
        self.plr.coins.set(5)
        self.plr.buy_card("Port")
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Port")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
