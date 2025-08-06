#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Root_Cellar"""

import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Root_Cellar(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RISING_SUN
        self.desc = "+3 Cards; +1 Action; +3 Debt"
        self.name = "Root Cellar"
        self.cost = 3
        self.cards = 3
        self.actions = 1

    def special(self, game: "Game.Game", player: "Player.Player"):
        player.debt.add(3)


###############################################################################
class Test_Root_Cellar(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Root Cellar"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Root Cellar")

    def test_play(self) -> None:
        self.plr.add_card(self.card, Piles.HAND)
        debt = self.plr.debt.get()
        hand_size = len(self.plr.piles[Piles.HAND])
        actions = self.plr.actions.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.debt.get(), debt + 3)
        self.assertEqual(len(self.plr.piles[Piles.HAND]), hand_size + 3 - 1)  # -1 for card played
        self.assertEqual(self.plr.actions.get(), actions + 1 - 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
