#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Samurai"""
import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Samurai(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION, Card.CardType.ATTACK]
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = """Each other player discards down to 3 cards in hand.
            At the start of each of your turns this game, +$1. (This stays in play.)"""
        self.name = "Samurai"
        self.cost = 6
        self.permanent = True

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """Each other player discards down to 3 cards in hand (once)"""
        for plr in player.attack_victims():
            plr.output(f"{player.name}'s Samurai: Discard down to 3 cards")
            plr.plr_discard_down_to(3)

    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        """At the start of each of your turns this game, +$1."""
        player.coins.add(1)
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    numtodiscard = len(player.piles[Piles.HAND]) - 3
    return player.pick_to_discard(numtodiscard)


###############################################################################
class Test_Samurai(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Samurai"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Samurai")

    def test_play(self) -> None:
        """Play card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.vic.test_input = ["1", "2", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(len(self.vic.piles[Piles.HAND]), 3)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
