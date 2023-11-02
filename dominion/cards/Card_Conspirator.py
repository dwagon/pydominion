#!/usr/bin/env python

import contextlib
import unittest
from dominion import Game, Card, Piles, Player, NoCardException


###############################################################################
class Card_Conspirator(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = """+2 coin. If you've played 3 or more actions this turn (counting
            this); +1 card, +1 action """
        self.name = "Conspirator"
        self.coin = 2
        self.cost = 4

    def special(self, game: Game.Game, player: Player.Player) -> None:
        if self.num_actions_played(player) >= 3:
            with contextlib.suppress(NoCardException):
                player.pickup_card()
            player.add_actions(1)

    def num_actions_played(self, player: Player.Player) -> int:
        return sum(1 for _ in player.piles[Piles.PLAYED] if _.isAction())


###############################################################################
class Test_Conspirator(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Conspirator", "Witch"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Conspirator")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play the conspirator with not enough actions"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_actions(self) -> None:
        """Play the conspirator with enough actions"""
        self.plr.piles[Piles.PLAYED].set("Witch", "Witch", "Witch")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
